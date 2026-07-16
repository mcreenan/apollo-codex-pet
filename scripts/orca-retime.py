#!/usr/bin/env python3
"""Rebuild a hatch-pet spritesheet for Orca playback (v2).

Orca plays one global fps with uniform frame stepping, only ever shows the
idle/running/waiting/review rows (plus a frozen `jumping` row while the pet
is dragged), and has no per-frame timing. This rebuild targets that reality:

- fps 6 with each pose held for 2 cells -> ~3 pose changes/sec, calm pacing
- calm rows (idle, waiting, running=work, review) play a ping-pong loop over
  their first 3 frames only: subtle, smooth, no jump-cuts
- directional running rows keep their gait cycle via 4 held key frames
- the jumping row becomes a single held mid-air pose so the frozen
  drag state always shows something intentional

Usage: orca-retime.py <src_pet_dir> <dst_bundle_dir> [installed_dir]
  src_pet_dir: contains pet.json + spritesheet.webp (hatch-pet package)
  dst_bundle_dir: Orca .codex-pet bundle dir to write (created/overwritten)
  installed_dir: optional Orca sidekicks/custom/<uuid> dir to patch in place
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image

CELL_W, CELL_H = 192, 208
COLS, ROWS = 8, 9
FPS = 6

PINGPONG = [0, 0, 1, 1, 2, 2, 1, 1]        # calm rows: subtle 0-1-2-1 loop
GAIT = [0, 0, 2, 2, 4, 4, 6, 6]            # cyclic runs: 4 held key frames
HELD_JUMP = [2] * 8                        # drag state: one mid-air pose

ROW_PLANS = {
    0: ("idle", PINGPONG, 8),
    1: ("running-right", GAIT, 8),
    2: ("running-left", GAIT, 8),
    3: ("waving", [0, 0, 1, 1, 2, 2, 3, 3], 8),
    4: ("jumping", HELD_JUMP, 1),
    5: ("failed", GAIT, 8),
    6: ("waiting", PINGPONG, 8),
    7: ("running", PINGPONG, 8),
    8: ("review", PINGPONG, 8),
}


def build(src_dir: str, dst_dir: str, installed_dir: str | None) -> None:
    src, dst = Path(src_dir), Path(dst_dir)
    sheet = Image.open(src / "spritesheet.webp").convert("RGBA")
    if sheet.size != (COLS * CELL_W, ROWS * CELL_H):
        raise SystemExit(f"unexpected sheet size {sheet.size}")

    out = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    animations = {}
    for row, (name, plan, frames) in ROW_PLANS.items():
        y = row * CELL_H
        for dst_col, src_col in enumerate(plan):
            cell = sheet.crop(
                (src_col * CELL_W, y, (src_col + 1) * CELL_W, y + CELL_H)
            )
            out.paste(cell, (dst_col * CELL_W, y))
        animations[name] = {"row": row, "frames": frames}

    manifest = json.loads((src / "pet.json").read_text())
    manifest.update(
        {
            "spritesheetPath": "spritesheet.webp",
            "frame": {"width": CELL_W, "height": CELL_H},
            "fps": FPS,
            "defaultAnimation": "idle",
            "animations": animations,
        }
    )
    manifest_text = json.dumps(manifest, indent=2) + "\n"

    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    # exact=True stops libwebp rewriting RGB under transparent pixels
    out.save(dst / "spritesheet.webp", lossless=True, exact=True)
    (dst / "pet.json").write_text(manifest_text)
    print(f"wrote {dst}")

    if installed_dir:
        inst = Path(installed_dir)
        installed = json.loads((inst / "pet.json").read_text())
        installed.update(manifest)
        shutil.copyfile(dst / "spritesheet.webp", inst / "spritesheet.webp")
        (inst / "pet.json").write_text(json.dumps(installed, indent=2) + "\n")
        print(f"patched {inst}")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
