---
name: wealth-framework
description: Business decision filter built from Hormozi ($100M Offers, $100M Leads, $100M Money Models), Thiel (Zero to One), DeMarco (The Millionaire Fastlane, CENTS), Greene (The 48 Laws of Power, The Laws of Human Nature), Kawasaki (The Art of the Start), Dalio (Principles), field-tested selling and execution laws, and founders' decision frameworks (Bezos, Paul Graham, Taleb, Musk). Use in EVERY business discussion - a business idea, an offer, a price, a choice between projects, an opportunity, a side hustle, prospecting, sales, pricing, monetization, upsells, recurring revenue, first customers, first $1,000, "should I launch X", "is it worth it". Also in French - idee de business, offre, prix, tarif, vendre, clients, prospection, projet, rentable, lancer, ca vaut le coup. When a decision is at stake, returns a go / go with conditions / no-go verdict with sourced, evidence-graded laws and the cheapest market test; otherwise adds at most three one-line insights, or stays silent. Always answers in the user's language.
---

# Wealth Framework

A decision filter for making money. It holds an idea, an offer or a choice up to the laws of
nine books, field-tested laws and the decision frameworks of great founders, then ends with the
cheapest test that lets the market decide. Every law carries its source and its evidence level.

## Step 0: freshness, once per conversation

Before the first use in a conversation, run:

```bash
python "<base directory of this skill>/scripts/sync.py"
```

Read the last line (JSON):

| `status` | Do |
|---|---|
| `up_to_date`, `updated` | Continue. If `skill_md_changed` is true, re-read this file first. |
| `read_origin_main` | Local edits exist: read files with `git -C <path> show origin/main:<file>` and tell the user. |
| `offline`, `not_a_clone` | Continue with the local files; say once "freshness not verified". |
| `error` | Tell the user and continue with the local files. |

Read through a skills catalog instead of a local folder (for example with `read-skill`): skip
this step, since the catalog's maintainer keeps it current, and open the files below through the
reference paths the catalog lists (with `read-note`), e.g. `.../wealth-framework/cheatsheet.md`.

## Language

Always answer in the user's language: French when the user writes French, English when they
write English. Keep law IDs and the authors' canonical names in English (Grand Slam Offer, CENTS).

## Pick the mode

- **Decision mode**: a decision is on the table. An idea to launch, an offer or a price to set,
  a choice between projects, an opportunity, quitting a job, signing a lease, hiring, raising
  money, "should I...". Run the five steps below and give a verdict.
- **Insight mode**: business talk with no decision to make (explaining, thinking aloud, planning).
  Add at most three laws, one line each: ID, level, and what it changes for the user's next move.
  If no law changes anything, add nothing. Never turn insight mode into an unrequested verdict.

## Decision mode: Dalio's five steps

1. **Goal.** What the user wants: amount, deadline, constraints (time, cash, skills). If unknown
   and it would change the verdict, ask ONE question; otherwise state your assumption.
2. **Problem.** Who has which problem, how urgent, and what stands between the idea and the goal.
3. **Diagnosis.** Run `cheatsheet.md` section 1 (first pass), then the sections that fit. Open
   the source file of every law you rely on and read its Rule and Violation tells: never cite a
   law from memory. List the laws respected and the laws broken, with ID and level.
4. **Verdict** (the design):
   - **no-go**: a law is broken at the root and no condition can fix it (no buyer in pain, no
     reachable channel, survival cash at stake, a copy entering interchangeable competition with
     no edge).
   - **go with conditions**: the broken laws are fixable; each condition names its law and the fix.
   - **go**: no material law broken; the test confirms it.
   Weigh the levels: 🟢 proven > 🟠 claimed or lived once > 🔴 to test. A 🔴 law alone never
   decides a no-go.
5. **Execution: the cheapest test.** One action, a deadline, and the number that decides
   ("20 conversations by Friday; 3 people who ask the price means continue"), plus what each
   outcome means. Prefer tests that ask the market (pre-selling, conversations, a manual first
   delivery) over tests that build.

**Two guards, at every decision:**
- **New toy?** Does this move the user toward their stated goal, or is it a new project that
  avoids executing the current plan? (GHN-4, GHN-5, FLE-1)
- **After a failed test: design or execution?** First check that the volume was really sent and
  the plan really followed. Execution failure: fix the volume, not the offer. Design failure (the
  volume was there and the market said no): fix the offer, the target or the price.
  (FLE-7, DAL-3, `sources/dalio-principles.md` "Design or execution?")

### Output (decision mode)

```markdown
**Verdict: go / go with conditions / no-go**: <one sentence why>

**Goal and problem:** <one or two lines>
**Laws respected:** <ID name level: why, one line each>
**Laws broken:** <ID name level: why, and the fix if there is one>
**Conditions:** <only for go with conditions>
**Cheapest test:** <action>, by <deadline>; <number> decides: if <result>, then <next move>.
**Guard:** <new toy or not, one line>
```

Keep it under about 250 words unless the user asks for more. Translate the labels into the
user's language.

## Agent-led offer scoring

The scripts do not score; they brief. When the user wants an offer scored
("grill my offer", "score this"), run the matching script and follow the brief it prints:

- `scripts/value_equation.py`: interviews the user about the offer (or takes the facts
  as arguments), then prints an agent brief. You score each Value Equation driver 1-10
  with justification, compute the score, name the weakest driver, and deliver the brutal
  "grill me" critique with fixes citing HOR-2 to HOR-10.
- `scripts/money_model.py`: collects the money-model numbers, then prints an agent brief.
  You judge the 30-day rule and the LTGP:CAC bar, then deliver the verdict with the fix
  order citing MNY-1 to MNY-10.

Read the brief, score from its facts only, never invent facts or numbers.

## Where the laws are

| File | IDs | Use for |
|---|---|---|
| `cheatsheet.md` | all | Start here: decision rules by situation, thresholds, warning phrases |
| `sources/hormozi-100m-offers.md` | HOR | Offer, price, value, guarantee, bonuses, scarcity |
| `sources/hormozi-100m-leads.md` | LDS | Getting leads: channels, Rule of 100, lead magnets |
| `sources/hormozi-100m-money-models.md` | MNY | Monetization: offer sequencing, 30-day rule, upsells, downsells, continuity |
| `sources/thiel-zero-to-one.md` | THI | Defensibility, competition, monopoly, distribution, secrets |
| `sources/demarco-millionaire-fastlane.md` | DEM | CENTS: is this a real business or a job in disguise? |
| `sources/kawasaki-art-of-the-start.md` | KAW | Meaning, market size, pitch, positioning copy |
| `sources/greene-48-laws-of-power.md` | G48 | Negotiation, attention, proof over argument |
| `sources/greene-laws-of-human-nature.md` | GHN | Buyer psychology and the founder's self-deception |
| `sources/dalio-principles.md` | DAL | The five-step skeleton, diagnosis, design or execution |
| `sources/field-laws-selling.md` | FLS | Field-tested selling: solutions, risk reversal, trust, asking |
| `sources/field-laws-execution.md` | FLE | Field-tested execution: focus, sending, follow-up, bottlenecks |
| `sources/la-table-frameworks.md` | TAB | Big decisions: runway, ruin, reversibility, control, timing |
| `glossary.md` | all | Every law by name |

## Rules

1. Cite only laws that exist in these files, with ID and level. Never invent a law, a number, a
   study or a quote. If no law covers the case, say so.
2. Keep the evidence levels: a 🔴 number is never presented as a fact.
3. Never recommend building more before a market test. The test asks the market.
4. Never suggest fake urgency or scarcity, invented testimonials, or contacting people without a
   legal basis (FLS-12 for Canada; elsewhere, check the local anti-spam law first).
5. Personal finance and investing are out of scope: no source here covers them. This is not
   legal, tax or investment advice.
6. Be direct. A no-go is said plainly, together with what would turn it into a go.

## Updating the skill (maintainer)

When asked to "update the wealth skill" with a new book or field note, follow the Fold-in
procedure: write `sources/<author>-<title>.md` in the exact format of `docs/SOURCE_FORMAT.md`
with a new ID prefix; add its rules to `cheatsheet.md` only where they change a decision; run
`python scripts/build_glossary.py`; add the file to the table above and to `CHANGELOG.md`; bump
the version; open a pull request. Never raise a law's level without new evidence.
