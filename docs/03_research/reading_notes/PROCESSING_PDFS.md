# Organizing and processing PDFs in this repo

> The repeatable procedure for taking a PDF (a paper dropped into the repo, or a classical
> source) and filing it, extracting it, taking notes on it, and wiring it into the BSD program.
> Entry points that link here: [`references/README.md`](../../../references/README.md),
> [`sources/README.md`](../../../sources/README.md), and the [reading-notes index](README.md).
> If you just dropped a PDF at the repo root, start at section 4.

## 1. Where PDFs live (three tiers)

| Tier | Directory | What goes here | PDF in git? | Index |
|---|---|---|---|---|
| Primary sources | [`sources/`](../../../sources/) | Classical / original documents (Birch and Swinnerton-Dyer 1965, the Clay problem description, open-access surveys) and their `.txt` conversions | **Committed** (gitignore whitelist `!sources/*.pdf`) | [`sources/README.md`](../../../sources/README.md) |
| Reference library | [`references/NN_topic/`](../../../references/) | Modern papers and monographs the program reads | **Gitignored** (`*.pdf`); only the index is tracked | [`references/README.md`](../../../references/README.md) |
| Notes | [`docs/03_research/reading_notes/`](.) | One `Author-Year-Topic.md` note per source, house style | n/a (markdown) | [`reading_notes/README.md`](README.md) |

The eight reference-library role folders (mapped to the proof architectures in
[`docs/solutions/README.md`](../../solutions/README.md)):
`01_modularity`, `02_heegner_gross_zagier`, `03_euler_systems`,
`04_iwasawa_main_conjecture`, `05_statistics_averages`, `06_function_field`,
`07_foundations_textbooks`, `08_surveys_originals`. The reading-notes index mirrors these folders.

**A PDF at the repo root is unfiled.** Root `*.pdf` is gitignored and belongs nowhere; file it into
`sources/` (primary source) or `references/NN_topic/` (reference paper). Do not leave it at root.

## 2. .gitignore rules (already in place)

```
*.pdf                # all PDFs ignored by default (references are copyrighted)
!sources/*.pdf       # EXCEPT primary sources, which are committed
```

So: `sources/` PDFs are tracked; `references/` PDFs are not (the tracked artifact is the index entry
plus the reading note). Scratch text extracts (`_name.txt`) are temporary; delete them when done. arXiv
papers are often open (Bhargava-Shankar, Bhargava-Skinner-Zhang, BKLPR), so they *could* be committed,
but we keep them in `references/` (gitignored, index-only) for uniformity; the arXiv ID in the index
lets anyone re-fetch.

## 3. Naming conventions

- Reference PDF: `Author(s)-Year-Short-Title.pdf`
  (e.g. `Gross-Zagier-1986-Heegner-Points-and-Derivatives-of-L-series.pdf`).
- Reading note: `Author-Year-Topic.md` (e.g. `Gross-Zagier-1986-Heegner-Points-Derivatives.md`).
- Keep the note filename close to the PDF filename so the two are traceable to each other.

## 4. The workflow (drop -> filed -> extracted -> noted -> mapped)

**Step 0 - classify.** Primary source or reference paper? Which of the eight topic folders? (Match the
paper's role to a proof architecture; `08_surveys_originals` for surveys and the founding papers.)

**Step 1 - file the PDF.** Move it from the root into `sources/` or `references/NN_topic/` with the
naming convention. References PDFs stay gitignored; sources PDFs are committed.

**Step 2 - index it.** Add a row to the relevant table:
- `references/README.md`: `| Author-Year-Title.pdf | Full citation | Role in the program |`
- or `sources/README.md`: `| File | Description |`

**Step 3 - extract the text** (for accurate notes; pick one):
- `pypdf`: `python -c "from pypdf import PdfReader; r=PdfReader('path.pdf'); open('_x.txt','w',encoding='utf-8').write(chr(10).join(p.extract_text() for p in r.pages))"`
- `pdfminer.six` (see [`sources/README.md`](../../../sources/README.md)).
- or the Read tool's `pages=` to read the PDF directly (good for theorem statements and formulas).
- Write to a scratch `_name.txt` at root (gitignored); delete it in Step 7.

**Step 4 - write the reading note** in `reading_notes/` in the **house style** (see any existing note,
e.g. [`Gross-Zagier-1986-...`](Gross-Zagier-1986-Heegner-Points-Derivatives.md) or
[`Tate-1966-...`](Tate-1966-BSD-Geometric-Analog.md)):
1. Title line: full citation.
2. Blockquote: the source's **role** in the program, **reading depth**, cross-links (the four-level
   framing in [`docs/02_graduate/`](../../02_graduate/), the three detectors in
   [`experiments/_shared/controls.py`](../../../experiments/_shared/controls.py), the research
   directions in [`research_directions/`](../research_directions/), the
   [atlas](../../research_atlas/README.md)), and how it differs from related notes.
3. `## One-line takeaway`.
4. `## Technical content (section by section)`: bold section headers, precise definitions and theorem
   statements, key formulas, page references. State the actual theorems.
5. `## Project mapping`: what is proven vs the gap; the exact regime (analytic rank 0/1 vs $\geq 2$;
   archimedean vs $p$-adic); which of the three detectors it triggers or passes; which research
   direction / experiment it feeds.
6. An honest `## Status` depth line.

Math uses `$...$` inline and `$$...$$` display. **No em dashes and no en dashes anywhere** (project
style); rewrite the sentence instead.

**Step 5 - index the note.** Add a row to `reading_notes/README.md` under the right `NN` folder, with a
one-line headline.

**Step 6 - deeper artifacts (only if warranted).** If the source is load-bearing for the front: write an
assessment in [`docs/03_research/`](..), and/or build experiments in
[`experiments/`](../../../experiments/) (each with a `LEARNINGS.md` finding and a `PLAN.md`/`TODO.md`
entry). Cross-link all of them to the reading note.

**Step 7 - clean up and commit.** Delete scratch `_*.txt`. Commit the tracked changes (the note, the
index rows, any assessment/experiments). The reference PDF itself is gitignored, so the move is local
only; the committed record is the index entry. Push per the per-action authorization policy.

## 5. The three-detector discipline (apply in every note's Project mapping)

Every note states, against [`experiments/_shared/controls.py`](../../../experiments/_shared/controls.py):

1. **Parity-only.** The root number gives the rank mod 2; a method that recovers only parity (modularity)
   cannot prove the full rank equality.
2. **Sha-finiteness assumed.** $\#\mathrm{Sha}$ finite is a theorem only for analytic rank $\leq 1$. A
   method that uses it in the open regime must flag the assumption.
3. **Function-field mirage.** BSD over $\mathbb{F}_q(C)$ is a theorem under finite Sha (Tate, Artin-Tate,
   Milne, Ulmer). A method that "works verbatim" over a function field has imported the geometric
   Frobenius the number-field case lacks.

Plus the **control pair**: rank $\leq 1$ (proven) vs rank $\geq 2$ (open). A source's bearing on the
program is whether it does anything genuinely new in the open regime.
