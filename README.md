# wealth-framework

A Claude Code skill that judges business decisions against the laws of nine books, field-tested
selling and execution laws, and the decision frameworks of great founders.

Bring it an idea, an offer, a price or a choice. When a decision is at stake, it answers
**go**, **go with conditions** or **no-go**, lists the laws respected and the laws broken (each
with its source and evidence level), and ends with the cheapest test that lets the market
decide. In ordinary business talk it stays quiet, or adds at most three one-line insights.

It answers in your language.

## Install

```bash
git clone https://github.com/TokDar2410621/wealth-framework ~/.claude/skills/wealth-framework
```

Windows (PowerShell):

```powershell
git clone https://github.com/TokDar2410621/wealth-framework "$HOME\.claude\skills\wealth-framework"
```

Install it as a git clone, not by copying files: at the start of each conversation the skill
runs `scripts/sync.py`, which updates the clone when a new version is out. It never overwrites
local edits or unpushed commits; if you changed files, it reads the current version from
`origin/main` instead and tells you.

Then talk business with Claude as usual. The skill loads on its own.

## Sources

| Source | File | Laws |
|---|---|---|
| Alex Hormozi, *$100M Offers* | `sources/hormozi-100m-offers.md` | HOR-1 to HOR-10 |
| Alex Hormozi, *$100M Leads* | `sources/hormozi-100m-leads.md` | LDS-1 to LDS-12 |
| Alex Hormozi, *$100M Money Models* | `sources/hormozi-100m-money-models.md` | MNY-1 to MNY-10 |
| Peter Thiel, *Zero to One* | `sources/thiel-zero-to-one.md` | THI-1 to THI-8 |
| MJ DeMarco, *The Millionaire Fastlane* (CENTS) | `sources/demarco-millionaire-fastlane.md` | DEM-1 to DEM-8 |
| Guy Kawasaki, *The Art of the Start* | `sources/kawasaki-art-of-the-start.md` | KAW-1 to KAW-9 |
| Robert Greene, *The 48 Laws of Power* | `sources/greene-48-laws-of-power.md` | G48-1 to G48-10 |
| Robert Greene, *The Laws of Human Nature* | `sources/greene-laws-of-human-nature.md` | GHN-1 to GHN-8 |
| Ray Dalio, *Principles* | `sources/dalio-principles.md` | DAL-1 to DAL-9 |
| Field laws: selling and offers | `sources/field-laws-selling.md` | FLS-1 to FLS-12 |
| Field laws: execution and distribution | `sources/field-laws-execution.md` | FLE-1 to FLE-12 |
| La Table: decision frameworks of the greats (Bezos, Paul Graham, Taleb, Musk, Thiel, Zuckerberg) | `sources/la-table-frameworks.md` | TAB-1 to TAB-12 |

120 laws in all. `cheatsheet.md` gathers the decision rules by situation; `glossary.md` lists
every law by name.

**Evidence levels.** Every law is marked 🟢 proven (controlled study, audited data, public law),
🟠 claimed by its author or observed once in the field, or 🔴 to test. Most book laws are 🟠:
authors rarely publish audited proof. The verdict weighs the levels, and a 🔴 law alone never
decides a no-go.

**What the files are.** Distilled decision rules written from reading notes and research
summaries, never the books' text. The field laws come from one founder's research log on why
people buy and what gets executed, anonymized. Personal finance and investing are out of scope.

## Tools

Code only where code beats the model: exact arithmetic, probabilities, and memory from one
conversation to the next. Judgment stays with the agent, written as markdown protocols. Every
tool has a manual fallback, so the skill still works where scripts cannot run.

- `scripts/journal.py`: the decision journal. Each verdict is logged with its cheapest test,
  its deadline and the number that decides; once the deadline passes, the skill asks what
  happened and builds the filter's own record (`stats`: tests actually run, tests met, laws
  cited in missed tests). The file lives outside the skill, in `~/.wealth-framework/`, and is
  never published.
- `scripts/channel_math.py`: expected replies and deals for a number of sends, and the
  probability of zero replies. Above 10%, a zero proves nothing (FLE-3).
- `scripts/money_model.py`: the 30-day rule, Client-Financed Acquisition and the LTGP:CAC
  bar for the number of people who deliver (MNY-1 to MNY-3), from gross profit, never revenue.
- `protocols/grill-offer.md`: judging an offer on the Value Equation. It rates each driver
  strong, medium or weak and names the weakest one; it gives no numeric score.
- `artifacts/offer-griller.html`: a form (French) the user can fill in to brief the agent
  before the grill.

## How it was checked

Before publication, the filter judged five past decisions whose outcomes were already known
(three failures, two successes), each in a separate blind session that saw only the skill and
the facts known on the decision day. Under a scoring rule written before the run, it was right on
five out of five (four on a strict reading).

**Read the conditions, not only the label.** All five verdicts came out "go with conditions":
the label did not separate the successes from the failures. What did was the conditions and the
cheapest test. In the three failures they named the real cause before it happened (follow-ups
never sent, inboxes that never reach the buyer, building before any money or written terms).
Only one success was independent, so this check measures above all the ability to foresee a
failure. The case files stay private: they describe a real person's business.

## Adding a book

Write `sources/<author>-<title>.md` in the format of `docs/SOURCE_FORMAT.md`, add its rules to
`cheatsheet.md` where they change a decision, run `python scripts/build_glossary.py`, list it in
`SKILL.md` and `CHANGELOG.md`, and open a pull request.

## Tests

```bash
pip install pytest
pytest tests
```

`tests/test_sync.py` runs the update script against real git repositories (a local remote and
clones): up to date, behind, a merged branch left checked out, local edits, offline, copied
install, wrong remote. `tests/test_tools.py` checks the arithmetic of `money_model.py` and
`channel_math.py`, and the journal's full loop (log, due, close, record, damaged lines).

## License

MIT. Book titles and law names belong to their authors; the files contain paraphrased decision
rules, not excerpts.
