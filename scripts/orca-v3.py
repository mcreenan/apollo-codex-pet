#!/usr/bin/env python3
"""Build v3 Orca .codex-pet bundles: wide 48-column sheets at 12fps.

Orca plays one flat fps over each animation row (steps(), no per-frame
timing) and only ever shows idle / running(work) / waiting / review, plus a
frozen `jumping` frame while dragging. v3 uses the schema headroom
(frames <= columns, fps <= 60) to give each played state a 4-second
choreographed loop: designed pose cycles held 4 frames each, with eased
transforms (breathing squash, sway, bobs, hops) gliding on every frame.

All frames are synthesized from the 57 existing poses. A uniform 0.95
content scale buys ~15px vertical headroom inside the 192x208 cell so
transforms never clip (source sprites only have 5px top margin).

Usage: orca-v3.py <src_pet_dir> <dst_bundle_dir>
"""
import json
import math
import shutil
import sys
from pathlib import Path

from PIL import Image

CELL_W, CELL_H = 192, 208
COLS = 48
FPS = 12
BAKED_SCALE = 0.95

SRC_ROWS = {"idle": 0, "rr": 1, "rl": 2, "wave": 3, "jump": 4,
            "failed": 5, "wait": 6, "work": 7, "review": 8}
SRC_POSES = {"idle": 6, "rr": 8, "rl": 8, "wave": 4, "jump": 5,
             "failed": 8, "wait": 6, "work": 6, "review": 6}


def load_cells(sheet_path):
    sheet = Image.open(sheet_path).convert("RGBA")
    return lambda row, col: sheet.crop(
        (col * CELL_W, SRC_ROWS[row] * CELL_H,
         (col + 1) * CELL_W, SRC_ROWS[row] * CELL_H + CELL_H))


def place(cell, dx=0.0, dy=0.0, rot=0.0, sx=1.0, sy=1.0):
    """Transform a full source cell, anchored bottom-center (feet planted)."""
    w = max(1, round(CELL_W * sx * BAKED_SCALE))
    h = max(1, round(CELL_H * sy * BAKED_SCALE))
    img = cell.resize((w, h), Image.LANCZOS)
    if rot:
        img = img.rotate(rot, resample=Image.BICUBIC, expand=False)
    frame = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    frame.paste(img, ((CELL_W - w) // 2 + round(dx), CELL_H - h + round(dy)), img)
    return frame


def pose_track(n_poses, hold=4, cycles=2):
    """Designed pose loop, each pose held `hold` frames, repeated `cycles`x."""
    return [p for _ in range(cycles) for p in range(n_poses) for _ in range(hold)]


def build_calm_row(cell, row, n_frames=48):
    """Choreographed loop for one played state. All sine terms complete
    integer cycles over n_frames so frame N-1 flows back into frame 0."""
    track = pose_track(SRC_POSES[row])
    frames = []
    for i in range(n_frames):
        t = i / n_frames
        dx = dy = rot = 0.0
        sx = sy = 1.0
        if row == "idle":
            sy = 1.0 - 0.020 * (0.5 - 0.5 * math.cos(8 * math.pi * t))  # 4 breaths
            sx = 2.0 - sy  # conserve volume
            rot = 1.5 * math.sin(4 * math.pi * t)                        # slow sway
        elif row == "work":
            dy = -4.0 * abs(math.sin(8 * math.pi * t))                   # busy trot bob
            dx = 2.5 * math.sin(4 * math.pi * t)
        elif row == "wait":
            rot = 3.0 * math.sin(4 * math.pi * t)                        # expectant tilt
            sy = 1.0 - 0.015 * (0.5 - 0.5 * math.cos(8 * math.pi * t))
        elif row == "review":
            rot = 5.0 * math.sin(8 * math.pi * t)                        # happy wag
            for start in (8, 32):                                        # two mini-hops
                if start <= i < start + 6:
                    ht = (i - start) / 5
                    dy = -10.0 * math.sin(math.pi * ht)
                    sy = 1.0 + 0.03 * math.sin(math.pi * ht)
        frames.append(place(cell(row, track[i]), dx=dx, dy=dy, rot=rot, sx=sx, sy=sy))
    return frames


def build(src_dir, dst_dir):
    src, dst = Path(src_dir), Path(dst_dir)
    cell = load_cells(src / "spritesheet.webp")

    rows = {}  # orca row index -> list of frames
    rows[0] = build_calm_row(cell, "idle")
    rows[1] = [place(cell("rr", c)) for c in range(8)]
    rows[2] = [place(cell("rl", c)) for c in range(8)]
    rows[3] = [place(cell("wave", c)) for c in [0, 1, 2, 3, 3, 2, 1, 0]]
    rows[4] = [place(cell("jump", 2))]          # frozen drag pose
    rows[5] = [place(cell("failed", c)) for c in range(8)]
    rows[6] = build_calm_row(cell, "wait")
    rows[7] = build_calm_row(cell, "work")
    rows[8] = build_calm_row(cell, "review")

    names = {0: "idle", 1: "running-right", 2: "running-left", 3: "waving",
             4: "jumping", 5: "failed", 6: "waiting", 7: "running", 8: "review"}

    out = Image.new("RGBA", (COLS * CELL_W, 9 * CELL_H), (0, 0, 0, 0))
    animations = {}
    for r, frames in rows.items():
        for c, frame in enumerate(frames):
            out.paste(frame, (c * CELL_W, r * CELL_H))
        animations[names[r]] = {"row": r, "frames": len(frames)}

    src_manifest = json.loads((src / "pet.json").read_text())
    manifest = {
        "id": f"{src_manifest['id']}-v3",
        "displayName": f"{src_manifest.get('displayName', src_manifest['id'])} v3",
        "description": src_manifest.get("description", ""),
        "spritesheetPath": "spritesheet.webp",
        "frame": {"width": CELL_W, "height": CELL_H},
        "fps": FPS,
        "defaultAnimation": "idle",
        "animations": animations,
    }

    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    out.save(dst / "spritesheet.webp", lossless=True, exact=True, method=4)
    (dst / "pet.json").write_text(json.dumps(manifest, indent=2) + "\n")
    size_mb = (dst / "spritesheet.webp").stat().st_size / 1e6
    print(f"{dst.name}: {out.size[0]}x{out.size[1]}, {size_mb:.1f}MB")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
