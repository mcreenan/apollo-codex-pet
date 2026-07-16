# Task: Generate 3 style variants of a Codex pet base image for Apollo the dog

First read and follow the installed image generation skill at `~/.codex/skills/.system/imagegen/SKILL.md`. Use $imagegen for ALL image generation. Do not use any other image generation path.

## Subject: Apollo

A medium-sized mutt. Mostly white/creme fur. Brown saddle patches on his back and sides. Brown face mask covering ears and cheeks, with a clean white blaze running up the middle of his face from muzzle to forehead. Brown ears. White chest, legs, belly, and underside. Dark nose, warm brown eyes. Friendly, alert, slightly goofy personality (tongue sometimes out).

## Reference photos (attach ALL THREE to every generation as identity grounding)

- refs/IMG_4195.png — full body, sitting, facing camera; shows markings layout
- refs/IMG_0887.png — face close-up; shows mask and blaze detail
- refs/IMG_9501.png — full body side profile; shows saddle patch pattern

## Generate exactly 3 images, one per style

For each style below, generate ONE image of Apollo as a Codex pet base:

1. **pixel** — chunky retro pixel-art sprite style, crisp pixels, limited palette
2. **plush** — soft plush/stuffed-animal toy look, rounded, huggable, gentle fabric texture
3. **sticker** — bold die-cut sticker style with clean thick outline, flat shading, playful

## Requirements for every variant (these are Codex pet base images)

- ONE single centered full-body pet character, whole body visible, compact silhouette
- Must read clearly when scaled down to 192x208 pixels
- Flat solid uniform chroma-key green background (#00B140 or similar pure green), edge-to-edge, nothing else in the scene
- Identity must match the reference photos: white/creme body, brown saddle patches, brown face mask with white central blaze, brown ears, white chest and legs
- Friendly expression, standing or sitting neutral idle pose
- NO text, labels, logos, shadows, glows, floor, scenery, props, or detached effects

## Output

Copy each selected final image to:

- variants/apollo-pixel.png
- variants/apollo-plush.png
- variants/apollo-sticker.png

After copying, delete the originals from ~/.codex/generated_images if they live there.

Final response: return exactly the three output file paths, one per line, plus a one-sentence QA note per variant confirming identity match and clean chroma background.
