# Task: Regenerate 4 clay rows as SMOOTH continuous motion loops

Read and follow the hatch-pet skill at `~/.codex/skills/hatch-pet/SKILL.md` and use `$imagegen` (per `~/.codex/skills/.system/imagegen/SKILL.md`) for all visual generation. Headless: never pause for confirmation. Subagents allowed per the skill.

This is a PARTIAL run: regenerate ONLY the `idle`, `waiting`, `running`, and `review` rows for the existing pet `apollo-clay`. Do NOT generate the other five rows, do NOT compose a full atlas, do NOT package.

## Why (the contract that matters most)

The current rows are six *distinct poses* per state; played in sequence they look choppy. Each regenerated row must instead be **six consecutive in-between frames of ONE continuous motion cycle** that loops seamlessly (frame 6 flows back into frame 1). Within a row: same camera, same scale, same body position, same footing, same limb configuration in every frame — only the intended micro-motion changes between adjacent frames. Adjacent frames should look nearly identical; the motion should only be obvious when the loop plays. Judge smoothness by flipping between adjacent frames: if any two adjacent frames read as "a different pose" rather than "the next instant of the same motion", the row fails.

## Setup

1. Bootstrap a run at `runs/clay-smooth` with `prepare_pet_run.py`:
   - pet-name "Apollo", pet-id `apollo-clay`, display-name "Apollo (Clay)"
   - description: "Apollo, a friendly medium-sized mutt with a white/creme coat, brown saddle patches, and a brown face mask split by a white blaze — clay edition."
   - style preset `clay`
   - references: `refs/IMG_4195.png`, `refs/IMG_0887.png`, `refs/IMG_9501.png`, `variants/apollo-clay.png`
   - pet notes: "White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression."
   - style notes: "keep the exact style, palette, proportions, and markings of the canonical base image across every row."
2. The canonical base is ALREADY APPROVED: copy `variants/apollo-clay.png` in as the base job's selected output (per the skill), create `references/canonical-base.png`, mark the base job complete. Do not regenerate the base.
3. Pose-family anchors: the currently shipped cells live in `dist/codex-pets/apollo-clay/spritesheet.webp` (192×208 cells, rows top-to-bottom: idle, running-right, running-left, waving, jumping, failed, waiting, running, review). Crop frame 0 of each of the four target rows to PNG and attach it to that row's generation job as an extra reference labeled "current pose family — keep this stance". The regenerated row must stay in the same stance family so the pet doesn't change character between states.

## Row choreography (edit each row's prompt file before generating)

Keep everything the skill's row prompts already require (chroma green #00B140, layout guide adherence, identity lock, no text/effects/shadows), and ADD the smooth-loop contract above plus this per-row motion brief:

- `idle` — sitting at rest exactly like the anchor frame. One slow breath over the loop: chest/shoulders rise ~2% by mid-loop and settle back; ears relax slightly; eyes do one soft blink across two adjacent mid-loop frames. Legs, paws, tail, and head position do not move.
- `waiting` — sitting attentive like the anchor frame, one forepaw slightly raised the ENTIRE loop (never lowered). The raised paw bobs a few pixels; the head tilts gently a few degrees to one side and back over the loop; ears perk. Nothing else moves.
- `running` — non-directional busy trot in place, facing the camera like the anchor frame: one coherent 6-phase gait cycle (legs progress through the trot phases in order, body bobs slightly with the gait). This row may show real leg motion — but it must be ONE cycle in phase order, not six unrelated running poses. No speed lines, no dust, no literal ground.
- `review` — sitting proudly like the anchor frame. The tail does one full wag sweep (left → center → right → center) across the loop; a subtle happy head bob; mouth open, pleased. Legs and paws planted throughout.

## Generate, extract, QA

- One `$imagegen` worker per row, each using: the row prompt file, the layout guide, `references/canonical-base.png`, and that row's pose-family anchor crop.
- Extract only these rows: `extract_strip_frames.py --states idle,waiting,running,review` into `runs/clay-smooth/frames/`; run `inspect_frames.py` on them. Use `--method stable-slots` (with the matching inspect flag) if per-frame fit causes size popping and the strip itself is stable.
- Smoothness QA per row (in addition to the skill's identity QA): for each adjacent frame pair (including 6→1), the frames must read as the same pose one instant apart. If a row fails identity or smoothness, repair per the skill (max 2 repair passes per row), then accept best effort and note it.
- Leave the final keyed 192×208 RGBA frames at `runs/clay-smooth/frames/<state>/`. Keep the decoded strips. No atlas, no packaging, no cleanup of frames.

## Final response — return exactly:

frames_root=<absolute path to runs/clay-smooth/frames>
rows=idle:<pass|fail>,waiting:<pass|fail>,running:<pass|fail>,review:<pass|fail>
notes=<one or two sentences on any compromises or repairs>
