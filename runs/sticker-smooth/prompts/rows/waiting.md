Create one horizontal animation strip for Codex pet `apollo-sticker`, state `waiting`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on perfectly flat solid chroma green #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `sticker`: Polished sticker mascot with bold clean shapes, crisp outline, flat colors, and minimal highlight detail. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Needs-input loop: expectant asking pose for approval, help, or user input.

State requirements:
- Show that Codex needs approval, help, or user input through an expectant asking pose.
- Keep the motion patient and readable, without turning it into ordinary idle or review.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Pose-family anchor: use the attached current `waiting` pose-family crop as the stance reference. Keep its exact sitting-attentive stance, camera, footing, body position, scale, and limb configuration.

Smooth-loop contract: these are six consecutive in-between frames of one continuous motion cycle, not six distinct poses. Adjacent frames (including frame 6 to frame 1) must read as the next instant of the same pose; keep camera, scale, body position, footing, and limb configuration fixed. Only the stated micro-motion may change.
Motion brief: sitting attentive like the anchor with one forepaw slightly raised in every frame; never lower it. The raised paw bobs only a few pixels, the head gently tilts a few degrees to one side and back over the loop, and ears stay perked. Nothing else moves.
