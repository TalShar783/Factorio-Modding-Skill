#!/usr/bin/env python3
"""ONE-SHOT scan of factorio-current.log for mod/script errors. Reads the file once, closes it, exits.
Usage: python scan_factorio_log.py [path-to-log]
Default path: %APPDATA%/Factorio/factorio-current.log (Windows), ~/.factorio/factorio-current.log otherwise.
Prints matching lines with 2 lines of trailing context; exit code 1 if any errors found.

AGENT CONTRACT:
- Run only when the user asks for a log check, or immediately after an instructed test launch fails.
- NEVER tail/watch/follow the log or hold it open (no tail -f, Get-Content -Wait, editor opens,
  polling loops). An open handle prevents the user from starting a new Factorio session.
- If you need fresh results, ask the user to relaunch, then run this once.
"""
import os, re, sys

PAT = re.compile(r"error|failed to load|exception|desync|cannot be loaded|Unknown key|"
                 r"doesn't contain key|out of bounds|attempt to (index|call|compare)", re.I)

def default_path():
    if os.name == "nt":
        return os.path.join(os.environ.get("APPDATA", ""), "Factorio", "factorio-current.log")
    return os.path.expanduser("~/.factorio/factorio-current.log")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else default_path()
    if not os.path.isfile(path):
        sys.exit(f"log not found: {path}")
    with open(path, encoding="utf-8", errors="replace") as f:  # read once; handle closed before any output
        lines = f.read().splitlines()
    hits = 0
    i = 0
    while i < len(lines):
        if PAT.search(lines[i]):
            hits += 1
            for j in range(i, min(i + 3, len(lines))):
                print(f"{j + 1}: {lines[j]}")
            print("---")
            i += 3
        else:
            i += 1
    print(f"{hits} error region(s) in {path}")
    sys.exit(1 if hits else 0)
