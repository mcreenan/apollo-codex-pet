#!/usr/bin/env python3
"""Extract smooth-row strips into 192x208 cells, keying only the background.

Replaces hatch-pet's global chroma keying for our regenerated rows: that
keys ANY pixel near the chroma color, which ate interior pixels (eyes, nose)
on clay. Here the key flood-fills from the slot border, so only background
connected to the outside goes transparent; a light despill removes green
cast on the resulting edge band.

Placement is row-stable: one scale and one offset per row (from the union
of all slots' content), so per-frame extraction can't re-center the body
and reintroduce wobble. Scale targets a reference content height so the pet
stays the same size as the row it replaces.

Usage: extract_rows.py <strip.png> <n_frames> <out_dir> [--target-height H]
"""
import argparse
from pathlib import Path

from PIL import Image

CELL_W, CELL_H = 192, 208
KEY = (0, 177, 64)
THRESHOLD = 96.0
BOTTOM_MARGIN = 5


PURE_THRESHOLD = 48.0  # enclosed pockets must be near-pure chroma to key


def _components(W, H, member):
    """Connected components (4-neighborhood) over pixels where member(x,y)."""
    seen = bytearray(W * H)
    comps = []
    for sy in range(H):
        for sx in range(W):
            if seen[sy * W + sx] or not member(sx, sy):
                continue
            comp = []
            stack = [(sx, sy)]
            seen[sy * W + sx] = 1
            while stack:
                x, y = stack.pop()
                comp.append((x, y))
                for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                    if 0 <= nx < W and 0 <= ny < H and not seen[ny * W + nx] \
                            and member(nx, ny):
                        seen[ny * W + nx] = 1
                        stack.append((nx, ny))
            comps.append(comp)
    return comps


def key_background(slot):
    """Key the background without eating the pet.

    Transparent = chroma-distance pixels connected to the slot border, plus
    enclosed pockets that are near-pure chroma (gaps between legs/tail).
    Interior pixels merely close to green (eyes, shading) survive. Also
    drops neighbor-bleed: disconnected opaque components hugging the slot's
    left/right edge (the next frame's dog crossing the slot boundary)."""
    px = slot.load()
    W, H = slot.size
    t2 = THRESHOLD * THRESHOLD

    def dist2(x, y):
        r, g, b = px[x, y][:3]
        return (r - KEY[0])**2 + (g - KEY[1])**2 + (b - KEY[2])**2

    chroma = _components(W, H, lambda x, y: dist2(x, y) <= t2)
    keyed = set()
    p2 = PURE_THRESHOLD * PURE_THRESHOLD
    for comp in chroma:
        touches_border = any(x in (0, W-1) or y in (0, H-1) for x, y in comp)
        near_pure = sum(dist2(x, y) for x, y in comp) / len(comp) <= p2
        if touches_border or (near_pure and len(comp) >= 30):
            keyed.update(comp)
    for x, y in keyed:
        px[x, y] = (0, 0, 0, 0)

    # neighbor bleed: opaque components glued to the slot's vertical edges
    opaque = _components(W, H, lambda x, y: px[x, y][3] >= 16)
    if opaque:
        main = max(opaque, key=len)
        for comp in opaque:
            if comp is main or len(comp) >= 0.3 * len(main):
                continue
            xs = [x for x, _ in comp]
            if min(xs) <= 2 or max(xs) >= W - 3:
                for x, y in comp:
                    px[x, y] = (0, 0, 0, 0)
                keyed.update(comp)

    # despill: on opaque pixels bordering keyed areas, cap green
    for x, y in list(keyed):
        for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in keyed:
                r, g, b, a = px[nx, ny]
                if a and g > max(r, b):
                    px[nx, ny] = (r, max(r, b), b, a)
    return slot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("strip")
    ap.add_argument("n_frames", type=int)
    ap.add_argument("out_dir")
    ap.add_argument("--target-height", type=int, default=None,
                    help="content height (px) the tallest frame should get")
    args = ap.parse_args()

    strip = Image.open(args.strip).convert("RGBA")
    W, H = strip.size
    slot_w = W // args.n_frames
    slots = [key_background(strip.crop((i * slot_w, 0, (i + 1) * slot_w, H)))
             for i in range(args.n_frames)]

    # registration: the pet drifts AND leans progressively across drawn
    # slots (translation alone leaves 15px+ of smear). Align each slot to
    # slot 0 with a rotation+translation search on half-res silhouettes,
    # pivoting rotation at the silhouette's foot center. Report the
    # residual per frame so the caller can drop frames that never align.
    def half_alpha(img):
        return img.getchannel("A").resize(
            (img.size[0] // 2, img.size[1] // 2), Image.BILINEAR)

    ref = half_alpha(slots[0])
    ref_bytes = ref.tobytes()
    RW, RH = ref.size
    rb = slots[0].getchannel("A").getbbox()
    pivot = ((rb[0] + rb[2]) / 2, rb[3])  # foot center, full-res coords
    residuals = [0.0]
    for i in range(1, args.n_frames):
        base = slots[i]
        def sad_at(rot, dx, dy, _cache={}):
            if rot not in _cache:
                img = base.rotate(rot, resample=Image.BICUBIC,
                                  center=pivot) if rot else base
                _cache[rot] = half_alpha(img)
            cand = _cache[rot].crop((dx, dy, dx + RW, dy + RH)).tobytes()
            return sum(abs(p - q) for p, q in zip(ref_bytes, cand))
        space = [(sad_at(r, dx, dy), r, dx, dy)
                 for r in (-4, -2, 0, 2, 4)
                 for dx in range(-16, 17, 4) for dy in range(-6, 7, 3)]
        _, r0, x0, y0 = min(space)
        space = [(sad_at(r, dx, dy), r, dx, dy)
                 for r in (r0 - 1, r0 - 0.5, r0, r0 + 0.5, r0 + 1)
                 for dx in range(x0 - 3, x0 + 4) for dy in range(y0 - 2, y0 + 3)]
        sad, r, dx, dy = min(space)
        residuals.append(sad / (RW * RH))
        img = base.rotate(r, resample=Image.BICUBIC, center=pivot) if r else base
        if dx or dy:
            shifted = Image.new("RGBA", img.size, (0, 0, 0, 0))
            shifted.paste(img, (-dx * 2, -dy * 2), img)
            img = shifted
        slots[i] = img
    print("alignment residual per frame:",
          [round(x, 1) for x in residuals])

    boxes = [s.getchannel("A").getbbox() for s in slots]
    union = (min(b[0] for b in boxes), min(b[1] for b in boxes),
             max(b[2] for b in boxes), max(b[3] for b in boxes))
    uw, uh = union[2] - union[0], union[3] - union[1]
    target_h = args.target_height or (CELL_H - 15)
    scale = min(target_h / uh, (CELL_W - 8) / uw)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sw, sh = round(uw * scale), round(uh * scale)
    ox = (CELL_W - sw) // 2
    oy = CELL_H - BOTTOM_MARGIN - sh
    for i, s in enumerate(slots):
        content = s.crop(union).resize((sw, sh), Image.LANCZOS)
        cell = Image.new("RGBA", (CELL_W, CELL_H), (0, 0, 0, 0))
        cell.paste(content, (ox, oy), content)
        cell.save(out / f"{i:02d}.png")
    print(f"{args.strip} -> {out}: {args.n_frames} cells, scale {scale:.3f}, "
          f"union {uw}x{uh}")


if __name__ == "__main__":
    main()
