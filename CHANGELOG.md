# Changelog

## 1.1.0 (2026-10-09)

- New source: Alex Hormozi, *$100M Money Models* (`sources/hormozi-100m-money-models.md`,
  MNY-1 to MNY-10): monetization and offer sequencing, Client-Financed Acquisition, the
  30-day rule, LTGP:CAC bars, upsells, downsells, continuity. 120 laws in all.
- *$100M Offers* source: M-A-G-I-C naming added to HOR-3, guarantee types detailed in HOR-5.
- Tools, on one rule: code only where code beats the model.
  - `scripts/journal.py`: decision journal (verdict, cheapest test, deadline, deciding number,
    then the real result); `SKILL.md` checks due tests at step 0 and logs every verdict.
  - `scripts/channel_math.py`: expected replies and deals, probability of zero (FLE-3).
  - `scripts/money_model.py`: computes the 30-day rule and the LTGP:CAC bar (MNY-1 to MNY-3).
  - `protocols/grill-offer.md`: the Value Equation grill as a markdown protocol, with no
    numeric score; it replaces `scripts/value_equation.py`, whose interview mode could not
    run when the agent launched it.
  - `artifacts/offer-griller.html`: a form that briefs the agent; it asks for a judgment and a
    verdict, no longer a score out of 100.
  - `tests/test_tools.py`: 21 tests for the three scripts.
- The deep-dive summary pages for *$100M Offers* and *$100M Money Models* moved to the
  maintainer's brain; the repository keeps only what the agent reads.
- Fixed a sentence in FLE-3 cut during the 1.0.0 anonymization.

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
