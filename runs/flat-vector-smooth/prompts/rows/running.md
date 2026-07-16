Create one horizontal animation strip for Codex pet `apollo-flat-vector`, state `running`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure user-selected #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `flat-vector`: Flat vector-style mascot with simple geometric forms, crisp color areas, clean outline, and minimal shading. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Non-directional busy trot in place, facing the camera like the attached pose-family anchor: active task effort through one coherent six-phase gait cycle. No directional travel.

State requirements:
- Show one coherent in-place trot gait: legs progress through six ordered trot phases and the body bobs slightly with that gait. Keep the pet front-facing and in the anchor stance family. This is the one exception to the normal no-locomotion rule: do show modest leg motion, but no travel.
- Do not show speed lines, dust clouds, floor shadows, motion trails, detached motion effects, or any literal ground.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Smooth-loop contract: These are six consecutive in-between instants of ONE continuous gait cycle, not six unrelated running poses. Frame 6 must flow seamlessly into frame 1. Keep camera, scale, body position, and footing stable except for the deliberately ordered leg-cycle and tiny body bob; adjacent frames must read as the next instant.
