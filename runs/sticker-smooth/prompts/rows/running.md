Create one horizontal animation strip for Codex pet `apollo-sticker`, state `running`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on perfectly flat solid chroma green #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `sticker`: Polished sticker mascot with bold clean shapes, crisp outline, flat colors, and minimal highlight detail. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Non-directional busy trot in place, facing the camera like the anchor: a coherent gait cycle with no directional travel.

State requirements:
- Show a compact busy trot in place, facing camera, with legs progressing through the trot phases in order and a tiny body bob. There is no direction, travel, speed-line, dust, or literal ground.
- Do not show long strides, directional travel, speed lines, dust clouds, floor shadows, motion trails, detached motion effects, or a treadmill.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Pose-family anchor: use the attached current `running` pose-family crop as the stance reference. Keep its camera, front-facing character, apparent scale, body placement, and compact silhouette.

Smooth-loop contract: these are six consecutive in-between frames of one continuous motion cycle, not six unrelated running poses. Adjacent frames (including frame 6 to frame 1) must be the next gait instant, with stable camera, scale, body placement, and overall compact posture. Use one coherent six-phase trot cycle in order; only the leg phase and subtle body bob change between frames.
Motion brief: non-directional busy trot in place, facing the camera like the anchor. The gait must visibly progress phase by phase and loop seamlessly. No speed lines, dust, or literal ground.
