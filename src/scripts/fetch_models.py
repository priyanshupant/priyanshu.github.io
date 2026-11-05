"""Download the Kokoro voice model (about 90 MB) into audio/models/ if it is missing.
   python scripts/fetch_models.py"""
import os, sys, urllib.request
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "audio", "models")
BASE = "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main/"
os.makedirs(D, exist_ok=True)

def get(rel, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return
    print("downloading", rel, flush=True)
    urllib.request.urlretrieve(BASE + rel, dest + ".part")
    os.replace(dest + ".part", dest)

get("onnx/model_quantized.onnx", os.path.join(D, "model_quantized.onnx"))
voices = {}
for v in ["af_heart"]:
    f = os.path.join(D, v + ".bin")
    get(f"voices/{v}.bin", f)
    voices[v] = np.fromfile(f, dtype=np.float32).reshape(-1, 1, 256)
np.savez(os.path.join(D, "voices.npz"), **voices)
print("models ready in", D)
