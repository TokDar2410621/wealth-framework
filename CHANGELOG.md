# Changelog

## 1.1.0 (2026-10-09)

- New source: Alex Hormozi, *$100M Money Models* (`sources/hormozi-100m-money-models.md`,
  MNY-1 to MNY-10): monetization and offer sequencing, Client-Financed Acquisition, the
  30-day rule, LTGP:CAC bars, upsells, downsells, continuity. 120 laws in all.
- *$100M Offers* source: M-A-G-I-C naming added to HOR-3, guarantee types detailed in HOR-5.
- New tools: `scripts/value_equation.py` (scores an offer on HOR-2's four drivers, names the
  weakest and the fix) and `scripts/money_model.py` (checks the 30-day rule and LTGP:CAC,
  MNY-1 to MNY-3).
- `artifacts/`: interactive French summary pages for *$100M Offers* and *$100M Money Models*,
  linked from their source files.

## 1.0.1 (2026-10-09)

- Step 0: when the skill is read through a catalog (`read-skill`), skip the freshness check and
  open the files through the catalog's reference paths.

## 1.0.0 (2026-10-09)

- First version: 110 laws from 8 books (Hormozi x2, Thiel, DeMarco, Kawasaki, Greene x2, Dalio),
  two families of field laws, and La Table's decision frameworks.
- Decision mode built on Dalio's five steps, with two guards: "new toy?" and "design or
  execution?" after a failed test. Insight mode for business talk with no decision at stake.
- Evidence levels on every law (🟢 proven, 🟠 claimed or lived once, 🔴 to test).
- `scripts/sync.py`: freshness check and safe update of the installed clone, tested against real
  git repositories.
- `scripts/build_glossary.py`: rebuilds the glossary from the source files.
