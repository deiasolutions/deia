# Master Librarian - BOK Curation System

**Version:** 1.0
**Service:** `src/deia/services/master_librarian.py`
**Specification:** `.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md`
**Created:** 2025-10-18
**Author:** CLAUDE-CODE-004 (Documentation Curator)

---

## Overview

The **Master Librarian** is a knowledge curation system responsible for reviewing, validating, and organizing submissions to the DEIA Body of Knowledge (BOK). It ensures quality standards, prevents duplicates, and maintains semantic indexing for discoverability.

**Key Features:**
- Automated submission review and quality validation
- PII and secrets detection
- Duplicate pattern detection
- Semantic indexing with tags and metadata
- Pattern lifecycle management (active → deprecated)
- Integration with Enhanced BOK Search

---

## Quick Start

### Python API

```python
from deia.services.master_librarian import MasterLibrarian

# Initialize
librarian = MasterLibrarian()

# Review a submission
result = librarian.review_submission("2025-10-18/agent-bc/pattern.md")

if result.status == SubmissionStatus.ACCEPTED:
    # Integrate into BOK
    entry = librarian.integrate_submission("2025-10-18/agent-bc/pattern.md", result)
    print(f"Pattern integrated: {entry.title}")
else:
    print(f"Rejected: {result.reason}")
    print(f"Issues: {result.issues}")

# Search BOK
patterns = librarian.search_bok("git collaboration", category="Process")
for pattern in patterns:
    print(f"- {pattern.title} ({pattern.path})")
```

### CLI Usage

```bash
# Review submission
deia librarian review "2025-10-18/my-submission/pattern.md"

# Integrate approved submission
deia librarian integrate "2025-10-18/my-submission/pattern.md"

# Search BOK
deia librarian query "git collaboration"
deia librarian query --category "Anti-Pattern" deployment
deia librarian query --tags "windows,encoding"

# Get BOK statistics
deia librarian stats
```

---

## Submission Workflow

### Step 1: Create Submission

Create a dated directory in `.deia/intake/`:

```
.deia/intake/2025-10-18/my-submission/
├── pattern.md          # Your pattern content
└── MANIFEST.md         # Required metadata
```

### Step 2: Write MANIFEST.md

```markdown
# Submission Manifest

**Title:** Pattern: Git Workflow for Multi-Agent Collaboration
**Category:** Process
**Tags:** git, collaboration, multi-agent, coordination
**Author:** CLAUDE-CODE-002
**Date:** 2025-10-18
**Confidence:** Validated
**Source Project:** deiasolutions
**Platform:** Platform-Agnostic

**Summary:**
Describes a git workflow optimized for multiple AI agents working simultaneously on the same repository, including branch naming conventions, commit message standards, and merge strategies.

**Why this is valuable:**
Reduces merge conflicts by 80% based on project data. Provides clear attribution and easy rollback capabilities.
```

### Step 3: Submit for Review

The Master Librarian will review your submission based on:

**Quality Standards:**
- ✅ **Completeness** - Has context, examples, and clear explanation
- ✅ **Clarity** - Understandable in 5 minutes
- ✅ **Accuracy** - Technically correct, tested examples
- ✅ **Reusability** - Applicable beyond single project
- ✅ **Uniqueness** - Not a duplicate
- ✅ **Safety** - No PII, secrets, or malicious code

**Review Outcomes:**
- **ACCEPTED** - Integrated into BOK
- **REVISION_REQUESTED** - Minor issues, can be fixed
- **REJECTED** - Duplicate or low value
- **BLOCKED** - Contains PII/secrets (cannot accept)

### Step 4: Integration (if approved)

If accepted, the Master Librarian will:
1. Copy pattern to appropriate BOK directory
2. Add entry to `.deia/index/master-index.yaml`
3. Archive intake submission to `processed/`
4. Notify submitter of integration

---

## BOK Structure

Patterns are organized by category:

```
bok/
├── patterns/           # General patterns
├── anti-patterns/      # Things to avoid
├── processes/          # Workflows and procedures
├── platforms/          # Platform-specific gotchas
├── methodologies/      # Development approaches
├── governance/         # Governance and philosophy
└── federalist/         # Federalist Papers (governance)
```

---

## API Reference

### MasterLibrarian

Main class for BOK curation.

#### `__init__(project_root: Optional[Path] = None)`

Initialize Master Librarian.

**Args:**
- `project_root` - Root directory of DEIA project (auto-detected if None)

---

#### `review_submission(intake_path: str) -> ReviewResult`

Review a submission for quality and acceptance.

**Args:**
- `intake_path` - Relative path within `.deia/intake/` (e.g., `"2025-10-18/agent-bc/pattern.md"`)

**Returns:**
- `ReviewResult` with status, issues, suggestions, approved_path

**Example:**
```python
result = librarian.review_submission("2025-10-18/my-pattern/submission.md")

if result.status == SubmissionStatus.ACCEPTED:
    print(f"Approved! Will be saved to: {result.approved_path}")
elif result.status == SubmissionStatus.REVISION_REQUESTED:
    print("Minor issues found:")
    for issue in result.issues:
        print(f"  - {issue}")
else:
    print(f"Rejected: {result.reason}")
```

---

#### `integrate_submission(intake_path: str, review_result: ReviewResult, metadata: Optional[SubmissionMetadata] = None) -> IndexEntry`

Integrate an approved submission into BOK.

**Args:**
- `intake_path` - Relative path within `.deia/intake/`
- `review_result` - Result from `review_submission()` (must be ACCEPTED)
- `metadata` - Optional metadata (parsed from manifest if not provided)

**Returns:**
- `IndexEntry` for the newly integrated pattern

**Raises:**
- `ValueError` - If submission not accepted or path invalid

**Example:**
```python
result = librarian.review_submission("2025-10-18/my-pattern/pattern.md")

if result.status == SubmissionStatus.ACCEPTED:
    entry = librarian.integrate_submission("2025-10-18/my-pattern/pattern.md", result)
    print(f"Integrated: {entry.title}")
    print(f"Location: {entry.path}")
    print(f"ID: {entry.id}")
```

---

#### `search_bok(query: str, category: Optional[str] = None, tags: Optional[List[str]] = None) -> List[IndexEntry]`

Search BOK index by keywords, category, or tags.

**Args:**
- `query` - Search keywords (searched in title, summary, tags)
- `category` - Optional category filter (e.g., "Pattern", "Anti-Pattern")
- `tags` - Optional tag filter (matches any tag in list)

**Returns:**
- List of matching `IndexEntry` objects

**Example:**
```python
# Search for git patterns
results = librarian.search_bok("git collaboration")

# Filter by category
anti_patterns = librarian.search_bok("deployment", category="Anti-Pattern")

# Filter by tags
windows_patterns = librarian.search_bok("", tags=["windows", "encoding"])

# Display results
for pattern in results:
    print(f"{pattern.title}")
    print(f"  Path: {pattern.path}")
    print(f"  Summary: {pattern.summary}")
    print(f"  Tags: {', '.join(pattern.tags)}")
```

---

#### `deprecate_pattern(pattern_id: str, superseded_by: Optional[str] = None, reason: Optional[str] = None) -> bool`

Mark a pattern as deprecated.

**Args:**
- `pattern_id` - ID of pattern to deprecate
- `superseded_by` - Optional ID of replacement pattern
- `reason` - Optional deprecation reason

**Returns:**
- `True` if successful, `False` if pattern not found

**Example:**
```python
# Deprecate old pattern
success = librarian.deprecate_pattern(
    "old-git-workflow",
    superseded_by="multi-agent-git-workflow",
    reason="Replaced with multi-agent version"
)

if success:
    print("Pattern deprecated successfully")
```

---

#### `get_statistics() -> Dict[str, Any]`

Get BOK statistics.

**Returns:**
- Dictionary with BOK metrics

**Example:**
```python
stats = librarian.get_statistics()

print(f"Total patterns: {stats['total_patterns']}")
print(f"Active patterns: {stats['active_patterns']}")
print(f"By category: {stats['by_category']}")
print(f"By confidence: {stats['by_confidence']}")
print(f"Total tags: {stats['total_tags']}")
```

---

## Data Models

### SubmissionStatus

Enum for submission review status.

**Values:**
- `PENDING` - Not yet reviewed
- `ACCEPTED` - Approved for integration
- `REJECTED` - Not suitable for BOK
- `REVISION_REQUESTED` - Needs minor fixes
- `BLOCKED` - Contains PII/secrets (cannot accept)

---

### ConfidenceLevel

Enum for pattern maturity/confidence.

**Values:**
- `EXPERIMENTAL` - New idea, not yet proven
- `VALIDATED` - Tested in 1-2 projects
- `PROVEN` - Battle-tested across multiple projects

---

### IndexEntry

Entry in the master BOK index.

**Fields:**
- `id: str` - Unique identifier (kebab-case)
- `path: str` - Path to pattern file
- `title: str` - Pattern title
- `category: str` - Category (Pattern, Anti-Pattern, etc.)
- `tags: List[str]` - Searchable tags
- `confidence: str` - Confidence level
- `date: str` - Creation date (YYYY-MM-DD)
- `created_by: str` - Author ID
- `summary: str` - One-sentence description
- `source_project: Optional[str]` - Source project
- `platform: str` - Platform (default: Platform-Agnostic)
- `deprecated: bool` - Whether deprecated
- `superseded_by: Optional[str]` - Replacement pattern ID

---

### ReviewResult

Result of submission review.

**Fields:**
- `status: SubmissionStatus` - Review outcome
- `issues: List[str]` - Problems found
- `suggestions: List[str]` - Improvement recommendations
- `approved_path: Optional[str]` - Target BOK path (if accepted)
- `reason: Optional[str]` - Explanation of decision

---

## Quality Validation

The Master Librarian performs automatic quality checks:

### PII and Secrets Detection

Checks for:
- Email addresses
- API keys and tokens
- SSH/SSN patterns
- Credentials

**If detected:** Status = `BLOCKED` (cannot be fixed, must sanitize)

### Duplicate Detection

Checks for:
- Exact title matches (case-insensitive)
- High tag overlap (>70%) + similar titles

**If detected:** Status = `REJECTED` with pointer to existing pattern

### Completeness Checks

- MANIFEST.md present
- Required fields filled
- Minimum content length (200 characters)
- Examples provided (recommended)

---

## Integration with Enhanced BOK Search

The Master Librarian integrates seamlessly with Enhanced BOK Search for advanced discovery:

```python
from deia.services.enhanced_bok_search import EnhancedBOKSearch

# Combined usage
librarian = MasterLibrarian()
search = EnhancedBOKSearch()

# Add pattern via librarian
result = librarian.review_submission("2025-10-18/pattern.md")
if result.status == SubmissionStatus.ACCEPTED:
    entry = librarian.integrate_submission("2025-10-18/pattern.md", result)

# Search with advanced features (semantic, fuzzy)
patterns = search.semantic_search("colaboration")  # Finds "collaboration" with typo
```

---

## Curation Workflows

### Daily Review Workflow

1. Check `.deia/intake/` for new submissions
2. Review each submission:
   ```python
   result = librarian.review_submission(path)
   ```
3. For ACCEPTED submissions:
   - Integrate into BOK
   - Notify submitter
4. For REVISION_REQUESTED:
   - Create feedback file
   - Request changes
5. For REJECTED/BLOCKED:
   - Explain reason
   - Point to existing pattern (if duplicate)

### Pattern Lifecycle

1. **Submission** → Review → Integrate
2. **Active** → Used in projects
3. **Deprecated** → Superseded by newer pattern
4. **Archived** → Preserved for historical reference

---

## Troubleshooting

### Submission rejected as duplicate but it's different

**Solution:** Add more unique tags or clarify how it differs in the title/summary.

### PII detection false positive

**Solution:** Pattern correctly flagged - remove or sanitize the detected content.

### Integration fails with "path not found"

**Solution:** Ensure submission exists in `.deia/intake/` with correct path structure.

### Search returns no results

**Solution:**
- Check spelling
- Try broader keywords
- Use `search_bok("")` to see all patterns
- Check if pattern is deprecated

---

## Best Practices

### For Submitters

1. **Search first** - Check if pattern already exists
2. **Complete MANIFEST.md** - All required fields
3. **Add examples** - Code, diagrams, or use cases
4. **Test code** - Ensure examples work
5. **Clear title** - Descriptive and searchable
6. **Good tags** - 3-5 relevant keywords
7. **Summary** - One sentence explaining value

### For Curators

1. **Review within 48 hours** - Don't let submissions pile up
2. **Provide specific feedback** - Help submitters improve
3. **Update index regularly** - Keep taxonomy current
4. **Deprecate gracefully** - Point to replacement
5. **Track metrics** - Monitor BOK health
6. **Enforce quality** - Better to reject than accept low-quality

---

## Configuration

The Master Librarian auto-detects project structure but can be configured:

```python
from pathlib import Path

# Custom project root
librarian = MasterLibrarian(project_root=Path("/custom/path"))

# Access directories
print(f"Intake: {librarian.intake_dir}")
print(f"BOK: {librarian.bok_dir}")
print(f"Index: {librarian.index_path}")
```

---

## Related Tools

- **Enhanced BOK Search** - Advanced search with semantic, fuzzy matching
- **BOK Pattern Validator** - Validate pattern format and structure
- **Session Logger** - Track curation activities
- **Query Router** - Route queries to appropriate search tools

---

## Support

**Questions?** Check:
- Specification: `.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md`
- Tests: `tests/unit/test_master_librarian.py` (46 tests, 87% coverage)
- Source: `src/deia/services/master_librarian.py`

**Report issues:** Create observation in `.deia/observations/`

---

**Last Updated:** 2025-10-18
**Version:** 1.0
**Status:** Production-ready
