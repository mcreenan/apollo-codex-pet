Create one horizontal animation strip for Codex pet `apollo-pixel`, state `running`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure user-selected #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `pixel`: Pixel-art-adjacent digital mascot with a chunky silhouette, simple dark outline, limited palette, flat cel shading, and visible stepped edges. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

State action: Working loop: focused active-task processing, thinking, typing, scanning, or effortful concentration; not literal foot-running, jogging, sprinting, treadmill motion, raised knees, long steps, pumping arms, or directional travel.

State requirements:
- Show the pet actively working or processing, as if running a task: focused posture, busy hands or paws, purposeful bobbing, thinking motion, tool or prop motion only if already part of the pet identity, or other non-locomotion activity.
- Do not show literal foot-running, jogging, sprinting, treadmill motion, raised knees, long steps, pumping arms, directional travel, speed lines, dust clouds, floor shadows, motion trails, or detached motion effects.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.

Smooth-loop contract: Make six consecutive in-between phases of one seamless continuous 6-phase gait cycle, not six unrelated running poses. Use the current pose-family anchor exactly: a non-directional busy trot in place, facing the camera. Keep camera, scale, overall body placement, and baseline stable; legs alone progress through coherent trot phases in order and the body bobs slightly with the gait. Adjacent frames must read as the next instant and frame 6 must flow directly into frame 1. This is the sole allowed real leg motion; no speed lines, dust, literal ground, or directional travel.

ANCHOR-LOCK REPAIR PRIORITY: The supplied pose-family anchor visibly shows Apollo in a focused side/three-quarter work stance, not a front-facing seated pose. Match that anchor's camera angle, crouched/leaning silhouette, leg placement, and tail position exactly. Animate only a coherent subtle in-place six-phase busy gait appropriate to that anchored stance; no camera turn, no new front-facing pose, no travel.
