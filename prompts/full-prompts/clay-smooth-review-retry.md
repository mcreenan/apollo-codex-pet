# Task: One more smooth `review` row for apollo-clay (simplified motion)

Read and follow the hatch-pet skill at `~/.codex/skills/hatch-pet/SKILL.md`; use `$imagegen` per `~/.codex/skills/.system/imagegen/SKILL.md`. Headless; no confirmations. Subagents allowed.

The run at `runs/clay-smooth` already exists (canonical base at `runs/clay-smooth/references/canonical-base.png`, layout guides prepared, and a review pose-family anchor was already used). A previous attempt at the `review` row failed smoothness QA with abrupt tail/body ghosting: the tail-wag brief made the model reposition the tail and body between frames.

Regenerate ONLY the `review` row, with this SIMPLER motion so every frame keeps an identical body:

- Apollo sits proudly, exactly matching the pose-family anchor (frame 0 of the bottom row of `dist/codex-pets/apollo-clay/spritesheet.webp` — crop it as the anchor reference again). Tail RESTS in one fixed position the entire loop — no wag.
- The ONLY motion across the 6 frames: a subtle happy head bob (head drops a few pixels toward mid-loop and rises back) and one soft blink across two adjacent mid-loop frames. Mouth open and pleased in every frame.
- Smooth-loop contract: the six slots are consecutive in-between instants of ONE seamless cycle, frame 6 flowing into frame 1; adjacent frames nearly identical; lock camera, scale, body, legs, paws, tail, footing, markings, identity.

Update `runs/clay-smooth/prompts/rows/review.md` accordingly (keep all standard identity/chroma/extraction requirements, chroma green #00B140), generate with the layout guide + canonical base + pose anchor attached, then re-extract just this row (`extract_strip_frames.py --states review`, `--method stable-slots` if needed) and re-run inspection and your smoothness QA on it. Max 2 attempts, then report best effort.

## Final response — return exactly:

frames_dir=<absolute path to runs/clay-smooth/frames/review>
row=review:<pass|fail>
notes=<one sentence>
