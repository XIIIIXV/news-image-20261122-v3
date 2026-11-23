#!/usr/bin/env python3
"""Entry point for news-image-20261122-v3 (round 3 rebuild).

Copies the pre-rendered entry.png into $MAKEFUN_OUTPUT_DIR.
Renders nothing and writes nothing into this repository directory,
so it runs cleanly on a read-only filesystem. The entry image is
drawn ahead of time by gen_22nov_v3.py; this file only moves bytes.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch", file=sys.stderr)
        return 1
    print("copied entry.png (%d bytes) to %s"
          % (os.path.getsize(dst), out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
