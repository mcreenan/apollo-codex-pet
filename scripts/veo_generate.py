#!/usr/bin/env python3
"""Generate a video with the Veo API (Gemini API, paid tier).

Image-to-video from a reference first frame + prompt, long-running
operation with polling, saves the MP4. Requires GEMINI_API_KEY.

Usage: veo_generate.py <prompt.txt> <reference.png> <out.mp4>
       [--model veo-3.1-fast-generate-preview] [--seconds 8]
       [--aspect 9:16] [--resolution 720p]
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request

BASE = "https://generativelanguage.googleapis.com/v1beta"


def call(method, url, key, body=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("x-goog-api-key", key)
    data = None
    if body is not None:
        req.add_header("Content-Type", "application/json")
        data = json.dumps(body).encode()
    try:
        with urllib.request.urlopen(req, data) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on {url}:\n{e.read().decode()[:2000]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt_file")
    ap.add_argument("reference")
    ap.add_argument("out")
    ap.add_argument("--model", default="veo-3.1-fast-generate-preview")
    ap.add_argument("--seconds", type=int, default=8)
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--resolution", default="720p")
    args = ap.parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY is not set")
    prompt = open(args.prompt_file).read().strip()
    img = base64.b64encode(open(args.reference, "rb").read()).decode()

    body = {
        "instances": [{
            "prompt": prompt,
            "image": {"bytesBase64Encoded": img, "mimeType": "image/png"},
        }],
        "parameters": {
            "aspectRatio": args.aspect,
            "resolution": args.resolution,
            "durationSeconds": args.seconds,
        },
    }
    op = call("POST", f"{BASE}/models/{args.model}:predictLongRunning",
              key, body)
    name = op.get("name")
    if not name:
        sys.exit(f"unexpected response:\n{json.dumps(op, indent=2)[:2000]}")
    print("operation:", name)

    while True:
        time.sleep(10)
        op = call("GET", f"{BASE}/{name}", key)
        if op.get("done"):
            break
        print("  ...generating")
    if "error" in op:
        sys.exit(f"generation failed:\n{json.dumps(op['error'], indent=2)}")

    resp = op.get("response", {})
    samples = (resp.get("generateVideoResponse", {}).get("generatedSamples")
               or resp.get("generatedVideos") or [])
    if not samples:
        sys.exit(f"no video in response:\n{json.dumps(resp, indent=2)[:2000]}")
    video = samples[0].get("video", samples[0])
    if video.get("bytesBase64Encoded"):
        blob = base64.b64decode(video["bytesBase64Encoded"])
    else:
        uri = video.get("uri")
        req = urllib.request.Request(uri)
        req.add_header("x-goog-api-key", key)
        with urllib.request.urlopen(req) as r:
            blob = r.read()
    with open(args.out, "wb") as f:
        f.write(blob)
    print(f"saved {args.out} ({len(blob) / 1e6:.1f}MB)")


if __name__ == "__main__":
    main()
