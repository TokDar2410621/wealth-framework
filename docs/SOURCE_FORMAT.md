# Source file format

Each file in `sources/` distills ONE source family (a book, or a family of field laws) into
decision rules the filter can apply. Adding a book later (the Fold-in procedure) produces one
more file in this exact format.

```markdown
# <Full title> (<Author>, <year>)

**Covers:** <3 to 6 topics>. **Use for:** <which decisions this source judges>.
**Provenance:** <how the knowledge reached the brain: book notes, web research summary, field sessions>; synced <YYYY-MM-DD>.

## Laws

### <ID>-<n> <Exact canonical name> <level>
- **Rule:** When <situation>, <do or judge> <X>, because <Z>.
- **Violation tells:** <observable signs that an idea breaks this law>.
- **Cheapest check:** <the smallest market test or measurement that settles it> (omit if none).
- **Source:** <book, chapter or page when known> or <field: what was lived, anonymized>.

(5 to 12 laws per file, the most decision-relevant first.)

## Thresholds and numbers
- <number or rule of thumb> (<level>, <source>)

## Anti-patterns
- **<name>:** <what it looks like> -> <why it fails>.

## Limits
- <criticisms; where this source is weak or contested>
```

## Evidence levels

- 🟢 **proven**: controlled study, audited data, public law.
- 🟠 **claimed**: stated by the author without audited proof, or observed once in the field.
- 🔴 **to test**: plausible but unverified; numbers taken from secondary summaries.

The verdict weighs them: breaking a 🟢 law weighs more than going against a 🔴 one.

## Rules

1. English. Keep the authors' exact names (Grand Slam Offer, Value Equation, CENTS, Rule of 100, radical truth).
2. Extract decision rules, not summaries. Write "When X, do Y, because Z".
3. Never copy book text. A canonical name, or a quote of one short sentence at most.
4. Public file: no names of clients, companies, products or people from the maintainer's life, no
   personal amounts (income, debt, net worth, prices charged), no city tied to a person. A lived
   case becomes generic: "a solo founder's SaaS: 12 months, $0 revenue".
5. Carry the level the brain note gives; never upgrade it. When a note flags a quote or a number
   as misattributed or unaudited, keep the flag.
6. No em-dash character anywhere.
7. Law IDs: HOR (Hormozi, $100M Offers), LDS (Hormozi, $100M Leads), THI (Thiel), DEM (DeMarco),
   KAW (Kawasaki), G48 (Greene, 48 Laws of Power), GHN (Greene, Laws of Human Nature),
   DAL (Dalio), FLE (field laws: execution and distribution), FLS (field laws: selling and offers),
   TAB (La Table: frameworks of the greats), MNY (Hormozi, $100M Money Models).
