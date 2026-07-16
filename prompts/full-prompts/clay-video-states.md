# Clay — Flow/Veo prompts for all four Orca states

Same recipe for every state: Flow "Frames" mode, Start frame =
`variants/apollo-clay-video-ref-16x9.png` (must match the session's 16:9
aspect), 8s, no End frame. Download Original, drop at
`runs/clay-video/<state>.mp4`, then:

```
python scripts/video_rows.py runs/clay-video/<state>.mp4 \
  runs/clay-video/cells/<state> --gif qa/clay-video-<state>.gif
```

Shared boilerplate (identical in each prompt): the first two and last two
sentences pin identity, camera, and background.

## idle

The exact dog from the first frame — the same sculpted clay figurine with
the same markings, proportions, pose, and position — sits perfectly still
on the same flat, uniform green background. Locked-off static camera, no
camera motion, no zoom, no cuts. Calm idle motion only: slow gentle
breathing, one soft blink, small ear twitches, a slow relaxed tail sway.
The paws never move or lift; the dog never changes position. The dog's
entire body, including the full tail, stays completely inside the frame
at all times. The background stays exactly the same flat solid green the
whole time — no shadows, no gradients, no floor plane. No other objects,
no text, no watermark.

## waiting

The exact dog from the first frame — the same sculpted clay figurine with
the same markings, proportions, pose, and position — sits perfectly still
on the same flat, uniform green background. Locked-off static camera, no
camera motion, no zoom, no cuts. Expectant waiting motion only: the dog
tilts its head curiously to one side, then slowly to the other, ears
perked and swiveling attentively, eyes fixed on the viewer, with gentle
breathing. The paws never move or lift; the dog never changes position.
The dog's entire body, including the full tail, stays completely inside
the frame at all times. The background stays exactly the same flat solid
green the whole time — no shadows, no gradients, no floor plane. No other
objects, no text, no watermark.

## running (work)

The exact dog from the first frame — the same sculpted clay figurine with
the same markings, proportions, pose, and position — sits perfectly still
on the same flat, uniform green background. Locked-off static camera, no
camera motion, no zoom, no cuts. Busy, focused motion only: the dog looks
quickly left, then right, then straight ahead as if intently tracking
something, ears flicking alertly, quick attentive breathing, tail giving
short brisk wags. The paws never move or lift; the dog never changes
position. The dog's entire body, including the full tail, stays
completely inside the frame at all times. The background stays exactly
the same flat solid green the whole time — no shadows, no gradients, no
floor plane. No other objects, no text, no watermark.

## review

The exact dog from the first frame — the same sculpted clay figurine with
the same markings, proportions, pose, and position — sits perfectly still
on the same flat, uniform green background. Locked-off static camera, no
camera motion, no zoom, no cuts. Proud, happy motion only: the dog sits
up a little taller with its chest out, mouth open in a pleased smile,
tail wagging enthusiastically side to side, one happy blink, ears up.
The paws never move or lift; the dog never changes position. The dog's
entire body, including the full tail, stays completely inside the frame
at all times. The background stays exactly the same flat solid green the
whole time — no shadows, no gradients, no floor plane. No other objects,
no text, no watermark.
