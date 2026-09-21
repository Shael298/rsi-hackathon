#!/usr/bin/env python3
"""List every output file with its columns / keys / types so it can be compared to the task spec.

    python check_outputs.py /app/output

Flags: missing dir, empty files, NaN / inf values, unparsable files.
Runs offline with only the standard library, plus pandas if available.
"""
import json
import math
import os
import sys


def _walk(d):
    for root, _dirs, files in os.walk(d):
        for f in sorted(files):
            yield os.path.join(root, f)


def _json_types(v, depth=0):
    if isinstance(v, dict):
        if depth >= 2:
            return "object"
        return {k: _json_types(x, depth + 1) for k, x in v.items()}
    if isinstance(v, list):
        inner = set()
        for x in v[:20]:
            if isinstance(x, (dict, list)):
                inner.add(type(x).__name__)
            else:
                inner.add(str(_json_types(x, depth + 1)))
        return "list[%s](%d)" % (",".join(sorted(inner)) or "empty", len(v))
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return "FLOAT-NAN/INF!!"
        return "float"
    if v is None:
        return "null"
    return type(v).__name__


def check_json(p):
    with open(p, encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)
    print("  keys/types: " + json.dumps(_json_types(data)))
    if "NaN" in raw or "Infinity" in raw:
        print("  !! JSON contains NaN/Infinity literal (invalid for strict parsers)")


def check_csv(p):
    try:
        import pandas as pd
    except ImportError:
        with open(p, encoding="utf-8") as f:
            header = f.readline().rstrip("\n")
            n = sum(1 for _ in f)
        print("  columns: %s" % header.split(","))
        print("  rows: %d" % n)
        return
    df = pd.read_csv(p)
    print("  columns (%d): %s" % (len(df.columns), list(df.columns)))
    print("  rows: %d" % len(df))
    na = df.isna().sum()
    na = na[na > 0]
    if len(na):
        print("  !! NaN counts: %s" % na.to_dict())
    num = df.select_dtypes("number")
    if num.size and ((num == float("inf")) | (num == float("-inf"))).any().any():
        print("  !! inf values present")
    if len(df) and len(df.columns):
        print("  first row: %s" % df.iloc[0].to_dict())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    d = sys.argv[1]
    if not os.path.isdir(d):
        print("!! output dir missing: %s" % d)
        return 1
    files = list(_walk(d))
    if not files:
        print("!! output dir is empty: %s" % d)
        return 1
    bad = 0
    for p in files:
        size = os.path.getsize(p)
        print("\n== %s (%d bytes)" % (p, size))
        if size == 0:
            print("  !! EMPTY FILE")
            bad += 1
            continue
        try:
            if p.endswith(".json"):
                check_json(p)
            elif p.endswith(".csv"):
                check_csv(p)
            else:
                with open(p, "rb") as f:
                    head = f.read(200)
                print("  head: %r" % head)
        except Exception as e:  # keep going; report every file
            print("  !! could not parse: %s: %s" % (type(e).__name__, e))
            bad += 1
    print("\n%d files checked, %d problems" % (len(files), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
