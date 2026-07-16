# Clay idle — video generation spec (Sora / Veo)

Goal: a short video of the clay Apollo idling in place, to be cut into a
48-frame Orca loop by `scripts/video_rows.py`.

## Inputs
- First-frame / reference image: `runs/clay-smooth/references/idle-video-ref.png`
  (720x1280, the clay idle master centered on flat chroma green #00B140)

## Settings
- Sora: model `sora-2`, size `720x1280`, seconds `8` (more loop-window choices than 4)
- Veo: `veo-3.1`, image-to-video with the reference as first frame, 8s

## Prompt

A claymation-style Jack Russell terrier figurine sits perfectly centered
on a flat, uniform chroma-green background (#00B140). Locked-off static
camera, no camera motion, no zoom, no cuts. The dog stays planted in
exactly the same spot for the entire video: calm idle motion only — slow
gentle breathing, one soft blink, small ear twitches, a slow relaxed tail
sway. The dog's paws never move or lift. Soft even studio lighting with
absolutely no shadows, reflections, or gradients on the green background;
the background stays one flat solid green at all times. No other objects,
no text, no watermark. The style is smooth sculpted clay with visible
subtle fingerprint texture, matching the reference image exactly:
same markings, same proportions, same pose.

## After generation
```
python scripts/video_rows.py <video.mp4> runs/clay-video/cells/idle \
  --gif qa/clay-video-idle.gif
```
Then eyeball the GIF; if good, author the cells into the sheet row and
smooth-rows.json (literal 48-frame track, no rig/interp) and rebuild.
