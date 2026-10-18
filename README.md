# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter sorts posts from r/IndianCricket, a large public Indian cricket fan community, into four types: `analysis`, `hot_take`, `reaction` and `news_info`. The community mixes stat-backed arguments, confident opinions, in-the-moment fan reactions and plain news or match logistics, and regulars can usually tell which is which within a sentence. I fine-tuned `distilbert-base-uncased` on 330 posts I labeled so it can sort new posts the same way.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:** An argument carried by a specific, checkable fact (a stat, record, date, figure or quote).

**Example 1:**
> Reminder that Bumrah had an economy of 6 in the WC this year bowling death overs on these 250 run pitches

**Example 2:**
> Hope is better than Gayle in T20Is? Shai Hope has more runs than Chris Gayle at better Average and Strike Rate and has more centuries as well. So is he better?

### `hot_take`

**Definition:** A confident opinion, claim, prediction or rant with no support, or only vague support ("almost all", "everyone").

**Example 1:**
> Steve Smith test avg fell off a cliff

**Example 2:**
> Don't think SKY is good enough to be a part of Indian T20 team. I feel like SKY is the most overrated T20 player and does not deserve to be a part of Indian T20 team, let alone, be the captain of the team.

### `reaction`

**Definition:** An immediate emotional, humorous or fan response, with no claim or argument.

**Example 1:**
> WTF!???!??! WAS THAT. NOW I AM SCARED.

**Example 2:**
> That reaction from Kl Rahul was epic

### `news_info`

**Definition:** Reports a fact, announcement or piece of logistics (headlines, match threads, squad news), or asks a neutral question, with no opinion stated.

**Example 1:**
> [News📰] Ravichandran Ashwin is set to be appointed as Team India's new Chief Selector ahead of the 2027 ODI World Cup.

**Example 2:**
> 🚨 MAHELA JAYAWARDENE STEPS DOWN AS THE MUMBAI INDIANS HEAD COACH. 🚨

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`.

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

If a specific, checkable fact (a stat, record, date, figure or quote) carries the argument, the post is `analysis`, even if the tone is heated. A vague quantifier such as "almost all" or "everyone", or a fact that only decorates an opinion already stated, does not count, so the post is `hot_take`. A second rule I used with it: if a post states an opinion at all, it is never `news_info`.



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** r/IndianCricket, a public subreddit. Reddit blocked scripted access, so I saved the public listings (hot, new, top of the year, top of the month, controversial of the year) as JSON from my browser and converted them to CSV with a short script (`json_to_csv.py`), keeping the title plus any body text. That gave 350 posts; after cleaning (HTML entities, duplicates, "content not supported" stubs) 346 remained, and 330 are in `labels.csv`. The 16 left out fit none of my four labels (for example empty prompts like "What's your thought on this?" and off-topic venting).

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

I labeled 20 posts cold first (a random sample, no tools and no AI, marked `cold` in the note column). The other 310 were pre-labeled by Claude and checked by me from my written definitions and marked "pre-labeled" in the note column; the rows it was least sure of were also marked "(uncertain)". I then read and corrected the pre-labeled rows. The final file is one unsplit `labels.csv` with text, label and note columns.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `reaction` | 113 | 34.2% |
| `news_info` | 95 | 28.8% |
| `hot_take` | 93 | 28.2% |
| `analysis` | 29 | 8.8% |
| **Total** | 330 | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* GG's North zone favoritism is ruining golden period of Indian cricket. Maybe I am wrong here, but GG seems to have extra preference for North Indians. Among nearly 10 debuts across various formats under GG, Almost all of them are from Hindi belt of North Ind…
>
> *Could have been:* `analysis` or `hot_take`.
>
> *I chose, because:* `hot_take`. It points at a count ("nearly 10 debuts") but says "almost all" without naming the players or states, so the fact is too vague to check and does not carry the argument. This is exactly the case my decision rule was written for.

**2.**
> *The post:* Stuart Binny for 2027 WC. Stuart Binny deserves to be in India's 2027 World Cup squad. Bumrah? 6/19. Shami? 5/18. Siraj? Whatever. Stuart Binny: 6/4. …
>
> *Could have been:* `analysis` or `hot_take`.
>
> *I chose, because:* `analysis`. It is playful and cherry-picked, but the bowling figures are specific and checkable and they carry the whole argument, so my rule says `analysis`. The tone does not matter.

**3.**
> *The post:* Was Rahul Dravid the most selfish cricketer to play for India? Yes… yessss. Rahul Dravid was the most selfish cricketer not only in India but in world also. Let me give you some reason: 2001, Aus vs Ind: Aus gave follow on …
>
> *Could have been:* `analysis` or `hot_take`.
>
> *I chose, because:* `analysis`. The opening claim is extreme and unsupported, but it goes on to name specific matches and events as its reasons, so checkable facts carry the argument. It was a close call and I could see it labeled `hot_take`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`.

**Settings:** <!-- epochs, learning rate, batch size, seed --> 3 epochs, learning rate 2e-5, batch size 16, max length 128 tokens, seed 42. Trained on CPU (torch 2.14.1+cpu), no GPU.

**Anything I changed from the defaults, and why:** Nothing. I used all the default settings.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

train 230 · val 50 · test 50 (stratified 70/15/15 of the 330 rows). Test split per label: `reaction` 17, `hot_take` 14, `news_info` 14, `analysis` 5. `analysis` has only 5 examples in the test split (fewer than about 8), so its F1 will swing a lot between seeds in unit 6.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* I gave Claude my 350 collected posts and asked what distinctions it could see in the actual text.
- *What came back:* Five types of post (short emotional reactions, confident claims with no support, arguments backed by a specific fact, questions and debate prompts, and news or match logistics) and a draft three-label set, with a note that news and match threads fit none of the three.
- *What I changed:* I added a fourth label, `news_info`, instead of filtering those posts out, and kept the `analysis` vs `hot_take` decision rule as my own.

**Moment 2**

- *What I asked for:* I asked Claude for a Python script to collect r/IndianCricket posts into a CSV.
- *What came back:* A scraper that called Reddit's public JSON endpoints. It failed on my machine with 403 "Blocked" errors on every listing and saved 0 posts.
- *What I changed:* I switched approach: I saved the same listings as JSON from my browser and had a second script (`json_to_csv.py`) convert them to the text, label, note CSV.

**Pre-labelling disclosure:** Claude pre-labeled 310 of the 330 rows in `labels.csv` from my four written definitions; those rows are marked "pre-labeled by AI" in the note column, and I read and corrected them. The other 20 rows (marked `cold`) are my own labels, made first with no AI help.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
