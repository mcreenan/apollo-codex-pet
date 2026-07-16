Create one horizontal animation strip for Codex pet `apollo-plush`, state `running`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure blue #0000FF. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `plush`: Soft plush toy mascot with rounded stitched forms, fuzzy fabric feel, simple sewn details, and readable toy-like proportions. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Non-directional busy trot in place, facing the camera like the supplied pose-family anchor. It is a stationary six-phase gait cycle for active task work, never directional travel.

State requirements:
- Show the pet actively working or processing through a compact, camera-facing stationary busy trot: focused posture, ordered leg motion, and tiny body bobbing.
- Do not show directional travel, speed lines, dust clouds, floor shadows, motion trails, detached motion effects, a literal ground, or oversized sprinting strides.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Smooth-loop contract (mandatory): These are six consecutive in-between instants from ONE seamless continuous motion cycle, not six unrelated running poses. Frame 6 must flow naturally into frame 1. Keep the same camera, scale, centered body position, and stable overall footing. Adjacent frames must read as the next instant of the same motion.

Motion brief: Match the supplied current-pose-family anchor exactly: facing the camera. Produce one coherent six-phase compact trot-in-place gait, with legs progressing through the gait phases in order and a slight synchronized body bob. Real leg motion is allowed only as this continuous phase-ordered cycle; no pose jumps, no lateral travel, no speed lines, dust, or literal ground.

Repair precision: Preserve every non-leg part of the anchor pose. Make the six cells consecutive in-betweens, not six broad key poses: each leg moves only a small fraction of its total stride from one cell to the next. Phase order must be a continuous repeating diagonal trot and the final frame must be only one small gait increment from the first. The loop must look smooth when flipping every neighboring pair.
