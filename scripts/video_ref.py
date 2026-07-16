#!/usr/bin/env python3
"""Build the 16:9 Flow/Veo start-frame reference for a style variant.

The variant art (already on chroma green #00B140) is centered on a
1920x1080 green canvas with generous margins so the tail and any motion
have room, and the frame's aspect exactly matches a 16:9 Flow session —
an aspect mismatch makes Flow crop or rotate the start frame, and any
transform stops it from pinning pixels (the dog gets re-rendered).

Usage: video_ref.py <variant.png> <out.png>
"""
import sys

from PIL import Image

KEY = (0, 177, 64)


def main():
    src = Image.open(sys.argv[1]).convert("RGB")
    canvas = Image.new("RGB", (1920, 1080), KEY)
    scale = 820 / src.size[1]
    r = src.resize((round(src.size[0] * scale), 820), Image.LANCZOS)
    canvas.paste(r, ((1920 - r.size[0]) // 2, 1080 - 120 - r.size[1]))
    canvas.save(sys.argv[2])
    print(f"{sys.argv[2]}: dog {r.size[0]}x{r.size[1]} on 1920x1080")


if __name__ == "__main__":
    main()
