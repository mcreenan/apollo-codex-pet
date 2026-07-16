#!/usr/bin/env python3
"""Turn a generated video (Sora/Veo) of Apollo on chroma green into a
48-frame row of 192x208 cells plus a preview GIF.

Pipeline: decode at --fps -> crop to subject (from frame 0's key) ->
chroma-key every frame (reuses extract_rows' border-connected keying) ->
find the best loop window (the pair of frames ~4s apart that look most
alike, so the wrap seam is invisible) -> resample to --n frames ->
row-stable placement (one scale + offset for the whole row).

Usage: video_rows.py <video> <out_dir> [--fps 12] [--n 48]
       [--target-height 198] [--gif out.gif]
"""
import argparse
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

_here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("extract_rows",
                                              _here / "extract_rows.py")
xr = importlib.util.module_from_spec(spec)
sys.modules["extract_rows"] = xr
spec.loader.exec_module(xr)

CELL_W, CELL_H = 192, 208
BOTTOM_MARGIN = 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out_dir")
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--target-height", type=int, default=198)
    ap.add_argument("--gif", default=None)
    ap.add_argument("--skip", type=float, default=0.0,
                    help="seconds to drop from the clip start (e.g. a "
                         "stand-up transition before a run-in-place loop)")
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-i", args.video,
             "-vf", f"fps={args.fps}", str(tmp / "%04d.png")], check=True)
        paths = sorted(tmp.glob("*.png"))[round(args.skip * args.fps):]
        print(f"{len(paths)} frames @ {args.fps}fps"
              f"{f' (skipped first {args.skip}s)' if args.skip else ''}")

        # subject crop from frame 0's key, padded; then key small
        first = Image.open(paths[0]).convert("RGBA")
        key = xr.detect_key(first)
        print("detected key:", key)
        keyed0 = xr.key_background(first.copy(), key)
        bb = keyed0.getchannel("A").getbbox()
        pad_x = (bb[2] - bb[0]) // 3
        pad_y = (bb[3] - bb[1]) // 6
        crop = (max(0, bb[0] - pad_x), max(0, bb[1] - pad_y),
                min(first.size[0], bb[2] + pad_x),
                min(first.size[1], bb[3] + pad_y))
        scale = 256 / (crop[3] - crop[1])
        size = (round((crop[2] - crop[0]) * scale), 256)

        frames = []
        for p in paths:
            f = Image.open(p).convert("RGBA").crop(crop).resize(
                size, Image.LANCZOS)
            f = xr.key_background(f, key)
            # keep only the dog: drop small disconnected blobs (generator
            # watermarks, sparkle artifacts) that survive keying and would
            # stretch the union bbox
            px = f.load()
            comps = xr._components(*f.size,
                                   lambda x, y: px[x, y][3] >= 16)
            if comps:
                main = max(comps, key=len)
                for comp in comps:
                    if comp is not main and len(comp) < 0.3 * len(main):
                        for x, y in comp:
                            px[x, y] = (0, 0, 0, 0)
            # interior despill: video lighting bounces the key color onto
            # the subject as small bright-green specks; cap any strongly
            # key-dominant channel on opaque pixels
            k = max(range(3), key=lambda i: key[i])
            W2, H2 = f.size
            for y in range(H2):
                for x in range(W2):
                    c = px[x, y]
                    if c[3] < 16:
                        continue
                    others = max(c[i] for i in range(3) if i != k)
                    if c[k] > others + 24:
                        c = list(c)
                        c[k] = others
                        px[x, y] = tuple(c)
            frames.append(f)

        # loop window: frames i and i+L most alike for L near n
        thumbs = [f.resize((48, 64), Image.BILINEAR).tobytes()
                  for f in frames]
        def diff(a, b):
            return sum(abs(x - y) for x, y in zip(thumbs[a], thumbs[b]))
        best = None
        for L in range(args.n - 8, args.n + 9):
            for i in range(0, len(frames) - L):
                d = diff(i, i + L)
                if best is None or d < best[0]:
                    best = (d, i, L)
        _, start, L = best
        print(f"loop window: frames {start}..{start + L} "
              f"(seam diff {best[0] / len(thumbs[0]):.1f})")
        loop = [frames[start + round(j * L / args.n)]
                for j in range(args.n)]

        boxes = [f.getchannel("A").getbbox() for f in loop]
        union = (min(b[0] for b in boxes), min(b[1] for b in boxes),
                 max(b[2] for b in boxes), max(b[3] for b in boxes))
        uw, uh = union[2] - union[0], union[3] - union[1]
        s = min(args.target_height / uh, (CELL_W - 8) / uw)
        sw, sh = round(uw * s), round(uh * s)
        ox, oy = (CELL_W - sw) // 2, CELL_H - BOTTOM_MARGIN - sh

        out = Path(args.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        cells = []
        for i, f in enumerate(loop):
            content = f.crop(union).resize((sw, sh), Image.LANCZOS)
            cell = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
            cell.paste(content, (ox, oy), content)
            cell.save(out / f"{i:02d}.png")
            cells.append(cell)
        print(f"{out}: {args.n} cells, scale {s:.3f}")

        if args.gif:
            gif = []
            for f in cells:
                bg = Image.new("RGBA", f.size, (32, 32, 32, 255))
                bg.paste(f, (0, 0), f)
                gif.append(bg.convert("RGB").resize(
                    (CELL_W * 2, CELL_H * 2), Image.NEAREST))
            gif[0].save(args.gif, save_all=True, append_images=gif[1:],
                        duration=round(1000 / args.fps), loop=0)
            print(f"{args.gif}: preview")


if __name__ == "__main__":
    main()
