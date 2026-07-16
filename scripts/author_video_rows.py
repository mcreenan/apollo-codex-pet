#!/usr/bin/env python3
"""Author video-derived state loops into a style's pet + bundle.

For each state whose cells exist under runs/<style>-video/cells/<state>/,
this points smooth-rows.json at the 48-frame directory (frames mode),
writes 6 evenly-spaced loop samples into the native sheet row (so the
codex CLI pet animates too), renders exact-playback preview GIFs, and
rebuilds the Orca bundle.

Usage: author_video_rows.py <style> [--no-build]
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

from PIL import Image

CELL_W, CELL_H = 192, 208
STATES = {"idle": ("idle", 0), "waiting": ("wait", 6),
          "running": ("work", 7), "review": ("review", 8)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("style")
    ap.add_argument("--no-build", action="store_true")
    args = ap.parse_args()

    pet = Path(f"dist/codex-pets/apollo-{args.style}")
    cells_root = Path(f"runs/{args.style}-video/cells")
    manifest_path = pet / "smooth-rows.json"
    manifest = (json.loads(manifest_path.read_text())
                if manifest_path.exists() else {})
    sheet = Image.open(pet / "spritesheet.webp").convert("RGBA")

    done = []
    for state, (key, row) in STATES.items():
        d = cells_root / state
        frames = sorted(d.glob("*.png"))
        if len(frames) != 48:
            print(f"{state}: {len(frames)} cells — skipped")
            continue
        manifest[key] = {"frames": str(d)}
        for c, fi in enumerate(range(0, 48, 8)):
            cell = Image.open(d / f"{fi:02d}.png")
            sheet.paste(Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0)),
                        (c * CELL_W, row * CELL_H))
            sheet.paste(cell, (c * CELL_W, row * CELL_H))
        done.append(state)

    if not done:
        sys.exit("no complete cell directories found")
    sheet.save(pet / "spritesheet.webp", lossless=True, exact=True,
               method=4)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"authored: {', '.join(done)}")

    spec = importlib.util.spec_from_file_location(
        "ob", Path(__file__).resolve().parent / "orca-bundle.py")
    ob = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ob)
    ob.preview(pet, f"qa/previews-{args.style}-video")
    if not args.no_build:
        ob.build(pet, f"dist/codex-pet-bundles/Apollo-{args.style}.codex-pet")


if __name__ == "__main__":
    main()
