"""
Merge cold_20.csv and prelabeled.csv into labels.csv (UTF-8, text,label,note).
Run from the repo folder:  python merge_labels.py
"""
import pandas as pd

FILES = ["cold_20.csv", "prelabeled.csv"]
VALID = {"analysis", "hot_take", "reaction", "news_info"}
ENCODINGS = ["utf-8-sig", "cp1252", "utf-16", "latin-1"]  # latin-1 never fails


def read_any(path):
    for enc in ENCODINGS:
        try:
            df = pd.read_csv(path, encoding=enc)
            print(f"{path}: read as {enc}, {len(df)} rows, columns={list(df.columns)}")
            return df
        except Exception as e:
            print(f"{path}: {enc} failed ({type(e).__name__}: {str(e)[:80]})")
    raise SystemExit(f"Could not read {path}")


frames = []
for f in FILES:
    df = read_any(f)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df[["text", "label", "note"]].copy()
    df["note"] = df["note"].fillna("")
    frames.append(df)

d = pd.concat(frames, ignore_index=True)

# normalise labels: strip spaces, lowercase, spaces->underscore
d["label"] = (
    d["label"].astype(str).str.strip().str.lower().str.replace(" ", "_")
    .replace({"nan": ""})
)

blank = d["label"] == ""
if blank.any():
    print(f"\nWARNING: {blank.sum()} rows have no label (cold rows you did not label?). Dropping them:")
    print(d[blank]["text"].str.slice(0, 70).to_string())
    d = d[~blank]

bad = ~d["label"].isin(VALID)
if bad.any():
    print("\nFIX THESE: labels not in", VALID)
    print(d[bad][["label", "text"]].assign(text=d["text"].str.slice(0, 60)).to_string())

d = d.drop_duplicates(subset="text").reset_index(drop=True)
d.to_csv("labels.csv", index=False, encoding="utf-8")

print(f"\nWrote labels.csv with {len(d)} rows")
print(d["label"].value_counts())
print((d["label"].value_counts(normalize=True) * 100).round(1).astype(str) + "%")
print("cold rows:", (d["note"].str.strip().str.lower() == "cold").sum())
