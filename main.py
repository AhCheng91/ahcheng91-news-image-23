#!/usr/bin/env python3
"""Copy the entry.png beside this script into $MAKEFUN_OUTPUT_DIR and verify it."""
import hashlib
import os
import shutil
import sys

NAME = "entry.png"


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    """Copy the picture, print its size and sha256, and exit 1 on a hash mismatch."""
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_dir = os.path.abspath(os.path.expanduser(out_dir))
    src_size = os.path.getsize(src)
    print("entry: %s %d bytes" % (NAME, src_size), flush=True)
    if src_size >= 1048576:
        print("too large", file=sys.stderr, flush=True)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, NAME)
    shutil.copyfile(src, dst)
    print("%d bytes -> %s" % (os.path.getsize(dst), dst))
    written, original = digest(dst), digest(src)
    print("sha256 %s" % written)
    if written != original:
        print("mismatch: %s" % original, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
