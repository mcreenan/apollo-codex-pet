# Task: Hatch a complete Codex pet — Apollo, pixel edition

Read and follow the hatch-pet skill at `~/.codex/skills/hatch-pet/SKILL.md`, completing the ENTIRE workflow through packaging and cleanup. Use `$imagegen` (per `~/.codex/skills/.system/imagegen/SKILL.md`) for all visual generation. You are running headless: do not pause to ask for confirmation; make reasonable decisions and proceed. You have permission to use subagents/lightweight workers as the skill directs.

## Pet identity

- Pet id: `apollo-pixel`
- Display name: `Apollo (Pixel)`
- Description: "Apollo, a friendly medium-sized mutt with a white/creme coat, brown saddle patches, and a brown face mask split by a white blaze — pixel edition."
- Style preset: `pixel`

## Canonical base — ALREADY GENERATED AND USER-APPROVED

`variants/apollo-pixel.png` was generated earlier with $imagegen from Apollo's photos and the user approved it as the canonical look. Do NOT regenerate the base from scratch: copy this image in as the base job's selected output (it satisfies the base contract: single centered full-body pet on flat #00B140 chroma green, no text/shadows/effects), create `references/canonical-base.png` from it, and mark the base job complete. Then generate all 9 animation rows grounded on it per the skill.

## Reference photos (identity grounding, pass via --reference)

- refs/IMG_4195.png — full body, sitting, facing camera
- refs/IMG_0887.png — face close-up (mask + blaze detail)
- refs/IMG_9501.png — full body side profile (saddle patches)
- variants/apollo-pixel.png — canonical approved base look

## Run parameters

- Run directory: runs/pixel
- Pet notes for prompts: "White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression."
- Style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row.

## Completion requirements

- Run the full deterministic pipeline: extract frames, inspect, compose atlas, validate, contact sheet, motion previews.
- Run final visual QA per the skill; repair failing rows (max 2 repair passes per row, then accept best effort and note it).
- Package to `~/.codex/pets/apollo-pixel/` (pet.json + spritesheet.webp).
- Keep qa/contact-sheet.png and qa/previews/ in the run dir; perform the skill's normal cleanup of intermediates.

## Final response — return exactly:

package=<absolute path to installed pet dir>
validation=<pass|fail>
visual_qa=<pass|fail>
notes=<one or two sentences on any compromises or repairs>
