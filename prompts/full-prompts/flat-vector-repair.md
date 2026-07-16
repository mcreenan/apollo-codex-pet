# Task: Repair the apollo-flat-vector hatch-pet run

Read and follow the hatch-pet skill at `~/.codex/skills/hatch-pet/SKILL.md`, specifically its Repair Workflow. Use `$imagegen` (per `~/.codex/skills/.system/imagegen/SKILL.md`) for any regeneration. Headless: do not pause for confirmation. Subagents allowed.

## Existing run

Run directory: runs/flat-vector
It completed with validation=pass but visual_qa=fail. Known defects from inspecting qa/contact-sheet.png:

1. **running-left row: frame 6 contains TWO overlapping dog sprites in one slot** — hard failure. The row also shows inconsistent per-frame scale (sprites shrink/grow across the loop).
2. **jumping row: mild size popping** (frame 4 noticeably smaller than the others).

## Repair instructions

- For running-left: the running-right row is healthy. Prefer deriving running-left by mirroring the approved running-right via `scripts/derive_running_left_from_running_right.py` (frame-by-frame, preserving temporal order). Only regenerate via $imagegen if mirroring is inappropriate.
- For jumping: if the source strip in decoded/ is stable and the popping is extraction-induced, rerun extraction with `--method stable-slots` (with `--allow-stable-slots` on inspection) rather than regenerating. Regenerate the row only if the strip itself is bad.
- The canonical base is at runs/flat-vector/references/canonical-base.png; identity and flat-vector style must be preserved.
- After repairs: re-run extract/inspect/compose/validate/contact-sheet/previews, then final visual QA per the skill.
- Re-stage the finished package (pet.json + spritesheet.webp) at runs/flat-vector/package-staging/apollo-flat-vector (id `apollo-flat-vector`, displayName `Apollo (Flat Vector)`).

## Final response — return exactly:

package=<absolute path to staged package dir>
validation=<pass|fail>
visual_qa=<pass|fail>
notes=<one or two sentences on what was repaired>
