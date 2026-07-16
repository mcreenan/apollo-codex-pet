#!/usr/bin/env python3
"""Procedural rig: animate ONE master drawing into a seamless 48-frame loop.

Interpolating between generated keyframes morphs (optical flow warps in 2D
while the drawings articulate in 3D) and generating many frames drifts
off-model. Rigging sidesteps both: every frame is derived from a single
master cell by small deterministic deformations, so identity drift and
morphing are impossible by construction and feet stay planted because the
deformation is zero at ground level.

Deformations:
- sway: horizontal shear that fades in with height above the ground —
  the body leans gently, hinged at the feet
- breath: vertical lift that fades in with height — chest/head rise a
  couple of pixels and settle
- tail wag: a feather-masked tail layer rotated a few degrees about the
  tail base
All bands move sub-pixel per frame via a bicubic mesh warp; every sine
completes integer cycles over the loop so frame 47 flows into frame 0.

Usage: rig.py <master_cell.png|sheet.webp:row:col> <out_dir> [--gif out.gif]
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

CELL_W, CELL_H = 192, 208
N_FRAMES = 48
FPS = 12
GROUND_Y = 188   # deformation is zero at/below this line (feet planted)


def band_warp(img, dx_of_y, dy_of_y, band=4):
    """Smooth whole-canvas warp: each horizontal band's source quad is
    offset by (dx(y), dy(y)) at its top and bottom edge; bicubic sampling
    gives sub-pixel motion with no seams."""
    W, H = img.size
    mesh = []
    for y0 in range(0, H, band):
        y1 = min(H, y0 + band)
        mesh.append(((0, y0, W, y1),
                     (-dx_of_y(y0), y0 - dy_of_y(y0),
                      -dx_of_y(y1), y1 - dy_of_y(y1),
                      W - dx_of_y(y1), y1 - dy_of_y(y1),
                      W - dx_of_y(y0), y0 - dy_of_y(y0))))
    return img.transform((W, H), Image.MESH, mesh, resample=Image.BICUBIC)


def rotate_layer(img, theta, ellipse, pivot, feather=5):
    """Rotate a feather-masked region (tail, raised paw) about a pivot."""
    if not theta:
        return img
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse(tuple(ellipse), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    layer = img.copy()
    layer.putalpha(ImageChops.multiply(img.getchannel("A"), mask))
    # composite over the UNCUT original: cutting a feathered hole makes the
    # whole feather ring translucent wherever the mask sits over opaque
    # body. Small rotations cover their own trailing edge, so the static
    # copy underneath stays hidden.
    out = img.copy()
    out.alpha_composite(layer.rotate(theta, resample=Image.BICUBIC,
                                     center=tuple(pivot)))
    return out


# Default clay-idle program; real programs live in each pet's
# smooth-rows.json as {"rig": {...}}. Amplitudes in px (sway/breath) or
# degrees (layers); freq = cycles per loop (integer, for a seamless wrap).
IDLE = {
    "sway": {"amp": 1.6, "freq": 1},
    "breath": {"amp": 1.6, "freq": 2},
    "layers": [{"amp": 3.0, "freq": 2, "phase": 0.9,
                "ellipse": (34, 136, 82, 196), "pivot": (76, 166)}],
}


def render(master, prog, n_frames=N_FRAMES):
    frames = []
    for i in range(n_frames):
        t = i / n_frames
        sway = prog.get("sway", {"amp": 0, "freq": 1})
        breath = prog.get("breath", {"amp": 0, "freq": 1})
        s = sway["amp"] * math.sin(2 * math.pi * sway["freq"] * t)
        b = breath["amp"] * (0.5 - 0.5 * math.cos(
            2 * math.pi * breath["freq"] * t))

        def w(y):  # sway weight: 1 at head, 0 at ground
            return max(0.0, (GROUND_Y - y) / (GROUND_Y - 5)) ** 1.3

        def v(y):  # breath weight
            return max(0.0, (GROUND_Y + 7 - y) / (GROUND_Y - 5))

        img = master
        for lay in prog.get("layers", []):
            theta = lay["amp"] * math.sin(
                2 * math.pi * lay["freq"] * t + lay.get("phase", 0.0))
            img = rotate_layer(img, theta, lay["ellipse"], lay["pivot"],
                               feather=lay.get("feather", 5))
        img = band_warp(img, lambda y: s * w(y), lambda y: -b * v(y))
        frames.append(img)
    return frames


def main():
    src, out_dir = sys.argv[1], Path(sys.argv[2])
    if ":" in src:
        path, row, col = src.rsplit(":", 2)
        sheet = Image.open(path).convert("RGBA")
        master = sheet.crop((int(col) * CELL_W, int(row) * CELL_H,
                             (int(col) + 1) * CELL_W,
                             (int(row) + 1) * CELL_H))
    else:
        master = Image.open(src).convert("RGBA")
    frames = render(master, IDLE)
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(frames):
        f.save(out_dir / f"{i:02d}.png")
    if "--gif" in sys.argv:
        gif_path = sys.argv[sys.argv.index("--gif") + 1]
        gif = []
        for f in frames:
            bg = Image.new("RGBA", f.size, (32, 32, 32, 255))
            bg.paste(f, (0, 0), f)
            gif.append(bg.convert("RGB").resize(
                (f.size[0] * 2, f.size[1] * 2), Image.NEAREST))
        gif[0].save(gif_path, save_all=True, append_images=gif[1:],
                    duration=round(1000 / FPS), loop=0)
        print(f"{gif_path}: {len(frames)} frames @ {FPS}fps")


if __name__ == "__main__":
    main()
