# Protocol: grill an offer (Value Equation)

Use when the user asks to score, grill or judge an offer, or pastes a brief from the Offer
Griller form (`artifacts/offer-griller.html`). This is judgment work: no script does it, and no
numeric score comes out of it. Multiplying four 1-to-10 guesses gives a precise-looking number
that the books do not support; what the Value Equation is good for is naming the weakest driver.

## 1. Collect the facts

Use the pasted brief if there is one: the user's self-ratings in it are claims to challenge, not
facts. Ask only for what is missing, one question at a time:

- who buys (one avatar) and the dream outcome in the buyer's own words;
- the main deliverable and the price;
- proof (cases, testimonials, numbers the user can show);
- time until the buyer sees a first result;
- what the buyer must do or give up;
- guarantee, bonuses, scarcity, the offer's name.

## 2. Rate each driver: strong, medium or weak

One line each, grounded only in the facts. A missing fact rates weak and is named as missing.

| Driver | Laws to open | Strong when |
|---|---|---|
| Dream outcome | HOR-2, HOR-3, HOR-7 | A result the buyer can picture, with its status gain and its timing |
| Perceived likelihood | HOR-5, FLS-4, FLS-6 | Lived proof, a specific self-triggering guarantee, one honest limit |
| Time delay | HOR-2, HOR-6 | A first visible result fast, with progress the buyer can see |
| Effort and sacrifice | HOR-2, LDS-7 | Done for the buyer; little to learn, decide or do |

## 3. Name the weakest driver

That is where the next unit of effort goes: fix it before adding features, bonuses or ads.

## 4. Grill

Brutal and specific, no flattery. Each hit names its law with ID and level and gives a concrete
fix. Typical hits: no guarantee or a vague one (HOR-5, FLS-2); bonuses that kill no objection
(HOR-9); invented scarcity (HOR-10, FLS-6); opening on the product instead of the pain (FLS-1);
priced as "cheaper" (FLS-3, HOR-4); an entry offer that loses money (MNY-4).

For the money side (CAC, 30-day profit, lifetime value), run
`python scripts/money_model.py` with the user's numbers; without scripts, compute 30-day gross
profit / CAC (1 passes, 2 is the target) and lifetime gross profit / CAC against 3, 6, 9 or 12
to 1 depending on how many people deliver the service (MNY-1 to MNY-3).

## 5. Close like any decision

End with the skill's decision output: the verdict (go, go with conditions, no-go) and the
cheapest test that checks the weakest driver with real buyers. Log it in the journal
(`scripts/journal.py add`). Answer in the user's language.

Never invent a fact, a number or a proof. A missing fact is never an assumed strength.
