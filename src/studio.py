"""Studio: watch the video slide by slide (one slide = one narration line), edit the
narration and the Manim code, and rebuild a scene (voice -> render -> mix).

    python studio.py            # then open http://localhost:8765

Uses only the standard library. Run it from anywhere; paths are relative to this file.
Set MANIM / PYTHON env vars if manim or python are not the ones on PATH.
"""
import json
import os
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
PY = os.environ.get("PYTHON", sys.executable)
MANIM = os.environ.get("MANIM", os.path.join(os.path.dirname(PY), "manim"))
VIDEO = os.path.join(ROOT, "final_720p30.mp4")
PORT = int(os.environ.get("PORT", "8765"))

STATE = {"running": False, "log": "", "scene": None, "ok": None}


def scenes():
    import importlib
    import pacing
    importlib.reload(pacing)
    nar = json.load(open(os.path.join(ROOT, "narration.json"), encoding="utf8"))
    tf = os.path.join(ROOT, "audio", "voice", "timing.json")
    timing = json.load(open(tf)) if os.path.exists(tf) else {}
    out, t = [], 0.0
    for f, sc, _ in pacing.SCENES:
        v = os.path.join(ROOT, "media", "videos", f[:-3], "720p30", sc + ".mp4")
        try:
            d = float(subprocess.check_output(["ffprobe", "-v", "0", "-show_entries", "format=duration",
                                               "-of", "csv=p=0", v]))
        except Exception:
            d = 0.0
        src = open(os.path.join(ROOT, f), encoding="utf8").read()
        m = re.search(r"^class %s\(" % sc, src, re.M)
        line = src[:m.start()].count("\n") + 1 if m else 1
        lines = [{"start": s, "end": e, "text": c} for s, e, c in timing.get(sc, {}).get("lines", [])]
        if not lines:                      # a scene with no narration: one slide for the whole scene
            lines = [{"start": 0.0, "end": d, "text": "(no narration)"}]
        out.append({"name": sc, "file": f, "line": line, "offset": t, "duration": d,
                    "lines": lines, "narration": nar.get(sc, [])})
        t += d
    return out


def run(cmd):
    STATE["log"] += "$ " + " ".join(cmd) + "\n"
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         env={**os.environ, "SFX_LOG": os.path.join(ROOT, "audio", "cues")})
    for ln in p.stdout:
        if "%|" in ln or "Animation" in ln and "%" in ln:
            continue                       # skip progress bars
        STATE["log"] = (STATE["log"] + ln)[-20000:]
    return p.wait() == 0


def rebuild(scene, voice):
    import pacing
    f = next(fi for fi, sc, _ in pacing.SCENES if sc == scene)
    STATE.update(running=True, log="", scene=scene, ok=None)
    ok = True
    if voice:
        ok = run([PY, "audio/tts.py", "--scene", scene])
    ok = ok and run([MANIM, "-qm", "--disable_caching", f, scene])
    ok = ok and run([PY, "audio/mix.py", "720p30"])
    STATE.update(running=False, ok=ok)
    STATE["log"] += "\nDONE\n" if ok else "\nFAILED (see log above)\n"


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def body(self):
        return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")

    def safe(self, p):
        full = os.path.realpath(os.path.join(ROOT, p))
        if not full.startswith(ROOT + os.sep) or not full.endswith(".py"):
            raise ValueError("only .py files inside the project")
        return full

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            return self.send(200, PAGE, "text/html; charset=utf-8")
        if path == "/api/data":
            mt = os.path.getmtime(VIDEO) if os.path.exists(VIDEO) else 0
            return self.send(200, json.dumps({"scenes": scenes(), "video": mt}))
        if path == "/api/status":
            return self.send(200, json.dumps(STATE))
        if path == "/api/file":
            from urllib.parse import parse_qs
            q = parse_qs(self.path.split("?", 1)[1])
            return self.send(200, json.dumps({"text": open(self.safe(q["path"][0]), encoding="utf8").read()}))
        if path == "/video.mp4":
            return self.video()
        self.send(404, "{}")

    def video(self):
        size = os.path.getsize(VIDEO)
        start, end = 0, size - 1
        rng = self.headers.get("Range")
        if rng:
            m = re.match(r"bytes=(\d*)-(\d*)", rng)
            if m.group(1):
                start = int(m.group(1))
            if m.group(2):
                end = int(m.group(2))
        end = min(end, size - 1)
        self.send_response(206 if rng else 200)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        if rng:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with open(VIDEO, "rb") as fh:
            fh.seek(start)
            left = end - start + 1
            try:
                while left > 0:
                    chunk = fh.read(min(1 << 20, left))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            d = self.body()
            if path == "/api/narration":
                f = os.path.join(ROOT, "narration.json")
                nar = json.load(open(f, encoding="utf8"))
                nar[d["scene"]] = d["items"]
                json.dump(nar, open(f, "w", encoding="utf8"), indent=1, ensure_ascii=False)
                return self.send(200, '{"ok":true}')
            if path == "/api/file":
                open(self.safe(d["path"]), "w", encoding="utf8").write(d["text"])
                return self.send(200, '{"ok":true}')
            if path == "/api/rebuild":
                if STATE["running"]:
                    return self.send(409, '{"error":"a rebuild is already running"}')
                threading.Thread(target=rebuild, args=(d["scene"], bool(d.get("voice"))), daemon=True).start()
                return self.send(200, '{"ok":true}')
        except Exception as e:
            return self.send(400, json.dumps({"error": str(e)}))
        self.send(404, "{}")


PAGE = r"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Determinants Studio</title>
<style>
:root{--bg:#111;--panel:#1b1b1b;--fg:#eee;--soft:#999;--acc:#f2c94c;--line:#2c2c2c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif}
header{padding:10px 16px;border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header b{color:var(--acc)}
main{display:grid;grid-template-columns:220px minmax(0,1fr) minmax(0,460px);height:calc(100vh - 50px)}
#list{overflow:auto;border-right:1px solid var(--line)}
#list div{padding:6px 12px;cursor:pointer;border-bottom:1px solid #191919}
#list div.on{background:#2a2614;color:var(--acc)}
#list small{color:var(--soft)}
#center{padding:12px;overflow:auto}
video{width:100%;background:#000;border-radius:6px}
#ctrl{display:flex;gap:8px;margin:10px 0;flex-wrap:wrap;align-items:center}
button{background:#2a2a2a;color:var(--fg);border:1px solid #3a3a3a;border-radius:6px;padding:6px 12px;cursor:pointer}
button.primary{background:#5a4a12;border-color:#7a6418}
button:disabled{opacity:.5}
#now{font-size:20px;margin:8px 0 4px}#meta{color:var(--soft)}
#side{border-left:1px solid var(--line);display:flex;flex-direction:column;min-height:0}
#tabs{display:flex;border-bottom:1px solid var(--line)}#tabs button{border:0;border-radius:0;flex:1;background:none}
#tabs button.on{border-bottom:2px solid var(--acc);color:var(--acc)}
.pane{flex:1;overflow:auto;padding:10px;display:none}.pane.on{display:block}
.item{display:flex;gap:6px;margin:6px 0;align-items:flex-start}.item .k{color:var(--soft);width:26px;padding-top:6px}
.item textarea{flex:1;min-height:54px;background:#151515;color:var(--fg);border:1px solid #333;border-radius:4px;padding:6px;font:inherit}
.item.cur textarea{border-color:var(--acc)}
.item input{width:70px;background:#151515;color:var(--fg);border:1px solid #333;border-radius:4px;padding:4px}
#code{width:100%;height:calc(100% - 44px);background:#0d0d0d;color:#ddd;border:1px solid #333;font:12.5px/1.4 ui-monospace,monospace;padding:8px;white-space:pre;tab-size:4}
#log{white-space:pre-wrap;font:12px ui-monospace,monospace;color:#bbb;background:#0d0d0d;padding:8px;border-radius:4px;min-height:200px}
label{color:var(--soft)}
@media(max-width:1000px){main{grid-template-columns:1fr;height:auto}#list{max-height:180px}#side{min-height:500px}}
</style></head><body>
<header><b>Determinants Studio</b><span id="pos" style="color:var(--soft)"></span>
<span style="flex:1"></span><span style="color:var(--soft)">← → slides · space play/pause</span></header>
<main>
<div id="list"></div>
<div id="center">
 <video id="v" controls preload="auto"></video>
 <div id="ctrl">
  <button onclick="go(-1)">◀ prev</button><button class="primary" onclick="playSlide()">▶ play slide</button>
  <button onclick="go(1)">next ▶</button>
  <label><input type="checkbox" id="through"> play through (don't stop at slide end)</label>
 </div>
 <div id="now"></div><div id="meta"></div>
</div>
<div id="side">
 <div id="tabs"><button class="on" data-p="nar">Narration</button><button data-p="code">Code</button><button data-p="build">Rebuild</button></div>
 <div class="pane on" id="nar"><div id="items"></div>
  <button onclick="addLine()">+ line</button> <button onclick="addPause()">+ pause</button>
  <button class="primary" onclick="saveNar()">Save narration</button>
  <p style="color:var(--soft)">A number is a pause in seconds. Line numbers match <code>self.cue(k)</code> in the code.
  After changing words, rebuild the scene with "re-record voice" ticked.</p></div>
 <div class="pane" id="code"><div style="display:flex;gap:8px;margin-bottom:6px"><span id="fname" style="color:var(--soft);flex:1"></span>
  <button class="primary" onclick="saveCode()">Save file</button></div><textarea id="codeta" spellcheck="false" style="width:100%;height:calc(100vh - 170px);background:#0d0d0d;color:#ddd;border:1px solid #333;font:12.5px/1.4 ui-monospace,monospace;padding:8px;white-space:pre;tab-size:4"></textarea></div>
 <div class="pane" id="build"><p>Rebuild <b id="bscene"></b>: render the scene, then remix the full video.</p>
  <label><input type="checkbox" id="voice" checked> re-record voice for this scene first</label><br><br>
  <button class="primary" id="bbtn" onclick="rebuild()">Rebuild scene</button>
  <p id="bstat" style="color:var(--soft)"></p><div id="log"></div></div>
</div>
</main>
<script>
let D=null,slides=[],cur=0,stopAt=null;const v=document.getElementById('v');
const $=id=>document.getElementById(id);
document.querySelectorAll('#tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#tabs button,.pane').forEach(x=>x.classList.remove('on'));b.classList.add('on');$(b.dataset.p).classList.add('on');if(b.dataset.p=='code')loadCode()});
async function load(keep){D=await (await fetch('/api/data')).json();slides=[];
 D.scenes.forEach((s,si)=>s.lines.forEach((l,k)=>slides.push({si,k,t0:s.offset+l.start,t1:s.offset+l.end,text:l.text})));
 v.src='/video.mp4?v='+D.video;
 $('list').innerHTML=D.scenes.map((s,i)=>`<div data-i="${i}" onclick="toScene(${i})">${s.name}<br><small>${fmt(s.offset)} · ${s.lines.length} slides</small></div>`).join('');
 show(keep?Math.min(cur,slides.length-1):0,false)}
function fmt(t){return Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0')}
function sc(){return D.scenes[slides[cur].si]}
let lastScene=-1;
function show(i,seek=true){cur=Math.max(0,Math.min(slides.length-1,i));const s=slides[cur],S=D.scenes[s.si];
 $('now').textContent=s.text;$('meta').textContent=`${S.name} · slide ${s.k+1}/${S.lines.length} · ${fmt(s.t0)}`;
 $('pos').textContent=`slide ${cur+1} / ${slides.length}`;
 document.querySelectorAll('#list div').forEach(d=>d.classList.toggle('on',+d.dataset.i==s.si));
 if(s.si!=lastScene){lastScene=s.si;renderItems();$('bscene').textContent=S.name;if($('code').classList.contains('on'))loadCode()}
 document.querySelectorAll('.item[data-k]').forEach(d=>d.classList.toggle('cur',+d.dataset.k==s.k));
 if(seek){v.currentTime=Math.max(0,s.t0-0.15)}}
function toScene(i){show(slides.findIndex(s=>s.si==i))}
function go(d){show(cur+d);playSlide()}
function playSlide(){const s=slides[cur];v.currentTime=Math.max(0,s.t0-0.15);stopAt=$('through').checked?null:(cur+1<slides.length&&slides[cur+1].si==s.si?slides[cur+1].t0-0.2:D.scenes[s.si].offset+D.scenes[s.si].duration-0.05);v.play()}
v.addEventListener('timeupdate',()=>{if(stopAt!==null&&v.currentTime>=stopAt){v.pause();stopAt=null}
 if(!v.paused){const i=slides.findIndex((s,j)=>v.currentTime>=s.t0-0.2&&(j+1==slides.length||v.currentTime<slides[j+1].t0-0.2));if(i>=0&&i!=cur)show(i,false)}});
document.addEventListener('keydown',e=>{if(['TEXTAREA','INPUT'].includes(e.target.tagName))return;
 if(e.key=='ArrowRight'){e.preventDefault();go(1)}else if(e.key=='ArrowLeft'){e.preventDefault();go(-1)}else if(e.key==' '){e.preventDefault();v.paused?playSlide():v.pause()}});
function renderItems(){const S=sc();let k=0;$('items').innerHTML=S.narration.map((x,i)=>{
 if(typeof x=='number')return `<div class="item"><span class="k">⏸</span><input type="number" step="0.1" value="${x}" data-i="${i}"> s <button onclick="delItem(${i})">✕</button></div>`;
 const t=Array.isArray(x)?x[0]:x;const h=`<div class="item" data-k="${k}"><span class="k">${k}</span><textarea data-i="${i}">${t.replace(/</g,'&lt;')}</textarea><button onclick="delItem(${i})">✕</button></div>`;k++;return h}).join('')}
function collect(){const S=sc();return S.narration.map((x,i)=>{const el=document.querySelector(`[data-i="${i}"]`);
 if(!el)return x; if(typeof x=='number')return parseFloat(el.value)||0; return el.value.trim()}).filter(x=>x!==null)}
function delItem(i){const S=sc();S.narration=collect();S.narration.splice(i,1);renderItems()}
function addLine(){const S=sc();S.narration=collect();S.narration.push('New line.');renderItems()}
function addPause(){const S=sc();S.narration=collect();S.narration.push(1.0);renderItems()}
async function saveNar(){const S=sc();S.narration=collect();const r=await fetch('/api/narration',{method:'POST',body:JSON.stringify({scene:S.name,items:S.narration})});
 alert(r.ok?'Saved. Rebuild the scene (with "re-record voice") to hear it.':'Save failed')}
async function loadCode(){const S=sc();$('fname').textContent=S.file+' · class '+S.name+' at line '+S.line;
 const r=await (await fetch('/api/file?path='+encodeURIComponent(S.file))).json();const ta=$('codeta');ta.value=r.text;
 const lh=17.5;setTimeout(()=>{ta.scrollTop=(S.line-3)*lh},50)}
async function saveCode(){const S=sc();const r=await fetch('/api/file',{method:'POST',body:JSON.stringify({path:S.file,text:$('codeta').value})});alert(r.ok?'Saved '+S.file:'Save failed')}
async function rebuild(){const S=sc();const r=await fetch('/api/rebuild',{method:'POST',body:JSON.stringify({scene:S.name,voice:$('voice').checked})});
 if(!r.ok){alert((await r.json()).error);return}$('bbtn').disabled=true;poll()}
async function poll(){const s=await (await fetch('/api/status')).json();$('log').textContent=s.log.slice(-6000);$('log').scrollTop=1e9;
 $('bstat').textContent=s.running?'Running… ('+s.scene+')':(s.ok===null?'':(s.ok?'Done. Video reloaded.':'Failed.'));
 if(s.running)setTimeout(poll,1500);else{$('bbtn').disabled=false;if(s.ok)load(true)}}
load();
</script></body></html>"""


if __name__ == "__main__":
    print(f"Studio on http://localhost:{PORT}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
