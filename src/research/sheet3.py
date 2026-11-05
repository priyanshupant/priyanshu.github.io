import subprocess, sys
from PIL import Image, ImageDraw
out=sys.argv[1]; fracs=[float(x) for x in sys.argv[2].split(",")]; specs=sys.argv[3:]
rows=[]
for spec in specs:
    f, sc = spec.split(":")
    v=f"media/videos/{f}/480p15/{sc}.mp4"
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",v]))
    ims=[]
    for x in fracs:
        p=f"/tmp/fr_{sc}_{x}.png"
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(min(d*x,d-0.1)),"-i",v,"-frames:v","1",p],check=True)
        ims.append(Image.open(p).resize((512,288)))
    rows.append((sc,ims))
n=len(fracs); s=Image.new("RGB",(512*min(n,3),308*len(rows)*((n+2)//3)),(40,40,40)); dr=ImageDraw.Draw(s)
y=0
for sc,ims in rows:
    for k,im in enumerate(ims):
        if k%3==0 and k: y+=308
        if k==0: dr.text((6,y+3),sc,fill=(255,255,0))
        s.paste(im,((k%3)*512,y+20))
    y+=308
s.crop((0,0,s.width,y)).save(out)
