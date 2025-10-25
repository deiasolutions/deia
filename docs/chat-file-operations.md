# Chat File Operations Guide

## Overview

The DEIA chat interface is aware of your project structure and can safely read files within your DEIA project boundaries.

## Getting Started

### Auto-Detection
When you open chat in a DEIA project, it automatically:
1. Detects the `.deia/` directory
2. Loads project metadata
3. Reads governance documents
4. Indexes BOK patterns
5. Prepares context for smarter responses

### Project Context
Chat automatically includes:
- **Project name and phase**
- **Team members and recent decisions**
- **Relevant BOK patterns**
- **Project governance and rules**

## Reading Files

### Basic File Read
```
Chat: Can you review the database schema in src/schema.sql?
```

Chat will:
1. Validate path is within project
2. Read file with correct encoding
3. Provide analysis in context

### Security Boundaries

Chat respects project boundaries:
- ✓ Can read: `src/`, `docs/`, project files
- ✓ Can read: `.deia/governance/`, public patterns
- ✗ Cannot read: `.git/`, `.env`, outside project

### File Navigation

Use breadcrumb navigation to:
- View current file context
- Jump between related files
- Explore project structure
- Discover relevant patterns

## Context-Aware Responses

Chat provides better responses because it:
- **Knows your project structure**
- **Understands your team's decisions**
- **References your BOK patterns**
- **Respects your project constraints**

### Example

```
Chat: How should I handle database errors?

[Chat automatically searches BOK for error handling patterns]
[Finds project's error handling architecture doc]

Chat: Based on your project's architecture, you should...
[References your actual conventions]
```

## Working with Patterns

### Auto-Linking
When chat mentions a BOK pattern:
```
Chat: This is similar to "error-recovery-001"

[You can click to view the full pattern]
```

### Pattern Extraction
From chat conversations:
```
User: Extract a pattern from this conversation
Chat: Extracted "database-indexing" pattern
[Shows sanitized version for review]
```

## Best Practices

1. **Stay Within Project Scope**
   - Chat works best when context is available
   - Share files for analysis

2. **Use File References**
   - Reference files by path for clarity
   - Chat will find and read them

3. **Leverage BOK Context**
   - Chat mentions relevant patterns
   - Follow your team's documented approaches

4. **Review Sensitive Content**
   - Chat won't access `.env` or secrets
   - Review files before sharing with others

## Troubleshooting

**Chat can't find a file**
- Check path is relative to project root
- Verify file is within project boundaries
- Check file isn't in `.git/` or `.env`

**Project context not loading**
- Ensure `.deia/metadata.json` exists
- Check `.deia/index/master-index.yaml` is valid
- Verify permissions allow read access

**Pattern search returns no results**
- No BOK patterns match your query
- Add more patterns to BOK
- Be more specific in your question

## Advanced Usage

### Custom Context
You can provide additional context:
```
Chat: Here's the project spec: [file content]
[Chat uses provided context for analysis]
```

### Multi-File Analysis
Reference multiple files:
```
Chat: Compare src/old_version.py with src/new_version.py
[Chat reads both files and provides analysis]
```

### Pattern Discovery
Chat helps you:
- Identify extractable patterns from code
- Suggest BOK pattern locations
- Find related patterns for reference
