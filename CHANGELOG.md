# Changelog

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
