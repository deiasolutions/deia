# Phase 2 Complete Walkthrough

## What Phase 2 Delivers

Phase 2 makes DEIA smart about your actual work:

1. **Pattern Extraction** - Turn sessions into reusable patterns
2. **File Operations** - Chat understands your project structure
3. **BOK Integration** - Patterns inform your development

## End-to-End Workflow

### Scenario: You Hit a Problem

**1. Chat Session**
```
You: Our queries are timing out, ideas?
Chat: [Suggests solutions from BOK + your context]
You: That worked! Let me extract a pattern.
```

**2. Pattern Extraction**
```
deia extract session-001.md

✓ Extracted: Database Query Optimization
✓ Type: best_practice
✓ Sanitized: Removed project names
✓ Review: [Shows diff]
You: Approve → Submits to BOK
```

**3. BOK Indexed**
```
Pattern added to .deia/index/master-index.yaml
Next time, chat will reference it automatically
```

**4. Team Benefits**
```
Other team members ask similar questions
Chat: "This is covered in your BOK: database-indexing-001"
Time saved: Everyone learns from everyone
```

## Feature Breakdown

### Pattern Extraction Features

**Automatic Detection**
- Identifies problem/solution in chat
- Categorizes by pattern type
- Suggests tags

**Sanitization**
- Removes PII automatically
- Redacts secrets
- Makes pattern shareable

**Validation**
- Checks quality requirements
- Suggests improvements
- Prevents low-quality patterns

**Review Interface**
- Shows before/after sanitization
- Displays template formatting
- Allows approval/rejection

### File Operations Features

**Project Detection**
- Auto-finds `.deia/` directory
- Loads project metadata
- Caches for performance

**Context Loading**
- Reads governance documents
- Indexes BOK patterns
- Prepares smart responses

**Safe Access**
- Validates path boundaries
- Blocks directory traversal
- Protects sensitive files

**File Navigation**
- Breadcrumb trail
- Structure explorer
- Relevant patterns sidebar

## Key Improvements Over Phase 1

| Aspect | Phase 1 | Phase 2 |
|--------|---------|---------|
| Sessions | Logged | Can extract patterns |
| Chat | Generic | Project-aware |
| Files | No access | Safe structured access |
| BOK | Manual patterns | Auto-extracted patterns |
| Context | Limited | Full project context |

## Common Use Cases

### Use Case 1: Learn from Others' Solutions
```
You: How do you handle API rate limiting?
Chat: Your BOK has "rate-limiting-001" from Sarah's session
[Pattern includes her exact solution + reasoning]
Result: Immediate, tested solution
```

### Use Case 2: Build on Your Knowledge
```
You: Extract this debugging technique
Chat: Pattern created + added to your BOK
Tomorrow: [Someone else finds it automatically]
Result: Captured knowledge compounds
```

### Use Case 3: Onboard Faster
```
New team member: What's your error handling approach?
Chat: [Automatically provides 5 relevant BOK patterns]
Result: New member learns standards instantly
```

## Technical Highlights

### Pattern Extraction Engine
- Analyzes conversation flow
- Extracts key insights
- Generates structured output

### Sanitization System
- Regex-based PII detection
- Redaction with context hints
- Reversible for internal use

### File Operations Security
- Path traversal prevention
- Project boundary enforcement
- Encoding detection
- Sensitive file blocking

### BOK Integration
- Automatic indexing
- Fuzzy pattern matching
- Relevance scoring
- Cross-referencing

## Getting Maximum Value

### For Individuals
1. Extract patterns from meaningful sessions
2. Tag for easy discovery
3. Reference others' patterns
4. Keep BOK growing

### For Teams
1. Share patterns regularly
2. Use chat to find solutions
3. Build on each other's work
4. Document decisions

### For Projects
1. Capture domain knowledge
2. Speed up onboarding
3. Prevent repeated mistakes
4. Celebrate discoveries

## Next Steps

1. Try pattern extraction on your last chat session
2. Review the sanitization suggestions
3. Submit a pattern to your BOK
4. Reference it in future chats
5. Watch your team's knowledge compound

## Troubleshooting

**Patterns not extracted automatically**
- Session needs clear problem/solution
- Assistant responses should be actionable

**Chat not aware of project**
- Ensure `.deia/metadata.json` exists
- Check file permissions

**BOK patterns not showing in chat**
- Index may be out of date
- Try refreshing project context
- Verify pattern was added correctly

## Success Indicators

✓ Extracting 1+ patterns per day
✓ Team referencing BOK patterns in chat
✓ New problems solved by existing patterns
✓ Pattern suggestions appearing proactively
✓ Knowledge visible and accessible

You've captured institutional knowledge. That's Phase 2.
