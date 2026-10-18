# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

Community: r/IndianCricket. Labels: `analysis`, `hot_take`, `reaction`, `news_info`.
These five criteria were written in unit 5, before anything was trained. Each
must hold on all three seeds in unit 6.

Context for the numbers: four labels means a random guesser gets about 25%, and
always predicting the biggest label gets about 34%. labels.csv has roughly 330
rows, so the 15% test split is about 50 posts (about 17 `reaction`, 14
`hot_take`, 14 `news_info`, and only about 3 `analysis`).
---

## 1.

<!-- Your criterion. It must name a number. -->



**Why this target:**



---

## 2.

<!-- Your criterion. -->



**Why this target:**



---

## 3.

<!-- Your criterion. -->



**Why this target:**



---

## 4.

<!-- Your criterion. -->



**Why this target:**



---

## 5.

<!-- Your criterion. -->



**Why this target:**



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
---

## 1. Overall accuracy is at least 0.60

Accuracy on the held-out test split is at least 0.60 on every seed.

**Why this target:** 0.60 is nearly double the 34% majority-label baseline, and
I would call a classifier that is right about 3 times in 5 useful for sorting
fan posts into four types. I did not go higher because opinion text is fuzzy
and the `hot_take` / `reaction` boundary is subjective, so I expect noise
even with careful labels.

---

## 2. The three large labels each have F1 of at least 0.50

`reaction`, `hot_take` and `news_info` each have an F1 of at least 0.50 on the
held-out test split, on every seed.

**Why this target:** these three labels each have about 90 to 100 examples
(roughly a third of the data each), so their scores should be steadier than
`analysis`. 0.50 is double the 0.25 random-guess level, and it forbids one of
these labels from being ignored while accuracy looks fine.

---

## 3. `analysis` has an F1 of at least 0.30

`analysis` has an F1 of at least 0.30 on the held-out test split, on every seed.

**Why this target:** `analysis` is my smallest label (about 21 examples, around
7% of the data), so only about 3 land in the test split and one post changes
its score a lot. I set it looser than criterion 2 for that reason. 0.30 still
requires the model to find some real `analysis` posts, which is more than the
zero a model that never predicts the label would score.

---

## 4. The trained model beats the zero-shot baseline on accuracy

The fine-tuned model's accuracy is higher than the baseline's accuracy on the
same test split (test_split.csv), on every seed.

**Why this target:** if a general model reading my definitions with no training
does as well as my fine-tuned model, the 330 labels and the training added
nothing. This one is a yes/no check, and it could well come out as no.

---

## 5. Label balance: no label above 40%, and `analysis` at least 5%

In labels.csv, no label is more than 40% of the rows, and `analysis` is at
least 5% of the rows.

**Why this target:** the course cap is 70%, but with four labels a 40% label
would already be heavily skewed toward one class. My current counts are about
34% / 30% / 30% / 7%. I set a floor on `analysis` because it is the thin
label, and below about 5% (roughly 16 rows) the model has almost nothing to
learn it from. This one I expect to meet.
