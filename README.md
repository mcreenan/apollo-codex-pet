# Apollo Pets

Apollo (a medium-sized mutt — white/creme coat, brown saddle patches, brown
face mask split by a white blaze) as an animated coding-agent pet, in six art
styles, for two hosts: the Codex CLI and [Orca](https://onorca.dev).

Everything was generated from three photos via the
[openai/skills `hatch-pet` skill](https://github.com/openai/skills) and
`$imagegen`, then post-processed with the scripts in `scripts/`.

## Styles

`pixel` · `plush` · `sticker` · `flat-vector` · `clay` · `painterly`

Approved base looks live in `variants/` (a 7th, `3d-toy`, has a base image but
its full run was cancelled).

## Layout

| Path | Contents |
|---|---|
| `photos/` | The three source photos of Apollo used for identity grounding |
| `refs/` | Same photos converted/resized to ≤1536px PNG for `$imagegen` |
| `variants/` | User-approved base look per style (full body on chroma green) |
| `dist/codex-pets/` | Native Codex CLI pets: `pet.json` + 8×9 spritesheet |
| `dist/codex-pet-bundles/` | Orca-importable `.codex-pet` bundles (v2 + v3) |
| `qa/<style>/` | Contact sheet + animation preview GIFs from each hatch run |
| `prompts/` | The codex exec prompts that drove generation (reproducibility) |
| `scripts/` | Post-processing generators (see below) |

## Installing

**Codex CLI** — copy a pet dir into place:

```bash
cp -R dist/codex-pets/apollo-plush ~/.codex/pets/
```

**Orca** — import a bundle via the status-bar pet menu → *Import .codex-pet*.
Prefer the `-v3` bundles.

## The two Orca bundle generations

Orca plays spritesheet pets with one flat fps, uniform `steps()` timing, and
only five of the nine animation rows: `idle`, `running` (working), `waiting`,
`review`, and `jumping` (a frozen frame while dragging). Both bundle versions
target that reality:

- **v2** (`Apollo-<style>.codex-pet`) — 8 columns @ 6fps. Held key frames and
  short ping-pong loops; simple but calm. Built by `scripts/orca-retime.py`.
- **v3** (`Apollo-<style>-v3.codex-pet`) — 48 columns @ 12fps. Each played
  state is a 4-second choreographed loop: the designed pose cycle held 4
  frames per pose, with eased transforms (breathing squash, sway, trot bob,
  wag rotation, mini-hops) gliding on every frame. All frames are synthesized
  from the 57 real poses — no regeneration. Built by `scripts/orca-v3.py`.

Orca manifest limits (from its import validator): ≤512 frames per animation
(and ≤ sheet columns), fps ≤ 60, frame ≤ 1024px per side, sheet ≤ 64MB,
sheet dimensions must be clean multiples of the frame size. WebP itself caps
dimensions at 16383px → 85 columns max at 192px cells.

## Scripts

```bash
# v2: retime a native codex pet for Orca's flat-fps playback
python3 scripts/orca-retime.py dist/codex-pets/apollo-plush out/Apollo-plush.codex-pet

# v3: 48-column choreographed bundle from a native codex pet
python3 scripts/orca-v3.py dist/codex-pets/apollo-plush out/Apollo-plush-v3.codex-pet
```

Both save WebP with `lossless=True, exact=True` — without `exact`, libwebp
rewrites RGB under fully-transparent pixels and the hatch-pet validator
rejects the sheet.

## Regenerating a style from scratch

1. Generate/approve a base look with `prompts/variant-prompt.md`.
2. Fill `prompts/full-run-template.md` (or use a ready file in
   `prompts/full-prompts/`) and run it headless:
   `codex exec --skip-git-repo-check -s workspace-write - < prompt.md`.
3. The codex sandbox can't write `~/.codex/pets` — copy the staged package in
   manually, then run the Orca scripts above.
