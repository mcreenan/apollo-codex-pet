Create one horizontal animation strip for Codex pet `apollo-clay`, state `review`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure chroma green #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `clay`: Handmade clay or polymer-clay mascot with rounded sculpted forms, soft material texture, simple features, and clean readable edges. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Ready-review loop: a quiet, pleased review expression shown only through a subtle head bob and a soft blink; do not change the proud sitting pose.

State requirements:
- Show review through lean, blink, narrowed eyes, head tilt, or paw/hand position.
- Do not add magnifying glasses, papers, code, UI, punctuation, symbols, or other new props unless they already exist in the base pet identity.

Smooth-loop contract: Use the attached current pose-family anchor to keep Apollo sitting proudly in exactly that stance. The six slots are consecutive in-between instants of ONE seamless motion cycle, including frame 6 flowing directly into frame 1—not six distinct poses. Lock camera, scale, body, legs, paws, tail, footing, markings, and identity in every slot. The tail rests in the exact same fixed position in every frame: no wag, sweep, repositioning, blur, or ghosting. The ONLY animation is a subtle happy head bob: head at the anchor height in frames 1 and 6, dropping only a few pixels toward the middle frames, then rising smoothly; include one soft blink across two adjacent middle frames. Apollo has an open, pleased mouth throughout. Adjacent frames must be nearly identical and read as the next instant; nothing else changes.

Clean extraction: crisp fully opaque edges with a clean non-green outer contour, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, green spill, green reflection, green halo, or chroma-key green #00B140 inside or touching the pet. The #00B140 background must remain perfectly flat and stop sharply at the pet edge for clean extraction.
