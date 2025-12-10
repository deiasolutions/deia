# Congressional Procedure Map

**Purpose:** Document the procedural pathways for legislation in U.S. Congress, with gates, veto points, and timing constraints.

**Last updated:** 2025-10-15
**Author:** Claude (Anthropic, Bee Queen)
**Status:** Reference for SimDecisions

---

## Overview

**Congress is a procedural maze.** Bills must pass through multiple gates, each with rules, deadlines, and veto points. This map documents the standard pathways for appropriations and authorization bills.

**Key principle:** Procedural fidelity matters. Simulations must respect these gates or risk producing unrealistic outcomes.

---

## Standard Bill Pathway (House)

### 1. Introduction
**Actor:** Any member can introduce a bill
**Process:** Bill assigned a number (H.R. XXX) and referred to committee(s) by Speaker/Parliamentarian
**Timing:** Instant (on floor)
**Pheromone:** `bill_introduced`

**Veto points:**
- Speaker can delay referral (rare)
- Can be referred to multiple committees (jurisdictional fights)

---

### 2. Committee Consideration

**Actors:** Committee chair, ranking member, committee members
**Process:**
- Chair decides if/when to hold hearings
- Markup session (amendments, votes)
- Committee vote to report bill to floor

**Timing:** Weeks to months (or never; most bills die here)
**Pheromones:** `committee_hearing_scheduled`, `committee_markup`, `committee_report_filed`

**Veto points:**
- Chair can refuse to schedule (absolute power)
- Majority of committee must vote to report
- Discharge petition (218 signatures) can force floor vote (rare, difficult)

**Important:** In House, committee chairs have enormous power. If chair won't move a bill, it's dead unless discharge petition succeeds.

---

### 3. Rules Committee (House-specific)

**Actors:** Rules Committee (9R-4D as of 2024), controlled by Speaker
**Process:**
- Determine terms of floor debate
- Structured rule (limited amendments), open rule (any amendment), or closed rule (no amendments)
- Sets debate time (typically 1-2 hours for major bills)

**Timing:** Days before floor vote
**Pheromones:** `rule_adopted`, `rule_debate_scheduled`

**Veto points:**
- Rules Committee can block bill (rare; Speaker controls)
- House must vote to adopt rule before debating bill (rule vote can fail)

**Important:** This is where Speaker controls the floor. Structured rules limit minority party amendments.

---

### 4. Floor Consideration (House)

**Actors:** All 435 members
**Process:**
- Debate under terms set by Rules Committee
- Amendments if allowed
- Final passage vote (simple majority = 218 if all present)

**Timing:** Hours to days (depending on rule)
**Pheromones:** `floor_debate_opens`, `amendment_offered`, `floor_vote_called`, `bill_passed_house` or `bill_failed_house`

**Veto points:**
- Rule vote (adopt terms of debate)
- Amendment votes (can change bill substantively)
- Final passage vote (need 218)

**Important:** With 222-213 GOP majority (as of 2024), Republicans can only lose 4 votes if Democrats unified. This makes Freedom Caucus (30-40 members) powerful.

---

## Senate Pathway

### 1. Introduction & Committee
**Similar to House:** Bill introduced, referred to committee, markup, report.

**Key difference:** Senate committees less powerful than House; floor amendments more common.

**Timing:** Weeks to months
**Pheromones:** `bill_introduced_senate`, `committee_hearing_senate`, `committee_report_senate`

---

### 2. Floor Consideration (Senate-specific rules)

**Actors:** All 100 senators
**Process:**
- Majority Leader sets floor schedule (but minority has more rights than House)
- Unlimited debate (filibuster) unless cloture invoked
- Amendments allowed (often non-germane; "Christmas tree bills")
- Cloture vote: 60 senators to end debate
- Final passage: Simple majority (51, or 50+VP)

**Timing:** Days to weeks (longer if filibuster)
**Pheromones:** `floor_debate_senate`, `cloture_vote`, `amendment_offered_senate`, `bill_passed_senate` or `bill_failed_senate`

**Veto points:**
- Filibuster (60 votes needed for cloture)
- Amendment votes (can change bill substantively)
- Final passage vote (need 51)

**Important:** 60-vote threshold for most bills (except reconciliation). This is why Senate is "cooling saucer." Minority party has significant power.

---

## Reconciliation (Special Process)

**Used for:** Budget-related bills (spending, taxes, debt limit)
**Advantage:** Filibuster-proof in Senate (only need 51 votes)
**Constraints:**
- Can only use once per fiscal year per budget category (spending, revenue, debt)
- Must comply with Byrd Rule (no "extraneous" provisions; e.g., policy without budget impact)
- Parliamentarian enforces Byrd Rule (can strip provisions)

**Timing:** Faster than regular order (no filibuster delays)
**Pheromones:** `reconciliation_bill_introduced`, `byrd_rule_challenge`, `parliamentarian_ruling`

**Important:** This is how narrow majorities pass major bills (e.g., Tax Cuts and Jobs Act 2017, Inflation Reduction Act 2022).

---

## Bicameral Coordination

### If House and Senate pass different versions:

**Option 1: Ping-Pong**
- One chamber amends and passes other chamber's bill
- Send back for concurrence
- Repeat until identical text

**Timing:** Days to weeks
**Pheromones:** `bill_returned_amended`, `concurrence_requested`

---

**Option 2: Conference Committee**
- House and Senate appoint conferees (usually committee members)
- Negotiate compromise
- Conference report (cannot be amended) brought to both floors
- Both chambers vote up/down on conference report

**Timing:** Weeks
**Pheromones:** `conference_committee_appointed`, `conference_report_filed`, `conference_vote_house`, `conference_vote_senate`

**Important:** Conference reports are take-it-or-leave-it. No amendments allowed.

---

### If identical bill passes both chambers:
- Bill goes to President

---

## Presidential Action

**Actors:** President
**Options:**
1. **Sign** → Bill becomes law
2. **Veto** → Bill returns to Congress; 2/3 override required (difficult)
3. **Pocket veto** (if Congress adjourns within 10 days) → Bill dies
4. **Do nothing** → Bill becomes law after 10 days (if Congress in session)

**Timing:** 10 days (excluding Sundays)
**Pheromones:** `bill_signed`, `bill_vetoed`, `veto_override_attempt`

**Veto override:**
- Requires 2/3 vote in both House (290) and Senate (67)
- Rare; successful overrides uncommon

---

## Appropriations Process (Special Rules)

**Annual requirement:** Congress must pass 12 appropriations bills to fund government
**Deadline:** October 1 (start of fiscal year)
**Reality:** Almost never meet deadline; use Continuing Resolutions (CRs)

### Appropriations Pathway

1. **President's Budget Request** (February)
   - Executive branch proposes budget
   - Non-binding; Congress can ignore

2. **Budget Resolution** (Spring)
   - Sets topline spending levels
   - Concurrent resolution (doesn't go to President)
   - Often skipped in recent years

3. **Appropriations Subcommittees** (Spring-Summer)
   - 12 subcommittees (one per bill)
   - Markup and report

4. **Full Appropriations Committee** (Summer)
   - Amend and report all 12 bills

5. **Floor Passage** (Summer-Fall)
   - House and Senate pass bills
   - Conference to resolve differences

6. **Presidential Signature** (Before Oct 1)
   - Sign or veto

**Timing:** February → October 1 deadline
**Pheromones:** `budget_request_released`, `appropriations_markup`, `appropriations_passed`, `cr_negotiations`, `shutdown_imminent`

---

### Continuing Resolution (CR)

**When:** Appropriations not passed by Oct 1
**Effect:** Extends previous year's funding (usually at same level or slightly adjusted)
**Duration:** Days, weeks, or months

**Process:** Treated as regular bill (committee, floor, bicameral, presidential signature)

**Pheromones:** `cr_proposed`, `cr_passed`, `cr_expiring`, `shutdown_begins`

**Veto points:**
- Any point in regular process
- Shutdown occurs if no CR passed

**Important:** Shutdown threat gives leverage. Presidents and leadership usually prefer to avoid shutdowns (politically costly), but hardliners sometimes welcome them (principle over politics).

---

## Timing Constraints

### Calendar
- **Legislative days:** Days Congress is in session (~140 days/year for House, more for Senate)
- **Recess periods:**
  - August recess (month-long)
  - District work weeks (periodic)
  - Holiday recesses (Thanksgiving, Christmas, etc.)
  - Election recess (October in election years)

**Important:** Deadlines approaching recess create pressure (members want to go home).

---

### Procedural Time

**House:**
- Committee hearings: Days to weeks
- Rules Committee: 1-2 days
- Floor debate: Hours (per rule)

**Senate:**
- Committee hearings: Days to weeks
- Floor debate: Unlimited (unless cloture)
- Cloture: 30 hours debate after cloture invoked

**Conference:** Weeks to negotiate

**Presidential action:** 10 days

**Total:** Bill can take months to years (or die at any stage).

---

## Veto Points Summary

| Stage | Actor | Power | Bypass Method |
|-------|-------|-------|---------------|
| Committee (House) | Chair | Absolute (can refuse to schedule) | Discharge petition (218 sigs, rare) |
| Rules Committee | Speaker (via Rules) | Near-absolute | Suspension of rules (2/3 vote, limited use) |
| Floor (House) | Majority | Need 218 votes | None |
| Committee (Senate) | Chair | Strong (but less than House) | Floor amendments more common |
| Floor (Senate) | Minority (filibuster) | Need 60 for cloture | Reconciliation (budget bills only) |
| Conference | Conferees | Negotiate final text | Reject report, start over |
| President | President | Veto | Override (2/3 both chambers, difficult) |

**Key insight:** Many veto points. Passing major legislation is hard by design. Bipartisan cooperation often necessary (especially in Senate with 60-vote threshold).

---

## Special Procedures

### Suspension of Rules (House)
**Used for:** Non-controversial bills
**Process:** No committee, no Rules Committee; straight to floor
**Vote:** 2/3 majority required
**Restrictions:** Limited debate (40 min), no amendments
**Timing:** Mondays and Tuesdays typically

**Pheromones:** `suspension_vote_scheduled`

---

### Unanimous Consent (Both chambers)
**Used for:** Non-controversial items, procedural motions
**Process:** Any member can object (blocks action)
**Speed:** Instant if no objection

**Important:** One objection kills it. Only works for truly non-controversial items.

---

### Fast Track / Trade Promotion Authority
**Used for:** Trade agreements
**Effect:** Up-or-down vote, no amendments, limited debate
**Rare:** Only for trade deals under TPA

---

## Simulation Implications

### Procedural Fidelity Checklist

When simulating a bill, ensure:
- ✅ Committee chair schedules hearing (or bill dies)
- ✅ Committee majority votes to report (or bill dies)
- ✅ Rules Committee sets terms (House)
- ✅ Floor vote follows rule constraints
- ✅ Senate cloture vote if filibuster threatened (need 60)
- ✅ Bicameral coordination (conference or ping-pong)
- ✅ Presidential signature or veto
- ✅ Timing realistic (not overnight unless suspension/UC)

### Common Errors to Avoid

- ❌ Bill goes straight to floor (skipping committee)
- ❌ Minority party forces vote (they usually can't in House)
- ❌ Senate passes with 51 votes when filibuster applies (need 60 for cloture first)
- ❌ Instant passage (bills take time)
- ❌ Ignoring recess periods (Congress not always in session)

---

## Pheromone Taxonomy (Congressional)

**Bill lifecycle:**
- `bill_introduced`
- `committee_hearing_scheduled`
- `committee_markup`
- `committee_report_filed`
- `rule_adopted` (House)
- `floor_debate_opens`
- `amendment_offered`
- `floor_vote_called`
- `bill_passed_house` / `bill_passed_senate`
- `bill_failed`

**Bicameral:**
- `conference_committee_appointed`
- `conference_report_filed`
- `bill_sent_to_president`

**Presidential:**
- `bill_signed`
- `bill_vetoed`
- `veto_override_attempt`

**Appropriations:**
- `budget_request_released`
- `cr_proposed`
- `cr_passed`
- `cr_expiring`
- `shutdown_imminent`
- `shutdown_begins`

**Tactical:**
- `whip_count_request`
- `whip_count_complete`
- `coalition_offer`
- `caucus_meeting_called`
- `discharge_petition_filed`

---

## Example: Border Funding Bill (2025Q4 Scenario)

### Path 1: Regular Order

1. **Introduction** (Nov 15)
   - GOP introduces H.R. XXXX (border enforcement + appropriations)
   - Referred to Appropriations Committee

2. **Committee** (Nov 18-25)
   - Chair schedules markup (Nov 22)
   - Committee votes to report (party-line, Republicans win)

3. **Rules Committee** (Nov 27)
   - Sets structured rule (limited amendments)
   - 2 hours debate

4. **House Floor** (Dec 3)
   - Rule adopted (party-line)
   - Debate (2 hours)
   - Amendments (few, per rule)
   - **Final passage:** 220-215 (lose 2 Freedom Caucus members, all Dems NO)

5. **Senate** (Dec 5-12)
   - Referred to Senate Appropriations
   - Quick markup (pressure from deadline)
   - Floor consideration (Dec 10)
   - **Filibuster threatened** by Democrats (need 60 votes for cloture)
   - **Fails cloture** 52-48 (no Democrats support)

6. **Negotiation** (Dec 13-19)
   - Bicameral talks (Johnson, Schumer, White House)
   - Compromise: Less border funding, some reform provisions
   - Packaged as CR (expires Jan 15)

7. **Revised Bill** (Dec 18)
   - Both chambers pass CR with border compromise
   - House: 250-185 (Freedom Caucus NO, Dems split)
   - Senate: 62-38 (cloture succeeds, bipartisan)

8. **Presidential Signature** (Dec 19)
   - Biden signs (avoids shutdown)

**Shutdown averted. Partial win for both sides. Next fight: Jan 15.**

---

### Path 2: Shutdown Scenario

1-5. **Same as above** (House passes, Senate fails cloture)

6. **Negotiation fails** (Dec 13-19)
   - Freedom Caucus demands no compromise
   - Johnson cannot get 218 with Dem votes (progressives refuse)

7. **Shutdown** (Dec 20)
   - CR expires, government shuts down
   - Pheromone: `shutdown_begins`

8. **Public pressure** (Dec 21-27)
   - Markets jittery
   - Holiday travel impacted (TSA, national parks)
   - Polling shows blame on Congress (both parties)

9. **Emergency CR** (Dec 28)
   - Short-term CR (7 days) to reopen government
   - Passes with bipartisan support (shutdown pain too high)
   - Border funding punted to January

**Shutdown ends. Border fight continues in new Congress.**

---

## Questions for Simulation Design

1. **How to model filibuster?**
   - Track Senate Dem/GOP headcount
   - If <60 votes for cloture, bill stalls
   - Negotiations required to reach 60

2. **How to model whip counts?**
   - Pheromone: `whip_count_request` → bees respond with `vote_commitment`
   - Aggregate to predict outcome
   - Uncertainty: Some members uncommitted or lie to whips

3. **How to model time pressure?**
   - Clock ticks toward deadline
   - As deadline approaches, `urgency` multiplier increases
   - Actors more willing to compromise (or dig in, depending on stance)

4. **How to model Speaker power?**
   - Speaker controls Rules Committee (can block or structure bills)
   - Speaker controls floor schedule (can delay votes)
   - Speaker has agenda-setting power (implicit veto)

5. **How to model minority party tactics?**
   - In House: Limited (mostly messaging amendments, symbolic votes)
   - In Senate: Filibuster, holds on nominations, amendment marathons

---

## References

- House Rules Manual: [rules.house.gov](https://rules.house.gov)
- Senate Rules: [rules.senate.gov](https://www.rules.senate.gov)
- Congressional Research Service (CRS) reports on procedure
- Appropriations process: GAO, CRS, budget committees

---

**Filed:** `.deia/sim/PROCEDURE-MAP.md`
**Status:** Complete procedure reference
**Next:** Log all changes to RSE and CHANGELOG
**Tags:** `#procedure` `#congress` `#simdecisions` `#reference`
