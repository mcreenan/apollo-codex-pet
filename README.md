# Apollo Codex Pets

Apollo is my dog. I wanted to make him into a digital companion to keep me
company while I'm at the office, so here he is as an animated coding-agent
pet, in six art styles, for two hosts: the Codex CLI and
[Orca](https://onorca.dev).

Everything was generated from three photos via the
[openai/skills `hatch-pet` skill](https://github.com/openai/skills) and
`$imagegen`, then post-processed with the scripts in `scripts/`.

## Styles

Idle animation for each style (GIF previews in `docs/gifs/`, built from the
idle row of the native spritesheets):

| `pixel` | `plush` | `sticker` |
|:---:|:---:|:---:|
| ![pixel](docs/gifs/pixel-idle.gif) | ![plush](docs/gifs/plush-idle.gif) | ![sticker](docs/gifs/sticker-idle.gif) |

| `flat-vector` | `clay` | `painterly` |
|:---:|:---:|:---:|
| ![flat-vector](docs/gifs/flat-vector-idle.gif) | ![clay](docs/gifs/clay-idle.gif) | ![painterly](docs/gifs/painterly-idle.gif) |

## Layout

| Path | Contents |
|---|---|
| `photos/` | The three source photos of Apollo used for identity grounding |
| `refs/` | Same photos converted/resized to ≤1536px PNG for `$imagegen` |
| `variants/` | User-approved base look per style (full body on chroma green) |
| `dist/codex-pets/` | Native Codex CLI pets: `pet.json` + 8×9 spritesheet |
| `dist/codex-pet-bundles/` | Orca-importable `.codex-pet` bundles, generated from `dist/codex-pets/` |
| `prompts/` | The codex exec prompts that drove generation (reproducibility) |
| `docs/gifs/` | Idle-animation GIF previews per style (used in this README) |
| `scripts/` | Post-processing generators (see below) |

## Installing

**Codex CLI** — copy a pet dir into place:

```bash
cp -R dist/codex-pets/apollo-plush ~/.codex/pets/
```

**Orca** — import a bundle via the status-bar pet menu → *Import .codex-pet*.

## The Orca bundles

Orca plays spritesheet pets with one flat fps, uniform `steps()` timing, and
only five of the nine animation rows: `idle`, `running` (working), `waiting`,
`review`, and `jumping` (a frozen frame while dragging). The bundles target
that reality: 48 columns @ 12fps, where each played state is a 4-second
choreographed loop — the designed pose cycle held 4 frames per pose, with
eased transforms (breathing squash, sway, trot bob, wag rotation, mini-hops)
gliding on every frame, and every frame anchored by its content bounding box
to a common foot baseline so the pet stays planted. All frames are
synthesized from the 57 real poses — no regeneration. Built by
`scripts/orca-bundle.py`.

The two `dist/` dirs are one artifact per host, not duplicates: the native
Codex CLI pets in `dist/codex-pets/` are also the only final-form home of
the 57 raw poses, making them the source the bundle script reads. Bundles
are regenerable from them in seconds; the reverse is not true, so
`dist/codex-pets/` is the dir to protect.

Orca manifest limits (from its import validator): ≤512 frames per animation
(and ≤ sheet columns), fps ≤ 60, frame ≤ 1024px per side, sheet ≤ 64MB,
sheet dimensions must be clean multiples of the frame size. WebP itself caps
dimensions at 16383px → 85 columns max at 192px cells.

## Scripts

```bash
# build a 48-column choreographed Orca bundle from a native codex pet
python scripts/orca-bundle.py dist/codex-pets/apollo-plush out/Apollo-plush.codex-pet
```

Saves WebP with `lossless=True, exact=True` — without `exact`, libwebp
rewrites RGB under fully-transparent pixels and the hatch-pet validator
rejects the sheet.

## Regenerating a style from scratch

1. Generate/approve a base look with `prompts/variant-prompt.md`.
2. Fill `prompts/full-run-template.md` (or use a ready file in
   `prompts/full-prompts/`) and run it headless:
   `codex exec --skip-git-repo-check -s workspace-write - < prompt.md`.
3. The codex sandbox can't write `~/.codex/pets` — copy the staged package in
   manually, then run the Orca script above.
