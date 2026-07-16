Create one horizontal animation strip for Codex pet `apollo-flat-vector`, state `idle`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure user-selected #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `flat-vector`: Flat vector-style mascot with simple geometric forms, crisp color areas, clean outline, and minimal shading. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Calm low-distraction seated resting loop: gentle breathing and one soft blink only.

State requirements:
- CRITICAL: idle is the low-distraction baseline state and the first frame is also used as the reduced-motion static pet.
- Use only subtle idle motion: gentle breathing, a tiny blink, a slight head or body bob, a very small material sway, or another quiet motion that fits the pet persona.
- Keep the pet essentially in the same pose, facing direction, silhouette, markings, palette, and prop state across all 6 frames.
- Idle variation must stay calm but still read as animation; do not repeat effectively identical copies across the loop.
- Do not show waving, walking, running, jumping, talking, working, reviewing, emotional reactions, large gestures, item interactions, or new props.
- Feet, base, body, or object anchor should remain planted or nearly planted.
- The first and last frames should be very close visually so the loop feels calm and does not pop.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Smooth-loop contract: These are six consecutive in-between instants of ONE continuous cycle, not six distinct poses. Frame 6 must flow seamlessly into frame 1. Keep the same camera, scale, body position, footing, and limb configuration in every frame; adjacent frames must be nearly identical and read as the next instant, not a new pose.
Motion brief: The attached pose-family anchor is the exact frame-0 pose. Reproduce its seated Apollo pose identically in all 6 slots. Use this closed-loop timing: frame 1 rest; frame 2 tiny chest/shoulder rise; frame 3 peak rise with eyes beginning a soft blink; frame 4 peak rise with blink closed; frame 5 tiny chest/shoulder rise with eyes open; frame 6 rest, matching frame 1. The ONLY motion is a 2–3 pixel breathing rise in the chest and shoulders plus that two-frame blink. Lock tail, legs, paws, head position, body outline, coat markings, face, and proportions absolutely. Every dog must be fully inside its own slot with at least 30px clear green background margin on every side. No head bob, ear motion, tail motion, limb motion, or marking changes.
