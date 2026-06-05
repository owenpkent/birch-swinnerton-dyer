# Sources

> Original PDFs and their converted text. PDFs are gitignored by default (copyright); the exception `!sources/*.pdf` in `.gitignore` lets you deliberately track a public-domain or open-access source if you choose. Converted plain text (for searching and quoting) is tracked.

## Layout

- `*.pdf`: original documents (track only public-access ones).
- `*.txt`: converted text, produced with `pdfminer.six` or `pypdf` (both in `requirements.txt`).

## Converting a PDF to text

```powershell
python -c "from pdfminer.high_level import extract_text; open('sources/NAME.txt','w',encoding='utf-8').write(extract_text('sources/NAME.pdf'))"
```

## Status

Primary-source tier, kept deliberately small. This repo runs fully offline from the bundled curve data in `experiments/_shared/curve_data.py` (public LMFDB/Cremona invariants), so no source PDF is required to run the experiments. Classical originals (the Birch and Swinnerton-Dyer 1965 paper, the Clay problem description) and their text conversions belong here when committed; the broader modern reference library (28 sources across eight topic folders) lives in [`../references/`](../references/) as gitignored PDFs plus a tracked index.

The reference library is now populated and read through. See [`../references/README.md`](../references/README.md) for the eight-folder index (with local-PDF status per source) and [`../docs/03_research/reading_notes/`](../docs/03_research/reading_notes/) for one deep reading note per source, each running the source against the three detectors. The drop-to-note workflow is documented in [`../docs/03_research/reading_notes/PROCESSING_PDFS.md`](../docs/03_research/reading_notes/PROCESSING_PDFS.md).

## Attribution and copyright

Do not commit copyrighted PDFs. The bibliography in `references/README.md` is the tracked record; the PDFs themselves stay local.
