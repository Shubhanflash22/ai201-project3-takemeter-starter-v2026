"""
Convert Reddit listing JSON files saved from your browser into raw_posts.csv
(columns: text, label, note; label left blank for you to fill in).

Usage:
    1. Save each listing page as a .json file inside ./reddit_json/
    2. python json_to_csv.py
"""
import csv
import glob
import json

IN_DIR = "reddit_json"
OUT_FILE = "raw_posts.csv"
MIN_CHARS = 25


def main():
    seen = set()
    rows = []
    files = sorted(glob.glob(f"{IN_DIR}/*.json"))
    if not files:
        print(f"No .json files found in ./{IN_DIR}/")
        return
    for path in files:
        try:
            with open(path, encoding="utf-8-sig") as f:
                data = json.load(f)["data"]["children"]
        except Exception as e:
            print(f"Skipping {path}: {e}")
            continue
        count_before = len(rows)
        for child in data:
            p = child["data"]
            title = (p.get("title") or "").strip()
            body = (p.get("selftext") or "").strip()
            if body in ("[removed]", "[deleted]"):
                body = ""
            text = f"{title}\n\n{body}".strip() if body else title
            key = text.lower()
            if len(text) < MIN_CHARS or key in seen:
                continue
            seen.add(key)
            rows.append(text)
        print(f"{path}: +{len(rows) - count_before} new posts")

    with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "label", "note"])
        for text in rows:
            w.writerow([text, "", ""])
    print(f"Saved {len(rows)} unique posts to {OUT_FILE}")


if __name__ == "__main__":
    main()
