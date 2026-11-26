"""Entry for make.fun bounty "Sum up 25 November's world news in one image".

The finished front page is stored in this repository as entry.png.
This program's only job is to deliver that image as the entry output:
it reads entry.png, checks it is a valid PNG within the bounty limits
(1024x1024 or smaller, 1 MiB or smaller), and writes an exact copy to
entry.png inside the output directory.

Before copying, it walks the whole PNG chunk structure: it verifies the
IHDR chunk (length 13, correct CRC, sane bit depth and colour type),
checks the CRC of every chunk, and refuses a file that is truncated,
has trailing garbage after IEND, or is missing its IEND chunk. That
way a damaged or half-written entry.png fails loudly here instead of
being submitted as a broken image.

Standard library only. No network access, no randomness, no
command-line arguments: every run produces the same output bytes.

Usage:
    MAKEFUN_OUTPUT_DIR=./output python3 main.py
"""

import os
import struct
import sys
import zlib

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_SIZE = 1 << 20          # 1 MiB
MAX_SIDE = 1024             # pixels
VALID_BIT_DEPTHS = (1, 2, 4, 8, 16)
VALID_COLOUR_TYPES = (0, 2, 3, 4, 6)


def load_source():
    """Read entry.png next to this file and return its bytes."""
    base = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(base, "entry.png"), "rb") as handle:
        return handle.read()


def _fail(message):
    sys.exit(f"error: {message}")


def check_image(data):
    """Validate the PNG chunk by chunk; return (width, height)."""
    if data[: len(PNG_MAGIC)] != PNG_MAGIC:
        _fail("entry.png does not start with a PNG signature")
    if len(data) > MAX_SIZE:
        _fail(
            f"entry.png is {len(data)} bytes, "
            f"over the {MAX_SIZE} byte limit"
        )

    # Walk the chunk stream: [length:4][type:4][data:length][crc:4] ...
    # Every chunk must fit inside the file, its CRC must match, and the
    # stream must end exactly at an IEND chunk with nothing after it.
    pos = len(PNG_MAGIC)
    width = height = None
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            _fail("entry.png is truncated inside a chunk header")
        length, chunk_type = struct.unpack_from(">I4s", data, offset=pos)
        if pos + 12 + length > len(data):
            _fail(f"entry.png is truncated inside the {chunk_type!r} chunk")
        chunk_data = data[pos + 8: pos + 8 + length]
        stored_crc, = struct.unpack_from(">I", data, offset=pos + 8 + length)
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            _fail(f"entry.png has a bad CRC in the {chunk_type!r} chunk")
        if chunk_type == b"IHDR":
            if width is not None:
                _fail("entry.png has more than one IHDR chunk")
            if length != 13:
                _fail("entry.png has an IHDR chunk of the wrong length")
            width, height, bit_depth, colour_type = struct.unpack_from(
                ">IIBB", chunk_data, offset=0
            )
            if bit_depth not in VALID_BIT_DEPTHS:
                _fail(f"entry.png has an unsupported bit depth {bit_depth}")
            if colour_type not in VALID_COLOUR_TYPES:
                _fail(f"entry.png has an unsupported colour type {colour_type}")
            if width > MAX_SIDE or height > MAX_SIDE:
                _fail(
                    f"image is {width}x{height}, "
                    f"over the {MAX_SIDE}x{MAX_SIDE} limit"
                )
        if chunk_type == b"IEND":
            seen_iend = True
            if pos + 12 + length != len(data):
                _fail("entry.png has trailing data after the IEND chunk")
            break
        pos += 12 + length
    if width is None:
        _fail("entry.png has no IHDR chunk")
    if not seen_iend:
        _fail("entry.png is missing its IEND chunk")
    return width, height


def write_output(data):
    """Write data to entry.png in the output directory and verify it."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    with open(out_path, "wb") as handle:
        handle.write(data)
    with open(out_path, "rb") as handle:
        if handle.read() != data:
            sys.exit("error: written file differs from entry.png")
    return out_path


def main():
    data = load_source()
    width, height = check_image(data)
    out_path = write_output(data)
    print(f"wrote {out_path}: {width}x{height}, {len(data)} bytes")


if __name__ == "__main__":
    main()
