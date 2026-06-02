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

Empty by default. This repo runs fully offline from the bundled curve data in `experiments/_shared/curve_data.py` (public LMFDB/Cremona invariants), so no source PDF is required to run the experiments. Add sources here as the literature survey (SURVEYOR) proceeds, and record each in [`../references/README.md`](../references/README.md) with a reading note in [`../docs/03_research/reading_notes/`](../docs/03_research/reading_notes/).

## Attribution and copyright

Do not commit copyrighted PDFs. The bibliography in `references/README.md` is the tracked record; the PDFs themselves stay local.
