"""make.fun entry: Sum up 25 November's world news in one image.

The program copies the finished image the repository holds
(entry.png) to /output/entry.png, byte for byte -- the simplest
program the make.fun skill describes for an image bounty. It uses
only the Python standard library, makes no network calls, and is
fully deterministic: every run writes the exact same bytes.

The image itself was rendered locally with Pillow by
build/render_image.py (kept in the repo for transparency); that
script is not run by the entry.

Run locally:
    MAKEFUN_OUTPUT_DIR=./output python3 main.py
"""

import os
import struct
import sys

SOURCE = "entry.png"
MAX_BYTES = 1048576  # 1 MiB
MAX_DIMENSION = 1024


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE)
    with open(source_path, "rb") as f:
        data = f.read()

    # Validate: a real PNG, 1024x1024 at most, 1 MiB at most.
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: entry.png is {len(data)} bytes, over the "
              f"{MAX_BYTES} byte limit", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        print(f"error: image is {width}x{height}, over the "
              f"{MAX_DIMENSION}x{MAX_DIMENSION} limit", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)

    # Read it back and confirm the copy is byte-identical.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("error: written file differs from entry.png",
              file=sys.stderr)
        return 1

    print(f"wrote {path}: {width}x{height}, {len(written)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
