#!/usr/bin/env python3
"""Copy the entry.png that sits beside this script to $MAKEFUN_OUTPUT_DIR."""
import hashlib
import os
import shutil
import sys

SRC_NAME = "entry.png"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(repo_root, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    out_dir = os.path.abspath(os.path.expanduser(out_dir))
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, SRC_NAME)

    shutil.copyfile(src, dst)

    size = os.path.getsize(dst)
    print("%d bytes written to %s" % (size, dst))

    src_hash = sha256_of(src)
    dst_hash = sha256_of(dst)
    print("sha256 %s" % dst_hash)
    if src_hash != dst_hash:
        sys.stderr.write("hash mismatch: %s != %s\n" % (src_hash, dst_hash))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
