#!/usr/bin/env python3
"""Download the latest runtime-api.json and prototype-api.json from lua-api.factorio.com.
Usage: python fetch_api_jsons.py [--out-dir DIR]   (default: this script's directory/../api)
Re-run after every game update, then run regenerate_indexes.py.
"""
import argparse, os, urllib.request

URLS = ["https://lua-api.factorio.com/latest/runtime-api.json",
        "https://lua-api.factorio.com/latest/prototype-api.json"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "api"))
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    for url in URLS:
        dest = os.path.join(a.out_dir, url.rsplit("/", 1)[1])
        urllib.request.urlretrieve(url, dest)
        print("Wrote", dest, os.path.getsize(dest), "bytes")
