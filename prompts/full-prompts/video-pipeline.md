# Video pipeline — one style, four states, start to bundle

The animation frames come from short Veo clips generated in Google Flow
(labs.google/flow); everything after the download is local and
deterministic. This replaced keyframe interpolation (2D warps of 3D
articulation read as morphing) and procedural rigging (edge/lighting
artifacts): video gives real articulated motion with frame-to-frame
coherence built in.

## 1. Generate in Flow (manual, per state)

Session settings: **Video → Frames mode → 16:9 → 8s** (x2 outputs to
pick from; the Flash model tier is usually fine).

- Start frame: `variants/apollo-<style>-video-ref-16x9.png`
  (rebuild any time with `python scripts/video_ref.py
  variants/apollo-<style>.png variants/apollo-<style>-video-ref-16x9.png`)
- End frame: the SAME image for idle / waiting / review — the clip then
  departs from and returns to identical pixels, which makes the loop
  seam nearly perfect. Leave End EMPTY for running: the loop is cut from
  the steady trot in the middle instead.
- Prompts: `prompts/full-prompts/<style>-video-states.md` (pose-aware,
  generated per style).

The start frame's aspect must exactly match the session's aspect —
any mismatch makes Flow crop/rotate the image, and a transformed start
frame stops pinning pixels (the dog gets re-rendered off-model).

Judging a take, in priority order: feet stay planted (no sliding or
repositioning); background stays flat green; motion is calm and dog-like;
identity matches the reference. Frame 0 should be literally the
reference image — if it isn't, the mode/slots are wrong.

## 2. Cut each clip into a 48-frame loop

Save downloads as `runs/<style>-video/<state>.mp4`
(state = idle | waiting | running | review), then:

```
python scripts/video_rows.py runs/<style>-video/<state>.mp4 \
  runs/<style>-video/cells/<state> --gif qa/<style>-video-<state>.gif
```

Add `--skip 2.5` for running clips that begin with a stand-up
transition. The cutter keys the background (auto-detected color), drops
disconnected blobs (Flow's watermark), despills key-colored specks off
the dog, finds the best loop window, and emits 48 placed cells plus a
preview GIF. Sanity numbers it prints: seam diff well under ~1 is a
clean wrap.

## 3. Author, preview, and build

After eyeballing the per-state GIFs:

```
python scripts/author_video_rows.py <style>
```

Authors every state with complete cells (partial is fine), writes 6 loop
samples per row into the native sheet, renders exact-playback previews
to `qa/previews-<style>-video/`, and rebuilds
`dist/codex-pet-bundles/Apollo-<style>.codex-pet`.
