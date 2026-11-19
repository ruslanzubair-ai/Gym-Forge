#!/usr/bin/env python3
"""Build index.html: the Gym Forge page with the exercise library and demo images embedded.

Needs: Python 3.9+, Pillow (pip install pillow), internet.
Data: https://github.com/yuhonas/free-exercise-db (check its license terms).
"""
import base64, concurrent.futures as cf, io, json, os, sys, time, urllib.parse, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, ".cache")
DB_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
IMG_BASE = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
MAX_SIDE, QUALITY = 220, 55

def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ai-gym-planner-build"})
            return urllib.request.urlopen(req, timeout=40).read()
        except Exception:
            if i == tries - 1: raise
            time.sleep(1.5)

def image(args):
    ex, i, path = args
    out = os.path.join(CACHE, f"{ex['id']}_{i}.webp")
    if not os.path.exists(out):
        im = Image.open(io.BytesIO(get(IMG_BASE + urllib.parse.quote(path)))).convert("RGB")
        s = MAX_SIDE / max(im.size)
        if s < 1:
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        im.save(out, "WEBP", quality=QUALITY, method=6)
    return ex["id"], i, out

def main():
    os.makedirs(CACHE, exist_ok=True)
    marker = os.path.join(CACHE, "params.txt")
    want = f"{MAX_SIDE}-{QUALITY}-v2"
    if not os.path.exists(marker) or open(marker).read() != want:  # drop images made with other settings
        for f in os.listdir(CACHE):
            if f.endswith(".webp"): os.remove(os.path.join(CACHE, f))
        open(marker, "w").write(want)
    dbf = os.path.join(CACHE, "exercises.json")
    if not os.path.exists(dbf):
        open(dbf, "wb").write(get(DB_URL))
    db = json.load(open(dbf, encoding="utf-8"))
    pool = [e for e in db if e.get("category") in ("strength", "powerlifting") and e.get("images")]
    print(f"{len(pool)} exercises")

    jobs = [(e, i, p) for e in pool for i, p in enumerate(e["images"][:2])]
    imgs = {}
    with cf.ThreadPoolExecutor(24) as ex:
        for eid, i, out in ex.map(image, jobs):
            imgs.setdefault(eid, {})[i] = base64.b64encode(open(out, "rb").read()).decode()
    imgs = {k: [v[i] for i in sorted(v)] for k, v in imgs.items()}

    lib = [{"id": e["id"], "n": e["name"], "l": e.get("level") or "beginner", "q": e.get("equipment") or "",
            "c": {"compound": "c", "isolation": "i"}.get(e.get("mechanic") or "", ""),
            "p": e.get("primaryMuscles") or [],
            "s": [s.strip() for s in (e.get("instructions") or [])[:8]]} for e in pool]

    def js(o):  # safe inside <script type="application/json">
        return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    tpl = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
    html = tpl.replace("__LIB__", js(lib)).replace("__IMGS__", js(imgs))
    out = os.path.join(ROOT, "index.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"wrote {out} ({os.path.getsize(out)/1e6:.1f} MB)")

if __name__ == "__main__":
    sys.exit(main())
