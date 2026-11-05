"""Narration per scene, stored in narration.json (edit there, or in the studio).
Each entry is a spoken line (str, or [spoken, caption]) or a number: a pause in seconds.
Line k (counting strings only) lines up with self.cue(k) in the scene."""
import json as _json
import os as _os

NARRATION = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "narration.json"), encoding="utf8"))
