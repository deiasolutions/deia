# Persona Cards: Schema and Usage

**Purpose:** Model political actors as role-bounded bees within LLHs, with evidence-based stances, constraints, and coalition ties.

**Last updated:** 2025-10-15
**Author:** Claude (Anthropic, Bee Queen)

---

## Philosophy

### What We're Simulating

**We simulate ROLES, not BEINGS.**

- **Mike Johnson the person** = a being (consciousness, agency, rights)
- **Speaker of the House** = a role (procedural powers, constraints, observable patterns)

**Persona cards capture the role:** What powers does this role have? What constraints? What observable stance patterns? What coalitions?

### What We're NOT Simulating

- ❌ Inner thoughts, motivations, feelings (we can't know these)
- ❌ "The real person" (unknowable, unethical to claim)
- ❌ Predictions of specific actions (too deterministic)

### What We ARE Simulating

- ✅ Observable stance patterns (with citations)
- ✅ Procedural powers and constraints (rules-based)
- ✅ Coalition affiliations (documented relationships)
- ✅ Budget constraints (attention, capital, staff, time)
- ✅ Behavioral tendencies (based on historical evidence)

---

## Schema

### File Format

```markdown
# Persona: [Role Name]

**Actor ID:** `[unique-id]`
**Type:** `bee | drone | leftenant_queen`
**LLH Affiliation:** `[parent-llh-id]`
**Role:** `[procedural-role]`
**Last Updated:** `[YYYY-MM-DD]`

---

## Role Definition

### Procedural Powers
[What this role can do institutionally]

### Constraints
[What limits this role's actions]

### Responsibilities
[What this role is expected to do]

---

## Stance Graph

### Issue: [Issue Name]

**Position:** [Clear statement of position]

**Confidence:** [high | medium | low]

**Evidence:**
- [Citation 1] - "[Quote or summary]" - [Source, Date]
- [Citation 2] - "[Quote or summary]" - [Source, Date]

**Uncertainty Notes:** [Where evidence is weak or contradictory]

---

## Coalition Ties

### Primary Affiliations
- `[llh-id]` - [Description of relationship]

### Active TAG Teams
- `[tag-id]` - [Role in TAG team] - [TTL/expiry]

### Known Alliances
- `[actor-id]` - [Nature of alliance] - [Citations]

### Known Tensions
- `[actor-id]` - [Nature of tension] - [Citations]

---

## Constraints & Budgets

### Political Capital
**Current:** [estimate]
**Burn Rate:** [high | medium | low]
**Constraints:** [What limits spending]

### Attention Budget
**Current:** [estimate]
**Major Commitments:** [List of attention sinks]

### Procedural Constraints
**Calendar:** [Deadlines, recess periods]
**Rules:** [Specific procedural limits]
**Caucus Pressure:** [Internal coalition demands]

---

## Behavioral Tendencies

### Rhetoric Style
[Observable patterns in public communication]

### Coalition Building
[Historical patterns in forming alliances]

### Procedural Moves
[Preferred tactics for advancing agenda]

### Risk Tolerance
[high | medium | low] - [Evidence]

---

## Simulation Hooks

### Pheromone Emissions (Typical)
- `[pheromone-type]` - [When/why emitted]

### Response Patterns
- When `[pheromone-type]` detected → [typical response]

### Veto Points
- [Where this role can block processes]

### Amplification Factors
- [What gives this role outsized influence]

---

## Metadata

**Data Sources:**
- [List of primary sources used]

**Last Evidence Date:** [Most recent citation date]

**Confidence Score:** [Overall: high | medium | low]

**Maintenance Notes:** [What needs updating, gaps in evidence]

---

## Version History

**v0.1** - [Date] - Initial creation - [Author]
[Future updates logged here]
```

---

## Field Definitions

### Actor ID
**Format:** `house-speaker-mike-johnson` or `governor-tx-greg-abbott`

**Uniqueness:** Must be unique across all personas

**Stability:** Should remain stable even if person changes (role-based, not name-based)

### Type Classification

**bee:** Individual actor with decision-making authority within an LLH
- Examples: Speaker, Committee Chair, Governor

**drone:** Task-executor with limited autonomy
- Examples: Staff, junior members following leadership

**leftenant_queen:** Deputy with delegation authority, typically TTL-scoped
- Examples: Committee ranking member acting as shadow chair, whip with temporary authority

### LLH Affiliation

**Primary LLH:** The main institutional home
- `house-republican-llh`, `senate-democratic-llh`, `state-tx-llh`

**Multiple affiliations possible:**
- AOC: `house-democratic-llh` + `progressive-caucus-llh`

### Stance Graph Structure

**Issue taxonomy:**
- `immigration-border-security`
- `fiscal-budget-fy2025`
- `healthcare-medicaid-expansion`
- [Expandable, use kebab-case]

**Position statement:**
- Clear, concise (1-2 sentences)
- Observable from public statements
- NOT inferred/assumed

**Confidence levels:**
- **high:** Multiple consistent citations, clear public record
- **medium:** Some evidence, but gaps or ambiguity
- **low:** Inferred from general patterns, weak direct evidence

**Evidence format:**
- **[Source]** - "Direct quote or clear paraphrase" - [Publication, Date]
- Example: **[CNN]** - "I will not support any bill that doesn't include border wall funding" - [Interview, 2024-09-15]

**Uncertainty notes:**
- Where has this actor flip-flopped?
- Where is evidence contradictory?
- Where are we inferring from party line vs. direct statement?

### Coalition Ties

**Primary affiliations:** Long-term institutional memberships

**TAG teams:** Short-lived, issue-specific coalitions with TTL

**Alliances:** Documented working relationships
- "Frequently co-sponsors bills with [actor]"
- "Part of [informal group] coalition"

**Tensions:** Documented conflicts
- "Publicly criticized [actor] on [issue]"
- "Competing for [resource/position]"

### Budgets

**Political capital:** Goodwill, reputation, favors owed/owing
- High capital = can take unpopular stands
- Low capital = must follow caucus line

**Attention budget:** Media cycles, staff time, public focus
- High-profile roles (Speaker) have limited attention
- Can't be everywhere at once

**Procedural constraints:** Real-world limitations
- Committee hearing schedules
- Floor time limits
- Recess periods
- Caucus meeting requirements

### Behavioral Tendencies

**Based on historical patterns, NOT personality inference:**
- "Typically co-sponsors bipartisan bills on [topic]"
- "Has used procedural motion X in past Y times"
- "Media strategy emphasizes [platform/format]"

**Avoid psychological claims:**
- ❌ "Is cautious by nature"
- ✅ "Historical pattern: proposes amendments rather than opposing outright"

---

## Usage in Simulation

### Initialization

1. **Load persona card** into actor registry
2. **Assign to LLH(s)** based on affiliation
3. **Initialize budgets** from persona constraints
4. **Register pheromone hooks** from simulation section

### During Simulation

**Stance lookup:**
- When event involves [issue], check stance graph
- Use confidence level to determine certainty of response
- Respect uncertainty notes (may abstain if evidence weak)

**Coalition behavior:**
- Check coalition ties for likely allies/opponents
- TAG team membership determines temporary loyalties
- Alliances/tensions influence coordination

**Constraint checking:**
- Before action, verify budgets (capital, attention, time)
- Check procedural constraints (can this role do X?)
- Honor rules-of-the-game (no actions outside role powers)

**Pheromone emission:**
- Based on simulation hooks, emit appropriate signals
- Example: Speaker bee emits `floor_schedule_update` when setting calendar

### Updating Personas

**Evidence-driven only:**
- New public statement → update stance graph
- New coalition → update ties
- Changed constraints → update budgets/rules

**Version control:**
- Never overwrite; append to version history
- Log what changed and why (with citation)

**Uncertainty increases over time:**
- Old evidence becomes stale
- Mark stances as lower confidence if not recently reaffirmed

---

## Quality Standards

### Citation Requirements

**≥90% stance claims with sources**
- Every position statement needs ≥1 citation
- Prefer direct quotes over paraphrases
- Always include date (recency matters)

**Source diversity:**
- Mix of: direct statements, voting records, co-sponsorships, media interviews
- Avoid single-source bias

**Attribution:**
- Clear source (publication, hearing record, press release)
- Clear date (not just year, but month/day if available)
- URL if available (for verification)

### Abstention Over Hallucination

**If evidence weak:** Mark confidence as low, note gaps

**If no evidence:** Don't create stance; leave absent

**Better to abstain in simulation than to fabricate.**

### Procedural Fidelity

**Powers must be real:**
- Check House/Senate rules
- Verify committee authorities
- Confirm procedural precedents

**Constraints must be real:**
- Actual calendar deadlines
- Actual budget limitations
- Actual caucus rules

### Bias Mitigation

**Avoid partisan framing:**
- ❌ "Obstructs progress on immigration reform"
- ✅ "Opposes H.R. 1234 citing border security concerns"

**Neutral language:**
- Describe positions without endorsing/condemning
- Let evidence speak

**Multiple perspectives:**
- Include both supportive and critical sources where available
- Note where actor's view differs from consensus

---

## Examples

### High-Quality Stance Entry

```markdown
### Issue: immigration-border-security

**Position:** Supports increased border enforcement funding, opposes pathway to citizenship without border security measures first.

**Confidence:** high

**Evidence:**
- **[House Floor Speech]** - "We cannot consider any immigration reform that doesn't first secure our southern border" - [C-SPAN, 2024-08-22]
- **[Committee Hearing]** - Voted YES on H.R. 2 (border security bill), voted NO on H.R. 1234 (comprehensive reform) - [House Judiciary, 2024-07-15]
- **[Press Release]** - "Border security is national security" - [Official site, 2024-09-01]

**Uncertainty Notes:** Has not clearly stated position on DACA specifically; general statements suggest opposition to legalization without border security, but no direct quote on DACA.
```

### High-Quality Coalition Entry

```markdown
### Known Alliances
- `house-republican-whip-tom-emmer` - Works closely on whip operations; co-sponsored 12 bills in 118th Congress - [Congress.gov]
- `governor-tx-greg-abbott` - Public coordination on border policy; joint press conference 2024-08-30 - [Texas Tribune]
```

---

## A/B Testing Notes

### Track 001A: Curated Snapshot
- Hand-build 6-8 personas with deep citations
- Focus on believability over scalability
- Goal: First simulation run succeeds

### Track 001B: Adapter-First
- Structured schema enables automated parsing
- Consistent format across all personas
- Goal: Scale to 50+ personas efficiently

**Both tracks use this schema.**

---

## Maintenance Protocol

### Regular Updates
- When new evidence emerges (speeches, votes, statements)
- When coalitions shift (new TAG team, broken alliance)
- When constraints change (new committee assignment, election)

### Staleness Detection
- If last evidence >90 days old → flag for review
- If confidence high but no recent reaffirmation → lower confidence

### Community Contributions
- Anyone can fork, improve personas
- Pull requests with citations welcome
- Version history preserves all changes

---

## Ethical Commitments

### We Simulate Roles, Not Beings

**This bears repeating:** We model observable patterns in institutional roles, not the inner lives of human beings.

**Legal disclaimer:** These personas are approximations for simulation purposes, not claims about actual persons. All stances based on public evidence.

### Transparency

**All sources cited.** Anyone can verify.

**All uncertainty noted.** We don't hide gaps.

**All forkable.** Disagree with our persona? Build your own.

### No Targeted Persuasion

**Purpose:** Understanding system dynamics, not influencing individuals.

**Not for:** Campaign messaging, opposition research, manipulation.

**For:** Civic education, scenario planning, procedural understanding.

---

## Questions?

See: `.deia/personas/house/speaker-mike-johnson.md` for complete example.

See: `.deia/scenarios/2025Q4-border-funding-crisis.yaml` for usage in context.

---

**Filed:** `.deia/personas/README.md`
**Status:** Schema definition
**Next:** Build example personas
**Tags:** `#personas` `#simdecisions` `#schema` `#nokings` `#roles-not-beings`
