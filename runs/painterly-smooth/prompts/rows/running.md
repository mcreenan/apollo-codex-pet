Create one horizontal animation strip for Codex pet `apollo-painterly`, state `running`.

Use the attached canonical base for identity. Use the attached layout guide only for slot count, spacing, centering, and padding; do not draw the guide.

Output exactly 6 full-body frames in one left-to-right row on flat pure user-selected #00B140. Treat the row as 6 invisible equal-width slots: one centered complete pose per slot, evenly spaced, with no overlap, clipping, empty slots, labels, or borders.

Identity: same pet in every frame: White/creme coat, brown saddle patches on back and sides, brown face mask with clean white central blaze from muzzle to forehead, brown ears, white chest/legs/belly, dark nose, warm brown eyes, friendly slightly goofy expression.. Preserve silhouette, face, proportions, markings, palette, material, style, and props.
Style: Pet-safe sprite: compact full-body mascot, readable in a 192x208 cell, clear silhouette, simple face, stable palette/materials, and crisp edges for chroma-key extraction. Style `painterly`: Painterly mascot with simplified brush texture, readable forms, stable palette, and enough edge clarity for clean extraction. User style notes: keep the exact style, palette, proportions, and markings of the canonical base image across every row..
Animation continuity: keep apparent pet scale and baseline stable within the row unless the state itself intentionally changes vertical position, such as `jumping`. Move the pose within the slot instead of redrawing the pet larger or smaller frame to frame.

Smooth continuous-loop contract: Create six consecutive in-between moments of one seamless cyclic motion, not six unrelated running poses. Frame 6 must flow directly back into frame 1. Keep the same camera, scale, body position, and center footing; adjacent frames must look like the next instant of the same phase-ordered gait, with no scale pops or baseline shifts.

Pose-family anchor: Use the attached current-pose-family image only to keep Apollo facing the camera in exactly this busy-trot stance family.

Motion brief: A non-directional busy trot in place, facing the camera. Show one coherent six-phase trot cycle: legs progress through gait phases in order and body bobs slightly with the gait. This row alone may have real leg motion, but do not travel or use speed lines, dust, or literal ground.

Repair priority: The previous strip drifted away from the current-pose-family anchor. Match the anchor's exact front-facing body stance, silhouette, and level of sitting/standing before animating; then change only the legs through a subtle, phase-ordered in-place trot and a tiny body bob. Do not change the torso posture, camera, or body height between frames.

State action: Working loop: focused active-task processing, thinking, typing, scanning, or effortful concentration; not literal foot-running, jogging, sprinting, treadmill motion, raised knees, long steps, pumping arms, or directional travel.

State requirements:
- Show the pet actively working or processing, as if running a task: focused posture, busy hands or paws, purposeful bobbing, thinking motion, tool or prop motion only if already part of the pet identity, or other non-locomotion activity.
- Do not show literal foot-running, jogging, sprinting, treadmill motion, raised knees, long steps, pumping arms, directional travel, speed lines, dust clouds, floor shadows, motion trails, or detached motion effects.

Clean extraction: crisp opaque edges, safe padding, no scenery, text, guide marks, checkerboard, shadows, glows, motion blur, speed lines, dust, detached effects, stray pixels, or chroma-key colors inside the pet.
