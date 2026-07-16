Create one horizontal animation strip for Codex pet `apollo-sticker`, state `idle`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on perfectly flat solid chroma green #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `sticker`: Polished sticker mascot with bold clean shapes, crisp outline, flat colors, and minimal highlight detail. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Calm low-distraction resting loop: subtle breathing, tiny blink, slight head/body bob, and only quiet persona-preserving motion.

State requirements:
- CRITICAL: idle is the low-distraction baseline state and the first frame is also used as the reduced-motion static pet.
- Use only subtle idle motion: gentle breathing, a tiny blink, a slight head or body bob, a very small material sway, or another quiet motion that fits the pet persona.
- Keep the pet essentially in the same pose, facing direction, silhouette, markings, palette, and prop state across all 6 frames.
- Idle variation must stay calm but still read as animation; do not repeat effectively identical copies across the loop.
- Do not show waving, walking, running, jumping, talking, working, reviewing, emotional reactions, large gestures, item interactions, or new props.
- Feet, base, body, or object anchor should remain planted or nearly planted.
- The first and last frames should be very close visually so the loop feels calm and does not pop.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Pose-family anchor: use the attached current `idle` pose-family crop as the stance reference. Keep its exact sitting stance, camera, footing, body position, scale, and limb configuration.

Smooth-loop contract: these are six consecutive in-between frames of one continuous motion cycle, not six distinct poses. Adjacent frames (including frame 6 to frame 1) must read as the next instant of the same pose; keep camera, scale, body position, footing, limb configuration, paws, tail, and head position fixed. Only the stated micro-motion may change.
Motion brief: sitting at rest exactly like the anchor. Make one slow breath over the loop: chest and shoulders rise about 2% by mid-loop, then settle back. Ears relax slightly. Put one soft blink across two adjacent mid-loop frames. Legs, paws, tail, and head position do not move.
