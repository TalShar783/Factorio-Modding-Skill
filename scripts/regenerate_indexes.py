#!/usr/bin/env python3
"""Regenerate references/prototype-index.md (grouped + TOC) from prototype-api.json.
Usage: python regenerate_indexes.py --prototype-json prototype-api.json [--out-dir references]
Fallback tool: only needed when FMTK's generated stub library isn't available in the
current VS Code workspace (see SKILL.md 'Development environment (FMTK)'). Events and
defines no longer get a hand-maintained index here - grep FMTK's events.lua/defines.lua
(or runtime-api.json as last resort) directly instead.
"""
import argparse, json, re, os, sys

def load_json(path):
    if not os.path.isfile(path):
        sys.exit(f"{path} not found - run 'python scripts/fetch_api_jsons.py' first (JSONs land in api/)")
    return json.load(open(path, encoding="utf-8"))

GROUP_ROOTS = {"EntityPrototype": "Entities", "ItemPrototype": "Items",
               "EquipmentPrototype": "Equipment", "TilePrototype": "Tiles",
               "AchievementPrototype": "Achievements"}
GROUP_ORDER = ["Entities", "Items", "Equipment", "Tiles", "Achievements", "Other"]

def first_sentence(desc):
    desc = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", (desc or "").strip())
    return desc.split(".")[0].strip()

def proto_group(p, by_name):
    cur = p
    while cur:
        if cur["name"] in GROUP_ROOTS:
            return GROUP_ROOTS[cur["name"]]
        cur = by_name.get(cur.get("parent"))
    return "Other"

def gen_prototype_index(api, out):
    by_name = {p["name"]: p for p in api["prototypes"]}
    groups = {g: [] for g in GROUP_ORDER}
    for p in sorted(api["prototypes"], key=lambda x: x["name"]):
        groups[proto_group(p, by_name)].append(p)
    L = ["# Factorio 2.x Prototype Index", "",
         f"Generated from prototype-api.json (api_version {api.get('api_version')}, game {api.get('application_version')}).",
         "Entries marked **[NO DESC]** have blank descriptions in the API - fill these in manually.",
         "Grouped by ancestry. 'Other' holds everything without an Entity/Item/Equipment/Tile/Achievement ancestor: recipes, technologies, fluids, categories, settings, visuals, utility prototypes.",
         "", "## Contents", ""]
    L += [f"- [{g}](#{g.lower()}) ({len(groups[g])})" for g in GROUP_ORDER]
    for g in GROUP_ORDER:
        L += ["", f"## {g}", "", "| Prototype class | typename | Description |", "|---|---|---|"]
        for p in groups[g]:
            tag = " *(abstract)*" if p.get("abstract") else ""
            tn = p.get("typename") or "*(abstract)*"
            d = first_sentence(p.get("description")) or "**[NO DESC]**"
            L.append(f"| {p['name']}{tag} | {tn} | {d} |")
    L += ["", "---", "*Abstract prototypes are base types only - not used directly in data:extend.*", ""]
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print("Wrote", out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--prototype-json", required=True)
    ap.add_argument("--out-dir", default=os.path.dirname(os.path.abspath(__file__)) + "/..")
    a = ap.parse_args()
    gen_prototype_index(load_json(a.prototype_json),
                        os.path.join(a.out_dir, "prototype-index.md"))
