# Running TakeMeter

This project trains a model. It runs on the local machine, in a notebook, from
inside this repo. No accounts, no keys, nothing hosted.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

`python test.py` checks the Python version against the pins, the disk, the
memory, and whether the packages import.

- **Disk:** about 9 GB free. The baseline model is roughly 1.6 GB and PyTorch is
  not small.
- **RAM:** about 6 GB. `baseline.py` peaks around 1.8 GB loading the zero-shot
  model and the training run peaks around 2.1 GB. Neither is comfortable beside
  an editor and a browser on a 4 GB machine.
- **Baseline model:** `test.py` shows `[WARN] Baseline model: not downloaded yet`
  until `python baseline.py` has run once and downloaded it (1.6 GB).

No API key and no accounts are needed. Nothing here calls a hosted model.

### Training device

`test.py` reports the device, and so does section 1 of the notebook:

| Device | What it means | Speed |
|---|---|---|
| `cuda` | An NVIDIA GPU | Under a minute per seed |
| `mps` | Apple Silicon (M1 and later) | Fast; much quicker than the CPU path |
| `cpu` | Everything else | A few minutes per seed |

The device is part of the result. Two people running the same notebook on the
same data with the same seed can get different numbers, because different
hardware does the arithmetic in a slightly different order. `results.json`
records it.

## The notebook

`takemeter.ipynb` runs from inside this repo.

1. Open it in VS Code (or `jupyter notebook`).
2. Pick the kernel: the `.venv` inside this project. In VS Code that's the
   selector in the top right. A wrong kernel is the most common way the first
   cell fails, and it reports that a package isn't installed when it is.
3. The two author lines in section 1's second cell only label the results.

Open it from the repo, not from a copy. The notebook writes next to the code and
expects `labels.csv` to be there; opened from elsewhere, it says so.

It reads and writes this folder. `labels.csv` is already here; `results.json`,
`test_split.csv` and `results_three_seeds_*.json` land here when the notebook
writes them. Nothing is pushed for you.

- Section 5 writes `results.json` and `test_split.csv`.
- Section 6 writes `results_three_seeds_<label>.json`. Set `RUN_LABEL = "after"`
  in that cell before a re-run, or the re-run overwrites the earlier numbers.

If rows are added to `labels.csv` mid-session, re-run section 2, which is what
reads the file. Changes to `LABELS`, the settings and the seed live in the
notebook file and are committed like any other change.

| Section | What it does |
|---|---|
| 1. Setup | Reports the device and confirms it can see the files |
| 2. Labels | `LABELS`, the settings, and the seed |
| 3. Split | 70/15/15, stratified |
| 4. Train | Minutes on a laptop CPU, under one on a GPU |
| 5. Results | Writes `results.json` and `test_split.csv` |
| 6. Three seeds | Retrains three times in one cell |
| 7. Confusion matrix | Prints a markdown table |

## The data

`labels.csv` has three columns:

| Column | What's in it |
|---|---|
| `text` | The whole post. Don't trim it to fit |
| `label` | One of the labels, spelled exactly as in `LABELS` |
| `note` | `cold` for the 20 labelled unaided, and a note on any that were pre-labelled |

`labels_template.csv` shows the shape. `data/practice_labels.csv` is a 60-post
set from a fictional running forum, already labelled, for running the whole
notebook without data of your own.

Keep it as one unsplit file. The notebook does the 70/15/15 split, and splitting
twice is how examples leak between training and test.

### The check before training

Section 2's last cell looks for things that break a run or quietly ruin it:

| It says | What it means |
|---|---|
| `[FIX ME] Labels in your CSV that aren't in LABELS` | A spelling or capital mismatch. `Hot_take` and `hot_take` are different |
| `[FIX ME] 'x' is 78% of your data` | Over the 70% cap. The model will learn to guess it |
| `[look at] N duplicate posts` | They land in different splits and inflate the score (leakage) |
| `[look at] Only 12 examples of 'x'` | Its test split will be tiny, so its F1 will jump between seeds |
| `[look at] 60 rows` | Under the 200-row floor. Training still runs, which is fine for the practice data |

## The baseline

```bash
python baseline.py
python baseline.py --trained results.json
```

This runs a general model over the posts using only the label definitions, with
no training. It is the opponent the fine-tuned model has to beat.

It scores `test_split.csv`, the held-out posts the notebook saved, which are the
same ones the trained model was measured on. If the file isn't there, it says so
and falls back to a random sample of `labels.csv`, which is not like-for-like.

Definitions go in `label_definitions.txt`, one per line as `label: definition`.
They are the entire input the model gets. Without the file it falls back to bare
label names, a much weaker prompt. Running it both ways measures what the
definitions are worth.

The second command adds a Trained column and prints the **Baseline vs. Trained**
table. It takes a few seconds per post, so 30 posts takes a couple of minutes.

## The agreement check

Staff labelled 30 posts under the taxonomy in `data/staff_taxonomy.md`. The same
30 are labelled again under those definitions, not the project's own, and
compared.

```bash
python agreement.py
```

| File | What it is |
|---|---|
| `data/staff_taxonomy.md` | The definitions and decision rules staff used |
| `data/staff_posts.csv` | The 30 posts, no labels |
| `data/staff_labels.csv` | The staff labels. Posts and labels join on `id` |
| `my_staff_labels.csv` | The same posts labelled by hand, with `text` and `label` columns |

With both staff files in `data/` under those names, the bare command finds them.
Anywhere else:

```bash
python agreement.py --staff-posts posts.csv --staff-labels labels.csv
```

Posts are matched on their text, so paste it unchanged. A retyped or trimmed
post won't match, and the script says which ones didn't.

It works out the rate and lists every disagreement, and stops there on purpose.
The rate is arithmetic; the adjudication is done by hand. This is the one
instrument that can tell a labelling problem from a model problem: a label pair
disagreed on with staff that the confusion matrix also confuses is a finding
about the labels, not the model.

## Commands

| Command | What it does |
|---|---|
| `python test.py` | Checks the environment |
| `python baseline.py` | The zero-shot baseline on the held-out posts |
| `python baseline.py --help` | All the options |
| `python agreement.py` | Own labels vs. the staff set |
| Notebook, sections 1-5 | Train once, write `results.json` |
| Notebook, sections 6-7 | Three seeds and the matrix |

## Where everything lives

| File | What it does |
|---|---|
| `takemeter.ipynb` | The training notebook |
| `baseline.py` | The zero-shot baseline |
| `agreement.py` | Own labels against the staff set |
| `analysis_candidates.py` | Finds new candidate `analysis` posts and merges approved ones into `labels.csv` |
| `json_to_csv.py` | Converts saved Reddit JSON into `raw_posts.csv` |
| `merge_labels.py` | Merges `cold_20.csv` and `prelabeled.csv` into `labels.csv` |
| `criteria.md` | The five acceptance criteria |
| `labels.csv` | The labelled data |
| `labels_template.csv` | The shape it needs |
| `label_definitions.txt` | The definitions, for the baseline |
| `data/practice_labels.csv` | The 60-post practice set |
| `data/staff_taxonomy.md`, `staff_posts.csv`, `staff_labels.csv` | The staff set |
| `README.md` | The write-up |
| `results.json`, `test_split.csv` | Written by the notebook |
| `results_three_seeds_before.json`, `results_three_seeds_after.json` | Written by section 6 with `RUN_LABEL` set |
| `baseline_results.json` | Written by `baseline.py` |
| `agreement_results.json` | Written by `agreement.py` |
| `my_staff_labels.csv` | Own labels on the staff set |

## Troubleshooting

| What you see | What it means |
|---|---|
| Section 1 says `cpu` | Correct on most laptops, and fine. Nothing to fix |
| `ModuleNotFoundError` in the notebook | Wrong kernel. Pick the `.venv` inside this project |
| `FileNotFoundError: labels.csv` | The file doesn't exist yet, or the notebook is open from a copy rather than the repo. Section 1's second cell says which |
| The machine crawls during training | Close the browser and anything heavy. Training peaks around 2.1 GB |
| `KeyError` during training | A label in the CSV isn't in `LABELS`. Check capitals and spaces |
| Training takes an hour | It is running on CPU |
| Accuracy swings 15 points between seeds | The dataset is too small or too lopsided for a stable measure. That is a diagnosis, not a mistake |
| A label's F1 is 0.00 | It probably has almost nothing in the test split. Check the split table |
| `baseline.py` says no `test_split.csv` | Section 5 never finished. Re-run it |
| `baseline.py` is downloading forever | First run only, ~1.6 GB |
| The baseline is very slow | Expected. A few seconds per post is what no fine-tuning costs at runtime |

The three usual causes when the notebook fails, in order: the kernel is the
system Python rather than this project's `.venv`, the notebook was opened from a
copy outside the repo, or a label in the CSV doesn't match `LABELS` exactly.

The `results*.json` files are deliberately not in `.gitignore`. They are evidence
the run happened, along with `test_split.csv` and `labels.csv`.
