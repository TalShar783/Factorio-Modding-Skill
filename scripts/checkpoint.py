#!/usr/bin/env python3
"""Git checkpoint before risky changes: stage everything, commit, tag. Local only - never pushes.
Usage: python checkpoint.py [message]
Restore later with: git reset --hard <tag>  (or git checkout <tag> -- path).
This is the ONE sanctioned git wrapper; all other git use is plain git commands (see SKILL.md).
"""
import subprocess, sys, time

def run(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()

if __name__ == "__main__":
    code, _ = run("rev-parse", "--is-inside-work-tree")
    if code != 0:
        sys.exit("Not a git repository. Refusing to act.")
    msg = " ".join(sys.argv[1:]) or "checkpoint"
    tag = "checkpoint-" + time.strftime("%Y%m%d-%H%M%S")
    run("add", "-A")
    code, out = run("commit", "-m", f"checkpoint: {msg}")
    if code != 0 and "nothing to commit" not in out:
        sys.exit(f"commit failed: {out}")
    if code != 0:
        print("Nothing to commit; no tag created.")
        sys.exit(0)
    code, out = run("tag", tag)
    if code != 0:
        sys.exit(f"tag failed: {out}")
    print(f"Committed and tagged {tag}")
