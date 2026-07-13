#!/usr/bin/env python3
"""Find prototype classes having ALL named properties (inheritance-resolved).
Usage: python find_prototypes_by_capability.py prototype-api.json --has fluid_box energy_source
       python find_prototypes_by_capability.py prototype-api.json --list-props AssemblingMachinePrototype
Answers "which native type already does most of this?" mechanically (SKILL.md paradigm 1).
Property names must be exact API names (e.g. fluid_box vs fluid_boxes differ by class) -
if unsure, --list-props a nearby class first.
"""
import argparse, json, os, sys

def load_json(path):
    import json, os, sys
    if not os.path.isfile(path):
        sys.exit(f"{path} not found - run 'python scripts/fetch_api_jsons.py' first (JSONs land in api/)")
    return json.load(open(path, encoding="utf-8"))


def all_props(name, by_name, cache):
    if name in cache:
        return cache[name]
    p = by_name.get(name)
    if not p:
        return {}
    props = dict(all_props(p.get("parent"), by_name, cache)) if p.get("parent") else {}
    for pr in p.get("properties", []) or []:
        props[pr["name"]] = pr
    cache[name] = props
    return props

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("api_json")
    ap.add_argument("--has", nargs="+", help="required property names (all must be present)")
    ap.add_argument("--list-props", help="list all (inherited) properties of one class")
    a = ap.parse_args()
    api = load_json(a.api_json)
    by_name = {p["name"]: p for p in api["prototypes"]}
    cache = {}
    if a.list_props:
        props = all_props(a.list_props, by_name, cache)
        if not props:
            sys.exit(f"unknown class: {a.list_props}")
        for n in sorted(props):
            opt = " (optional)" if props[n].get("optional") else ""
            print(f"{n}{opt}")
    elif a.has:
        want = set(a.has)
        hits = []
        for p in sorted(api["prototypes"], key=lambda x: x["name"]):
            if p.get("abstract"):
                continue
            if want <= set(all_props(p["name"], by_name, cache)):
                hits.append(f"{p['name']} | {p.get('typename', '')}")
        print(f"{len(hits)} non-abstract classes with all of: {', '.join(sorted(want))}")
        if hits:
            print("\n".join(hits))
        else:
            print("0 matches does NOT mean no native type exists - verify property spelling with "
                  "--list-props <NearbyClass>; names differ by class (e.g. fluid_box vs fluid_boxes).")
    else:
        ap.error("use --has or --list-props")
