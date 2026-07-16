Create one horizontal animation strip for Codex pet `apollo-painterly`, state `waiting`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure user-selected #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `painterly`: Painterly mascot with simplified brush texture, readable forms, stable palette, and enough edge clarity for clean extraction. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

Smooth continuous-loop contract: Create six consecutive in-between moments of one seamless cyclic motion, not six distinct poses. Frame 6 must flow directly back into frame 1. Keep the same camera, scale, body position, and footing in every frame; adjacent frames must look nearly identical, as the next instant of the same motion. Change only the stated micro-motion; do not introduce pose changes, scale pops, or baseline shifts.

Pose-family anchor: Use the attached current-pose-family image only to keep Apollo in exactly this attentive sitting stance.

Motion brief: One forepaw remains slightly raised in every frame; never lower it. The raised paw bobs only a few pixels, the head tilts a few degrees gently to one side and returns over the loop, and ears stay perked. Nothing else moves.

Repair priority: The previous attempt made head and body changes too distinct. Make this replacement far more subtle: treat each adjacent pair as a nearly identical next instant. Keep torso and all non-mentioned parts pixel-stable in apparent placement; only a tiny paw bob and a very slight incremental head-angle change are permitted.

State action: Needs-input loop: expectant asking pose for approval, help, or user input.

State requirements:
- Show that Codex needs approval, help, or user input through an expectant asking pose.
- Keep the motion patient and readable, without turning it into ordinary idle or review.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.
