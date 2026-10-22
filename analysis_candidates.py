"""
Milestone 5 helper: find NEW candidate `analysis` posts and, after you have
reviewed them, add the ones you approve to labels.csv.

Step A (find candidates):
    1. Save Reddit search pages as .json files into ./reddit_json_analysis/
    2. python analysis_candidates.py
       -> writes candidates_analysis.csv (new posts with the most numbers first)

Step B (after you labelled rows `analysis` in candidates_analysis.csv):
    python analysis_candidates.py --merge
       -> backs up labels.csv, appends your approved rows, prints new counts
"""
import argparse
import glob
import html
import json
import re
import sys
from pathlib import Path

import pandas as pd

IN_DIR = "reddit_json_analysis"
CAND = "candidates_analysis.csv"
MAX_CANDIDATES = 150
STUB = re.compile(
    r"\s*This post contains content not supported on old Reddit\.?\s*"
    r"\[Click here to view the full post\]\([^)]*\)"
)


def clean(text):
    text = html.unescape(str(text)).replace("\u200b", "").replace("&#x200B;", "")
    text = STUB.sub("", text).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text[:1200]


def key(text):
    return re.sub(r"\s+", " ", clean(text)).lower()[:100]


def existing_keys():
    keys = set()
    for path in ("labels.csv", "raw_posts.csv"):
        if Path(path).exists():
            df = pd.read_csv(path, encoding="utf-8-sig")
            keys |= {key(t) for t in df["text"]}
    return keys


def find_candidates():
    files = sorted(glob.glob(f"{IN_DIR}/*.json"))
    if not files:
        sys.exit(f"No .json files in ./{IN_DIR}/ - save the search pages there first.")
    seen = existing_keys()
    rows = []
    for path in files:
        try:
            with open(path, encoding="utf-8-sig") as f:
                children = json.load(f)["data"]["children"]
        except Exception as e:
            print(f"Skipping {path}: {e}")
            continue
        added = 0
        for child in children:
            p = child["data"]
            title = (p.get("title") or "").strip()
            body = (p.get("selftext") or "").strip()
            if body in ("[removed]", "[deleted]"):
                body = ""
            text = clean(f"{title}\n\n{body}" if body else title)
            k = key(text)
            if len(text) < 60 or k in seen:
                continue
            seen.add(k)
            numbers = len(re.findall(r"\d+(?:\.\d+)?", text))
            if numbers < 2:
                continue
            rows.append((numbers, text))
            added += 1
        print(f"{path}: {added} new candidate posts")
    rows.sort(key=lambda r: -r[0])
    rows = rows[:MAX_CANDIDATES]
    out = pd.DataFrame({"text": [r[1] for r in rows], "label": "", "note": ""})
    out.to_csv(CAND, index=False, encoding="utf-8-sig")  # opens cleanly in Excel
    print(f"\nWrote {CAND} with {len(out)} candidates (most numbers first).")
    print("Open it, read each post, and type  analysis  in the label column ONLY for")
    print("posts where a specific checkable fact carries the argument. Leave the rest blank.")


def merge():
    if not Path(CAND).exists():
        sys.exit(f"{CAND} not found. Run without --merge first.")
    cand = pd.read_csv(CAND, encoding="utf-8-sig")
    cand["label"] = cand["label"].fillna("").astype(str).str.strip().str.lower()
    keep = cand[cand["label"] == "analysis"].copy()
    if keep.empty:
        sys.exit("No rows labelled 'analysis' in the candidates file.")

    labels = pd.read_csv("labels.csv", encoding="utf-8-sig")
    backup = Path("labels_before_improvement.csv")
    if not backup.exists():
        labels.to_csv(backup, index=False, encoding="utf-8")
        print(f"Backed up the original to {backup}")

    have = {key(t) for t in labels["text"]}
    keep = keep[~keep["text"].map(key).isin(have)]
    keep["note"] = "added in unit 6 improvement (analysis); reviewed by me"
    merged = pd.concat([labels, keep[["text", "label", "note"]]], ignore_index=True)
    merged.to_csv("labels.csv", index=False, encoding="utf-8")

    print(f"\nAdded {len(keep)} new analysis rows. labels.csv now has {len(merged)} rows:")
    counts = merged["label"].value_counts()
    for name, n in counts.items():
        print(f"  {name:<10} {n:>4}  {n / len(merged):.1%}")
    if len(keep) < 25:
        print("\nNote: fewer than ~30 added. That is fine, but say the real number in your README.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    merge() if args.merge else find_candidates()
