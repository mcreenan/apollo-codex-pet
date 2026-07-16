# Task: Regenerate `idle` and `review` rows for apollo-flat-vector (simplified motion)

Read and follow the hatch-pet skill at `~/.codex/skills/hatch-pet/SKILL.md`; use `$imagegen` per `~/.codex/skills/.system/imagegen/SKILL.md`. Headless; no confirmations. Subagents allowed.

The run at `runs/flat-vector-smooth` already exists (canonical base at `runs/flat-vector-smooth/references/canonical-base.png`, layout guides prepared). The previous `idle` and `review` rows failed QA: frame 1 of each strip had the dog partially cut off at the slot's left edge, and later frames drifted off-model (markings and body proportions changed).

Regenerate ONLY these two rows, with SIMPLER motion so every frame keeps an identical body, and with the dog fully inside each slot with clear margin on all sides:

- `idle`: Apollo sits calmly, exactly matching frame 0 of the top row of `dist/codex-pets/apollo-flat-vector/spritesheet.webp` (crop it as the pose-family anchor). The ONLY motion across the 6 frames: a gentle breathing cycle (chest/shoulders rise a few pixels toward mid-loop and settle back) and one soft blink across two adjacent mid-loop frames. Tail, legs, paws, head position, markings: locked.
- `review`: Apollo sits proudly, matching frame 0 of the bottom row of the same spritesheet (crop as anchor). Tail RESTS in one fixed position the whole loop — no wag. The ONLY motion: a subtle happy head bob (head drops a few pixels toward mid-loop and rises back) and one soft blink across two adjacent mid-loop frames. Mouth open and pleased in every frame.
- Smooth-loop contract for both: the six slots are consecutive in-between instants of ONE seamless cycle, frame 6 flowing into frame 1; adjacent frames nearly identical; lock camera, scale, body, legs, paws, tail, footing, markings, identity. EVERY frame fully inside its slot with at least 30px of background margin on every side.

Update `runs/flat-vector-smooth/prompts/rows/{idle,review}.md` accordingly (keep all standard identity/chroma/extraction requirements, chroma green #00B140), generate with the layout guide + canonical base + pose anchor attached, then re-extract just these rows (`extract_strip_frames.py --states idle,review`, `--method stable-slots` if needed) and re-run inspection and your smoothness QA. Max 2 attempts per row, then report best effort.

## Final response — return exactly:

frames_root=<absolute path to runs/flat-vector-smooth/frames>
rows=idle:<pass|fail>,review:<pass|fail>
notes=<one sentence>
