Create one horizontal animation strip for Codex pet `apollo-pixel`, state `waiting`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure user-selected #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `pixel`: Pixel-art-adjacent digital mascot with a chunky silhouette, simple dark outline, limited palette, flat cel shading, and visible stepped edges. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Needs-input loop: expectant asking pose for approval, help, or user input.

State requirements:
- Show that Codex needs approval, help, or user input through an expectant asking pose.
- Keep the motion patient and readable, without turning it into ordinary idle or review.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Smooth-loop contract: Make six consecutive in-between moments of one seamless continuous loop, not six distinct poses. Keep identical camera, scale, body placement, footing, and silhouette across all frames; adjacent frames must read as the next instant, and frame 6 must flow directly into frame 1. Use the current pose-family anchor exactly: Apollo sits attentive with one forepaw slightly raised in every frame, never lowered. That already-raised paw bobs only a few pixels; the head gently tilts a few degrees to one side and returns over the loop; ears remain perked. Nothing else moves.

ANCHOR-LOCK REPAIR PRIORITY: The supplied pose-family anchor visibly shows Apollo standing attentive in side/three-quarter view with one forepaw raised. Match that standing anchor's camera, leg placement, tail position, and silhouette exactly; do not turn Apollo into a seated or front-facing pose. The already-raised paw remains raised every frame and only bobs a few pixels; retain the gentle head tilt and perked ears.
