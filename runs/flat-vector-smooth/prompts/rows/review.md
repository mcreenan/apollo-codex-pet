Create one horizontal animation strip for Codex pet `apollo-flat-vector`, state `review`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure user-selected #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `flat-vector`: Flat vector-style mascot with simple geometric forms, crisp color areas, clean outline, and minimal shading. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Proud seated happy review loop: subtle head bob and one soft blink only; mouth open and pleased throughout.

State requirements:
- Show review through lean, blink, narrowed eyes, head tilt, or paw/hand position.
- Do not add magnifying glasses, papers, code, UI, punctuation, symbols, or other new props unless they already exist in the base pet identity.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Smooth-loop contract: These are six consecutive in-between instants of ONE continuous cycle, not six distinct poses. Frame 6 must flow seamlessly into frame 1. Keep the same camera, scale, body position, footing, and limb configuration in every frame; adjacent frames must be nearly identical and read as the next instant, not a new pose.
Motion brief: The attached pose-family anchor is the exact frame-0 pose. Reproduce its proud seated Apollo pose identically in all 6 slots, with the mouth open and pleased in every frame. Use this closed-loop timing: frame 1 head at anchor height; frame 2 head 1–2px lower; frame 3 head 3px lower with eyes beginning a soft blink; frame 4 head 3px lower with blink closed; frame 5 head 1–2px lower with eyes open; frame 6 head at anchor height, matching frame 1. The ONLY motion is this subtle happy head bob and the two-frame blink. Tail rests in one fixed position for the entire loop. Lock camera, scale, body, legs, paws, footing, body outline, coat markings, proportions, and identity. Every dog must be fully inside its own slot with at least 30px clear green background margin on every side. No tail wag, body bounce, limb motion, or marking changes.
