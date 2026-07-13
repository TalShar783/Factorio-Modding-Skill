#!/usr/bin/env python3
"""Look up runtime API members with the REAL positional parameter order resolved.
Usage: python query_api.py runtime-api.json LuaEntity.add_fluid   # method/attribute
       python query_api.py runtime-api.json on_built_entity       # event
       python query_api.py runtime-api.json fluid                 # substring search fallback
Replaces the pretty-print-then-grep workflow. The 'parameters' arrays in runtime-api.json are
alphabetical; this prints them sorted by their 'order' field (the actual call order).
"""
import json, sys

def load_json(path):
    import json, os, sys
    if not os.path.isfile(path):
        sys.exit(f"{path} not found - run 'python scripts/fetch_api_jsons.py' first (JSONs land in api/)")
    return json.load(open(path, encoding="utf-8"))

def show_method(cls, m):
    ps = sorted(m.get("parameters", []) or [], key=lambda p: p.get("order", 0))
    # takes_table lives under m["format"] in current JSONs; fall back to the old
    # top-level field for older API dumps.
    fmt = m.get("format") or {}
    takes_table = fmt.get("takes_table", m.get("takes_table"))
    if takes_table:
        style = "single named-table argument" + (" (table optional)" if fmt.get("table_optional") else "")
    else:
        style = "positional"
    print(f"{cls}.{m['name']}  [{style}]")
    for p in ps:
        t = p.get("type")
        t = t if isinstance(t, str) else (t.get("complex_type", "complex") if isinstance(t, dict) else "?")
        opt = " (optional)" if p.get("optional") else ""
        print(f"  {p.get('order', '?')}: {p['name']} : {t}{opt}")
    r = m.get("return_values") or []
    if r:
        print("  returns:", ", ".join(str((rv.get('type') if isinstance(rv.get('type'), str) else 'complex')) for rv in r))

def show_attr(cls, a):
    # Current JSONs express readability/writability via presence of read_type/
    # write_type (and carry no top-level "type"); older dumps used read/write
    # booleans plus a "type". Support both.
    readable = a.get("read_type") is not None or a.get("read", False)
    writable = a.get("write_type") is not None or a.get("write", False)
    t = a.get("type") or a.get("read_type") or a.get("write_type") or "complex"
    t = t if isinstance(t, str) else "complex"
    rw = ("R" if readable else "") + ("W" if writable else "")
    print(f"{cls}.{a['name']} : {t}  [{rw}]")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    api = load_json(sys.argv[1])
    q = sys.argv[2]
    classes = {c["name"]: c for c in api.get("classes", [])}
    if "." in q:
        cname, mname = q.split(".", 1)
        c = classes.get(cname) or sys.exit(f"unknown class: {cname}")
        for m in c.get("methods", []) or []:
            if m["name"] == mname:
                show_method(cname, m); sys.exit()
        for a in c.get("attributes", []) or []:
            if a["name"] == mname:
                show_attr(cname, a); sys.exit()
        sys.exit(f"{cname} has no member {mname} - it does not exist in 2.x")
    for e in api.get("events", []) or []:
        if e["name"] == q:
            print(f"event {q}  filter: {e.get('filter') or 'none'}")
            for d in sorted(e.get("data", []) or [], key=lambda x: x.get("order", 0)):
                t = d.get("type"); t = t if isinstance(t, str) else "complex"
                print(f"  {d['name']} : {t}{' (optional)' if d.get('optional') else ''}")
            sys.exit()
    if q in classes:
        c = classes[q]
        print(f"class {q}: {len(c.get('methods', []) or [])} methods, {len(c.get('attributes', []) or [])} attributes")
        for m in c.get("methods", []) or []: print(f"  method {m['name']}")
        for a in c.get("attributes", []) or []: print(f"  attr   {a['name']}")
        sys.exit()
    ql = q.lower()  # substring fallback
    for c in api.get("classes", []) or []:
        for m in c.get("methods", []) or []:
            if ql in m["name"].lower(): print(f"{c['name']}.{m['name']}()")
        for a in c.get("attributes", []) or []:
            if ql in a["name"].lower(): print(f"{c['name']}.{a['name']}")
    for e in api.get("events", []) or []:
        if ql in e["name"].lower(): print(f"event {e['name']}")
