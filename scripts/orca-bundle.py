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
       orca-bundle.py --preview <src_pet_dir> [gif_out_dir]
"""
import itertools
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rig  # noqa: E402

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


INTERP_PAD = 32   # gap between the RGB and alpha halves of the interp canvas
INTERP_MATTE = 60  # neutral gray the RGB half is composited onto


def interp_cycle(keyframes, n_frames=COLS):
    """Expand a short keyframe cycle into n_frames optical-flow in-betweens.

    Generated strips only stay on-model for a handful of frames, so high
    frame counts come from interpolation, not generation: ffmpeg's
    minterpolate synthesizes the in-betweens deterministically and cannot
    drift the character. RGB (composited on neutral gray) and alpha ride
    side by side on one canvas so both get identical motion vectors; three
    copies of the cycle are interpolated and the middle one kept, so the
    wrap seam is interpolated like any other neighbor and the loop is
    seamless.
    """
    C = len(keyframes)
    fps, rem = divmod(n_frames, C)
    assert rem == 0, f"cycle length {C} must divide {n_frames}"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "in").mkdir()
        (tmp / "out").mkdir()
        for i in range(3 * C):
            f = keyframes[i % C]
            canvas = Image.new("RGB", (CELL_W * 2 + INTERP_PAD, CELL_H),
                               (INTERP_MATTE,) * 3)
            rgb = Image.new("RGB", (CELL_W, CELL_H), (INTERP_MATTE,) * 3)
            rgb.paste(f, (0, 0), f)
            canvas.paste(rgb, (0, 0))
            canvas.paste(f.getchannel("A").convert("RGB"),
                         (CELL_W + INTERP_PAD, 0))
            canvas.save(tmp / "in" / f"{i:03d}.png")
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-framerate", "1",
             "-i", str(tmp / "in" / "%03d.png"),
             "-vf", f"minterpolate=fps={fps}:mi_mode=mci:mc_mode=aobmc:"
                    "me_mode=bidir:vsbmc=1",
             "-start_number", "0", str(tmp / "out" / "%03d.png")],
            check=True)
        frames = []
        for i in range(n_frames, 2 * n_frames):  # middle cycle only
            canvas = Image.open(tmp / "out" / f"{i:03d}.png").convert("RGB")
            rgb = canvas.crop((0, 0, CELL_W, CELL_H)).load()
            alpha = canvas.crop((CELL_W + INTERP_PAD, 0,
                                 CELL_W * 2 + INTERP_PAD, CELL_H))
            al = alpha.convert("L").load()
            frame = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
            fp = frame.load()
            for y in range(CELL_H):
                for x in range(CELL_W):
                    a = al[x, y]
                    if a < 12:  # kill matte fringe
                        continue
                    r, g, b = rgb[x, y]
                    if a < 255:  # un-composite from the gray matte
                        m = INTERP_MATTE * (255 - a)
                        r = min(255, max(0, round((r * 255 - m) / a)))
                        g = min(255, max(0, round((g * 255 - m) / a)))
                        b = min(255, max(0, round((b * 255 - m) / a)))
                    fp[x, y] = (r, g, b, a)
            frames.append(frame)
    return frames


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


def build_calm_row(cell, row, n_frames=48, smooth=None):
    """Choreographed loop for one played state. All sine terms complete
    integer cycles over n_frames so frame N-1 flows back into frame 0.

    Rotations pivot about the feet, which doubles how far the head travels
    vs a center pivot — amplitudes stay small so sway reads as breathing,
    not a metronome. Calm states hold poses 8 frames to cut pose-snap rate."""
    if smooth:
        # Row was regenerated as a continuous in-between loop with frames
        # already feet-registered to each other, so frames get ONE shared
        # anchor for the whole row. Per-frame bbox anchoring would re-shift
        # frames whenever the lowest pixel moves (a wagging tail) and undo
        # the registration.
        #   {"rig": {...}, "master": c}  procedural rig: ONE master cell
        #                           deformed into n_frames (scripts/rig.py)
        #   {"cycle": [...]}        keyframe cells in loop order, expanded to
        #                           n_frames by optical-flow interpolation
        #   {"track": [...], "hold": h}  literal playback, track*hold frames
        if "rig" in smooth:
            # rig in raw sheet coords (programs are measured there), then
            # place() each frame identically: deformations keep the bbox
            # bottom static, so per-frame anchoring cannot re-shift frames
            master = cell(row, smooth.get("master", 0))
            return [place(f) for f in rig.render(master, smooth["rig"],
                                                 n_frames)]
        if "cycle" in smooth:
            track = smooth["cycle"]
        else:
            track = [p for p in smooth["track"] for _ in range(smooth["hold"])]
            assert len(track) == n_frames, (row, len(track))
        w = round(CELL_W * BAKED_SCALE)
        h = round(CELL_H * BAKED_SCALE)
        imgs = {p: cell(row, p).resize((w, h), Image.LANCZOS)
                for p in set(track)}
        row_bottom = max(i.getchannel("A").getbbox()[3] for i in imgs.values())
        dy = BASELINE_Y - row_bottom
        frames = []
        for p in track:
            frame = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
            frame.paste(imgs[p], ((CELL_W - w) // 2, dy), imgs[p])
            frames.append(frame)
        if "cycle" in smooth:
            frames = interp_cycle(frames, n_frames)
            # Pose-to-pose retiming: uniform interpolation output means every
            # frame is mid-warp, which reads as morphing, not animation. Rest
            # on each keyframe and spend only a few eased frames traveling.
            seg = n_frames // len(track)
            trans = smooth.get("transition", max(2, seg // 3))
            retimed = []
            for s in range(len(track)):
                retimed.extend([frames[s * seg]] * (seg - trans))
                for j in range(1, trans + 1):
                    t = j / (trans + 1)
                    e = t * t * (3 - 2 * t)  # smoothstep ease in/out
                    retimed.append(frames[s * seg + min(seg - 1, round(e * seg))])
            frames = retimed
        return frames
    # Every other played state gets the calm treatment: smoothest pose order
    # and long holds. Its poses are never in-betweens, so frequent snaps
    # read as glitching in any state; energy comes from transforms instead.
    order = similarity_cycle([cell(row, p) for p in range(SRC_POSES[row])])
    hold, rem = divmod(n_frames, len(order))
    track = [p for i, p in enumerate(order) for _ in range(hold + (i < rem))]
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
            rot = 1.2 * math.sin(8 * math.pi * t)                        # happy wag
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


def load_smooth(src):
    smooth_path = src / "smooth-rows.json"
    if not smooth_path.exists():
        return {}
    return {k: v for k, v in json.loads(smooth_path.read_text()).items()
            if not k.startswith("_")}


def preview(src_dir, out_dir):
    """Render the four played states exactly as Orca will play them —
    including interpolation — as 2x GIFs, without building a bundle.
    Pipeline gate: eyeball these before orca-bundle.py <src> <dst>."""
    src, out = Path(src_dir), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cell = load_cells(src / "spritesheet.webp")
    smooth = load_smooth(src)
    for row in ("idle", "wait", "work", "review"):
        frames = build_calm_row(cell, row, smooth=smooth.get(row))
        gif = []
        for f in frames:
            bg = Image.new("RGBA", f.size, (32, 32, 32, 255))
            bg.paste(f, (0, 0), f)
            gif.append(bg.convert("RGB").resize(
                (f.size[0] * 2, f.size[1] * 2), Image.NEAREST))
        gif[0].save(out / f"{row}.gif", save_all=True, append_images=gif[1:],
                    duration=round(1000 / FPS), loop=0)
        print(f"{out / (row + '.gif')}: {len(frames)} frames @ {FPS}fps")


def build(src_dir, dst_dir):
    src, dst = Path(src_dir), Path(dst_dir)
    cell = load_cells(src / "spritesheet.webp")
    smooth = load_smooth(src)

    rows = {}  # orca row index -> list of frames
    rows[0] = build_calm_row(cell, "idle", smooth=smooth.get("idle"))
    rows[1] = [place(cell("rr", c)) for c in range(8)]
    rows[2] = [place(cell("rl", c)) for c in range(8)]
    rows[3] = [place(cell("wave", c)) for c in [0, 1, 2, 3, 3, 2, 1, 0]]
    rows[4] = [place(cell("jump", 2))]          # frozen drag pose
    rows[5] = [place(cell("failed", c)) for c in range(8)]
    rows[6] = build_calm_row(cell, "wait", smooth=smooth.get("wait"))
    rows[7] = build_calm_row(cell, "work", smooth=smooth.get("work"))
    rows[8] = build_calm_row(cell, "review", smooth=smooth.get("review"))

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
    if sys.argv[1] == "--preview":
        preview(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "qa/preview")
    else:
        build(sys.argv[1], sys.argv[2])
