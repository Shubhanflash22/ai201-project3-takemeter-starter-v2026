# Acceptance criteria: TakeMeter

Five criteria that say what "working" means for this classifier, written **before** anything was trained. Each must hold on all three seeds in unit 6.

Community: r/IndianCricket. Labels: `analysis`, `hot_take`, `reaction`, `news_info`.

Context for the numbers: four labels means a random guesser gets about 25%, and always predicting the biggest label gets about 34%. labels.csv has roughly 330 rows, so the 15% test split is about 50 posts (about 17 `reaction`, 14 `hot_take`, 14 `news_info`, and only about 3 `analysis`).

---

## 1. Overall accuracy is at least 0.60

Accuracy on the held-out test split is at least 0.60 on every seed.

**Why this target:** 0.60 is nearly double the 34% majority-label baseline, and I would call a classifier that is right about 3 times in 5 useful for sorting fan posts into four types. I did not go higher because opinion text is fuzzy and the `hot_take` / `reaction` boundary is subjective, so I expect noise even with careful labels.

---

## 2. The three large labels each have F1 of at least 0.50

`reaction`, `hot_take` and `news_info` each have an F1 of at least 0.50 on the held-out test split, on every seed.

**Why this target:** these three labels each have about 90 to 100 examples (roughly a third of the data each), so their scores should be steadier than `analysis`. 0.50 is double the 0.25 random-guess level, and it forbids one of these labels from being ignored while accuracy looks fine.

---

## 3. `analysis` has an F1 of at least 0.30

`analysis` has an F1 of at least 0.30 on the held-out test split, on every seed.

**Why this target:** `analysis` is my smallest label (about 21 examples, around 7% of the data), so only about 3 land in the test split and one post changes its score a lot. I set it looser than criterion 2 for that reason. 0.30 still requires the model to find some real `analysis` posts, which is more than the zero a model that never predicts the label would score.

---

## 4. The trained model beats the zero-shot baseline on accuracy

The fine-tuned model's accuracy is higher than the baseline's accuracy on the same test split (test_split.csv), on every seed.

**Why this target:** if a general model reading my definitions with no training does as well as my fine-tuned model, the 330 labels and the training added nothing. This one is a yes/no check, and it could well come out as no.

---

## 5. Label balance: no label above 40%, and `analysis` at least 5%

In labels.csv, no label is more than 40% of the rows, and `analysis` is at least 5% of the rows.

**Why this target:** the course cap is 70%, but with four labels a 40% label would already be heavily skewed toward one class. My current counts are about 34% / 30% / 30% / 7%. I set a floor on `analysis` because it is the thin label, and below about 5% (roughly 16 rows) the model has almost nothing to learn it from. This one I expect to meet.
