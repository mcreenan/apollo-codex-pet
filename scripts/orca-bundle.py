#!/usr/bin/env python3
"""Build Orca .codex-pet bundles: wide 48-column sheets at 12fps.

Orca plays one flat fps over each animation row (steps(), no per-frame
timing) and only ever shows idle / running(work) / waiting / review, plus a
frozen `jumping` frame while dragging. We use the schema headroom
(frames <= columns, fps <= 60) to give each played state a 4-second
choreographed loop: designed pose cycles held 4 frames each, with eased
transforms (breathing squash, sway, bobs, hops) gliding on every frame.

All frames are synthesized from the 57 existing poses. A uniform 0.95
content scale buys ~15px vertical headroom inside the 192x208 cell so
transforms never clip (source sprites only have 5px top margin).

Usage: orca-bundle.py <src_pet_dir> <dst_bundle_dir>
"""
import itertools
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
BASELINE_Y = CELL_H - 6  # content bbox bottom sits here in every frame

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
    """Transform a full source cell, feet planted on a common baseline.

    Vertically the content alpha-bbox bottom lands on BASELINE_Y (cell-edge
    padding varies per pose, so pasting by cell would float). Horizontally
    poses stay as drawn — bbox re-centering would shift the whole body
    whenever a lifted paw or tail moves the bbox. Rotation pivots about the
    bottom-center foot anchor so sway/wag never lifts the feet.
    """
    w = max(1, round(CELL_W * sx * BAKED_SCALE))
    h = max(1, round(CELL_H * sy * BAKED_SCALE))
    img = cell.resize((w, h), Image.LANCZOS)
    # bbox from alpha only: sources keep RGB junk under transparent pixels
    bottom = (img.getchannel("A").getbbox() or (0, 0, w, h))[3]
    anchor_x = CELL_W / 2 + dx
    anchor_y = BASELINE_Y + dy
    frame = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
    frame.paste(img, (round((CELL_W - w) / 2 + dx),
                      round(anchor_y - bottom)), img)
    if rot:
        frame = frame.rotate(rot, resample=Image.BICUBIC,
                             center=(anchor_x, anchor_y))
    return frame


def pose_track(n_poses, hold=4, cycles=2, order=None):
    """Designed pose loop, each pose held `hold` frames, repeated `cycles`x."""
    order = order if order is not None else range(n_poses)
    return [p for _ in range(cycles) for p in order for _ in range(hold)]


def similarity_cycle(cells, k_min=4):
    """Cyclic pose order minimizing the WORST visual snap between neighbors.

    Source pose rows are distinct drawings, not in-betweens, so playing them
    in sheet order can jump between very different poses. Brute-forces cycles
    on downscaled thumbnails (n is small), and may drop outlier poses — a
    pose that transitions smoothly to nothing doesn't belong in a calm loop
    (kept only if dropping it doesn't clearly help)."""
    thumbs = []
    for c in cells:
        t = c.resize((48, 52), Image.BILINEAR)
        thumbs.append(list(t.convert("RGBA").tobytes()))
    n = len(cells)
    d = {}
    for a in range(n):
        for b in range(a + 1, n):
            d[a, b] = sum(abs(x - y) for x, y in zip(thumbs[a], thumbs[b]))
    def edge(a, b):
        return d[min(a, b), max(a, b)]
    def best_cycle(subset):
        first, rest = subset[0], subset[1:]
        best = None
        for p in itertools.permutations(rest):
            cyc = (first,) + p
            edges = [edge(cyc[i], cyc[(i + 1) % len(cyc)]) for i in range(len(cyc))]
            key = (max(edges), sum(edges))
            if best is None or key < best[0]:
                best = (key, list(cyc))
        return best
    (worst, _), order = best_cycle(tuple(range(n)))
    for k in range(n - 1, k_min - 1, -1):
        cand = min((best_cycle(s) for s in itertools.combinations(range(n), k)),
                   key=lambda c: c[0])
        if cand[0][0] < 0.8 * worst:  # drop poses only for a clear win
            (worst, _), order = cand
    return order


def build_calm_row(cell, row, n_frames=48):
    """Choreographed loop for one played state. All sine terms complete
    integer cycles over n_frames so frame N-1 flows back into frame 0.

    Rotations pivot about the feet, which doubles how far the head travels
    vs a center pivot — amplitudes stay small so sway reads as breathing,
    not a metronome. Calm states hold poses 8 frames to cut pose-snap rate."""
    n_poses = SRC_POSES[row]
    if row in ("idle", "wait"):  # calm states: fewer snaps, smoothest order
        order = similarity_cycle([cell(row, p) for p in range(n_poses)])
        hold, rem = divmod(n_frames, len(order))
        track = [p for i, p in enumerate(order) for _ in range(hold + (i < rem))]
    else:  # work is a gait, review is energetic: keep the authored order
        track = pose_track(n_poses, hold=4, cycles=2)
    frames = []
    for i in range(n_frames):
        t = i / n_frames
        dx = dy = rot = 0.0
        sx = sy = 1.0
        if row == "idle":
            sy = 1.0 - 0.020 * (0.5 - 0.5 * math.cos(8 * math.pi * t))  # 4 breaths
            sx = 2.0 - sy  # conserve volume
            rot = 0.8 * math.sin(4 * math.pi * t)                        # slow sway
        elif row == "work":
            dy = -4.0 * abs(math.sin(8 * math.pi * t))                   # busy trot bob
            dx = 2.5 * math.sin(4 * math.pi * t)
        elif row == "wait":
            rot = 1.2 * math.sin(4 * math.pi * t)                        # expectant tilt
            sy = 1.0 - 0.015 * (0.5 - 0.5 * math.cos(8 * math.pi * t))
        elif row == "review":
            rot = 2.5 * math.sin(8 * math.pi * t)                        # happy wag
            for start in (8, 32):                                        # two mini-hops
                if start <= i < start + 6:
                    ht = (i - start) / 5
                    # hop + stretch + wag must fit the 10px top headroom of
                    # the tightest styles; wag eases out so the leap is upright
                    dy = -6.0 * math.sin(math.pi * ht)
                    sy = 1.0 + 0.015 * math.sin(math.pi * ht)
                    rot *= 1.0 - math.sin(math.pi * ht)
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
        "id": src_manifest["id"],
        "displayName": src_manifest.get("displayName", src_manifest["id"]),
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
