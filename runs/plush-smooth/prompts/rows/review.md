Create one horizontal animation strip for Codex pet `apollo-plush`, state `review`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure blue #0000FF. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `plush`: Soft plush toy mascot with rounded stitched forms, fuzzy fabric feel, simple sewn details, and readable toy-like proportions. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Ready-review loop: focused inspection of completed output with lean, blink, narrowed eyes, head tilt, or paw pose.

State requirements:
- Show review through lean, blink, narrowed eyes, head tilt, or paw/hand position.
- Do not add magnifying glasses, papers, code, UI, punctuation, symbols, or other new props unless they already exist in the base pet identity.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Smooth-loop contract (mandatory): These are six consecutive in-between instants from ONE seamless continuous motion cycle, not six different pose ideas. Frame 6 must flow naturally into frame 1. Keep the same camera, scale, body position, footing, and limb configuration in every frame; adjacent frames must be nearly identical and read as the next instant of the same pose.

Motion brief: Match the supplied current-pose-family anchor exactly: sitting proudly, mouth open and pleased. Tail performs one full smooth wag sweep left to center to right to center across the loop; give the head a subtle happy bob. Legs and paws stay planted throughout.

Repair precision: The tail is the only clear moving silhouette. Show one visibly readable but compact continuous wag with a small, even tail-tip increment between each neighboring cell, including cell 6 back to cell 1. Do not switch tail shapes or positions abruptly. Keep the open pleased mouth, planted paws, and body outline nearly unchanged.
