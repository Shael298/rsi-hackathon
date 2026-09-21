#!/usr/bin/env python3
"""run.py - run solve.py, then list every output file with columns / keys / types, in ONE tool call.

    python /harbor/skills/stbench-skill/run.py [/app/solve.py] [/app/output]

Prints the last lines of solve.py's output, then the check_outputs.py report.
Exit code = solve.py's exit code (non-zero means fix the traceback first).
"""

from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    solve = sys.argv[1] if len(sys.argv) > 1 else "/app/solve.py"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "/app/output"
    r = subprocess.run([sys.executable, solve], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(solve)))
    tail = (r.stdout or "")[-3000:]
    print(tail)
    if r.returncode != 0:
        print("---- solve.py FAILED (exit %d), stderr tail ----" % r.returncode)
        print((r.stderr or "")[-3000:])
        return r.returncode
    print("---- outputs ----")
    c = subprocess.run([sys.executable, os.path.join(HERE, "check_outputs.py"), out_dir], capture_output=True, text=True)
    print((c.stdout or "")[-6000:])
    if c.stderr:
        print((c.stderr or "")[-1000:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
