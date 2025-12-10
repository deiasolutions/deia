# Context Loader - Service Documentation

**Service:** Context Loader
**Module:** `src/deia/services/context_loader.py`
**Purpose:** Intelligent context management for DEIA AI interactions
**Status:** Production-ready (90% test coverage)
**Created:** 2025-10-18
**Author:** CLAUDE-CODE-002 (Documentation Systems Lead)

---

## Overview

The Context Loader is a core DEIA service that intelligently assembles contextual information from multiple sources to enhance AI interactions. It loads, prioritizes, and manages context windows with security, performance, and memory efficiency.

### Key Features

- **Multi-source loading** - Files, BOK patterns, sessions, preferences, project structure
- **Intelligent prioritization** - Relevance scoring and source ranking
- **Memory management** - Configurable size limits and automatic truncation
- **Performance optimization** - Caching with TTL, lazy loading
- **Security integration** - PathValidator and FileReader for safe file access
- **Fast assembly** - Typical context assembly <100ms

---

## When to Use Context Loader

Use Context Loader when you need to:

- Assemble rich context for AI prompts
- Load project-specific information dynamically
- Combine multiple context sources (files + patterns + sessions)
- Enforce memory/size constraints on context
- Cache frequently accessed context for performance
- Maintain security boundaries during context loading

---

## Quick Start

### Basic Usage

```python
from src.deia.services.context_loader import ContextLoader

# Initialize with project root
loader = ContextLoader(project_root="/path/to/deia/project")

# Load context from multiple sources
context = loader.load_context(
    include_files=["README.md", "pyproject.toml"],
    include_patterns=["testing", "error-handling"],
    include_sessions=3,
    include_preferences=True,
    max_size_bytes=50000
)

# Use the assembled context
print(f"Loaded {context.source_count} sources ({context.total_size} bytes)")
print(f"Assembly time: {context.assembly_time_ms}ms")

for source in context.sources:
    print(f"- {source.source_type}: {source.path} ({source.relevance_score})")
```

### Output Example

```
Loaded 6 sources (12450 bytes)
Assembly time: 45ms
- file: /path/to/project/README.md (1.0)
- file: /path/to/project/pyproject.toml (1.0)
- pattern: /path/to/project/bok/testing.md (0.9)
- pattern: /path/to/project/bok/error-handling.md (0.9)
- session: /path/to/project/.deia/sessions/20251018-123456.md (0.7)
- preferences: /path/to/project/.deia/config.yaml (0.5)
```

---

## Architecture

### Context Sources

The Context Loader supports five source types, prioritized in this order:

| Priority | Source Type | Relevance Score | Description |
|----------|-------------|-----------------|-------------|
| 1 (Highest) | **Files** | 1.0 | Explicitly requested project files |
| 2 | **BOK Patterns** | 0.9 | Relevant knowledge patterns |
| 3 | **Sessions** | 0.7 | Recent conversation history |
| 4 | **Preferences** | 0.5 | User configuration |
| 5 (Lowest) | **Structure** | 0.4 | Project directory overview |

**Priority Loading:** Higher priority sources load first. If size limit is reached, lower priority sources are excluded.

### Data Flow

```
┌─────────────────┐
│ User Request    │
│ (load_context)  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Security Validation     │
│ (PathValidator)         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Source Loading          │
│ (Priority Order)        │
│                         │
│ 1. Files               │
│ 2. BOK Patterns        │
│ 3. Sessions            │
│ 4. Preferences         │
│ 5. Structure           │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Relevance Filtering     │
│ Size Limit Enforcement  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Context Window Assembly │
│ (ContextWindow object)  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│ Return to User  │
└─────────────────┘
```

---

## API Reference

### ContextLoader Class

#### `__init__(project_root, max_context_size=102400, cache_ttl=300, enable_caching=True)`

Initialize Context Loader.

**Parameters:**
- `project_root` (str): Absolute path to DEIA project root
- `max_context_size` (int): Maximum context size in bytes (default: 100KB)
- `cache_ttl` (int): Cache time-to-live in seconds (default: 300s)
- `enable_caching` (bool): Enable/disable caching (default: True)

**Raises:**
- `ValueError`: If project_root doesn't exist or is not a directory

**Example:**
```python
loader = ContextLoader(
    project_root="/path/to/project",
    max_context_size=50000,    # 50KB limit
    cache_ttl=600,             # 10 minute cache
    enable_caching=True
)
```

---

#### `load_context(...)`

Load and assemble context from multiple sources.

**Parameters:**
- `include_files` (List[str], optional): File paths to include (relative to project root)
- `include_patterns` (List[str], optional): BOK pattern IDs or search queries
- `include_sessions` (int, optional): Number of recent sessions to include (default: 0)
- `include_preferences` (bool, optional): Include user preferences (default: False)
- `include_structure` (bool, optional): Include project structure (default: False)
- `max_size_bytes` (int, optional): Maximum total size (overrides instance default)
- `relevance_threshold` (float, optional): Minimum relevance score 0.0-1.0 (default: 0.0)

**Returns:**
- `ContextWindow`: Assembled context window with sources and metadata

**Example:**
```python
context = loader.load_context(
    include_files=["src/main.py", "tests/test_main.py"],
    include_patterns=["unit-testing", "mocking"],
    include_sessions=2,
    include_preferences=True,
    max_size_bytes=30000,
    relevance_threshold=0.6  # Only sources with relevance >= 0.6
)
```

---

#### `clear_cache()`

Clear all cached data.

**Example:**
```python
loader.clear_cache()
```

---

#### `get_cache_stats()`

Get cache performance statistics.

**Returns:**
- `Dict`: Cache statistics including hits, misses, hit rate

**Example:**
```python
stats = loader.get_cache_stats()
print(f"Cache hit rate: {stats['hit_rate_percent']}%")
print(f"Total entries: {stats['entries']}")
```

**Output:**
```python
{
    'enabled': True,
    'entries': 5,
    'hits': 42,
    'misses': 18,
    'hit_rate_percent': 70.0,
    'ttl_seconds': 300
}
```

---

#### `is_deia_project()`

Check if current directory is a DEIA project.

**Returns:**
- `bool`: True if `.deia/` directory exists

**Example:**
```python
if loader.is_deia_project():
    print("Valid DEIA project")
```

---

#### `get_config()`

Get current configuration.

**Returns:**
- `Dict`: Configuration settings

**Example:**
```python
config = loader.get_config()
print(config['max_context_size'])
print(config['cache_ttl'])
```

---

### ContextWindow Dataclass

Result of context loading operation.

**Attributes:**
- `sources` (List[ContextSource]): List of loaded context sources
- `total_size` (int): Total size in bytes
- `source_count` (int): Number of sources
- `assembly_time_ms` (int): Assembly time in milliseconds
- `truncated` (bool): Whether context was truncated
- `summary` (str): Human-readable summary

**Methods:**
- `to_dict()`: Convert to dictionary for serialization

---

### ContextSource Dataclass

Represents a single context source.

**Attributes:**
- `source_type` (str): Type (file, pattern, session, preferences, structure)
- `content` (str): The actual content
- `path` (str): File path or identifier
- `relevance_score` (float): Relevance score 0.0-1.0
- `size_bytes` (int): Content size in bytes
- `metadata` (Dict): Additional metadata

**Methods:**
- `to_dict()`: Convert to dictionary for serialization

---

## Usage Examples

### Example 1: Loading Project Files

```python
from src.deia.services.context_loader import ContextLoader

loader = ContextLoader("/path/to/project")

# Load specific project files
context = loader.load_context(
    include_files=[
        "README.md",
        "src/main.py",
        "tests/test_main.py"
    ]
)

# Access loaded content
for source in context.sources:
    if source.source_type == "file":
        print(f"File: {source.path}")
        print(f"Size: {source.size_bytes} bytes")
        print(f"Content preview: {source.content[:100]}...")
```

---

### Example 2: Loading BOK Patterns

```python
# Load relevant patterns for current task
context = loader.load_context(
    include_patterns=[
        "error-handling",
        "logging-best-practices",
        "unit-testing"
    ]
)

# Extract pattern content
for source in context.sources:
    if source.source_type == "pattern":
        pattern_id = source.metadata.get("pattern_id")
        print(f"Pattern: {pattern_id}")
        print(f"Relevance: {source.relevance_score}")
```

---

### Example 3: Mixed Context with Size Limit

```python
# Load comprehensive context with size constraint
context = loader.load_context(
    include_files=["README.md", "CONTRIBUTING.md"],
    include_patterns=["code-review", "git-workflow"],
    include_sessions=3,
    include_preferences=True,
    include_structure=True,
    max_size_bytes=25000  # 25KB limit
)

print(f"Summary: {context.summary}")
print(f"Total size: {context.total_size} bytes")
print(f"Truncated: {context.truncated}")
print(f"Assembly time: {context.assembly_time_ms}ms")
```

---

### Example 4: Relevance Filtering

```python
# Only load highly relevant context
context = loader.load_context(
    include_files=["src/core.py"],
    include_patterns=["architecture", "design-patterns"],
    include_sessions=5,
    relevance_threshold=0.8  # Only relevance >= 0.8
)

# All sources will have relevance >= 0.8
# (excludes sessions=0.7, preferences=0.5, structure=0.4)
```

---

### Example 5: Cache Management

```python
loader = ContextLoader("/path/to/project", cache_ttl=600)

# First call - cache miss
context1 = loader.load_context(include_structure=True)

# Second call - cache hit (fast)
context2 = loader.load_context(include_structure=True)

# Check cache performance
stats = loader.get_cache_stats()
print(f"Hit rate: {stats['hit_rate_percent']}%")

# Clear cache if needed
loader.clear_cache()
```

---

## Configuration

### Default Settings

```python
DEFAULT_MAX_CONTEXT_SIZE = 102400  # 100KB
DEFAULT_CACHE_TTL = 300  # 5 minutes
MAX_FILES_PER_LOAD = 50  # Maximum files in single load
```

### Custom Configuration

```python
# Low-memory configuration
loader = ContextLoader(
    project_root="/path/to/project",
    max_context_size=25000,   # 25KB limit
    cache_ttl=120,            # 2 minute cache
    enable_caching=True
)

# High-performance configuration
loader = ContextLoader(
    project_root="/path/to/project",
    max_context_size=500000,  # 500KB limit
    cache_ttl=900,            # 15 minute cache
    enable_caching=True
)

# No caching (always fresh)
loader = ContextLoader(
    project_root="/path/to/project",
    enable_caching=False
)
```

---

## Performance Considerations

### Caching Strategy

**When cache helps:**
- Project structure (rarely changes)
- BOK patterns (static content)
- Preferences (infrequent updates)

**When cache doesn't help:**
- Session history (always changing)
- Dynamic file content

**Cache invalidation:**
- Automatic after TTL expires
- Manual via `clear_cache()`

### Size Limits

**Why size limits matter:**
- AI models have token limits
- Memory constraints
- Network bandwidth (if sending context remotely)

**Best practices:**
- Start with default 100KB
- Adjust based on use case
- Monitor `truncated` flag
- Use `relevance_threshold` to filter

### Assembly Performance

**Typical assembly times:**
- Small context (1-5 files): <50ms
- Medium context (5-20 files): 50-200ms
- Large context (20-50 files): 200-500ms

**Optimization tips:**
- Enable caching for static content
- Use `max_size_bytes` to limit scope
- Apply `relevance_threshold` early
- Limit `include_sessions` count

---

## Security Model

Context Loader integrates with DEIA's security services:

### PathValidator Integration

All file paths validated through `PathValidator`:
- ✅ Blocks directory traversal (`../` attacks)
- ✅ Enforces project boundary
- ✅ Blocks sensitive files (.env, .git, credentials)
- ✅ Resolves symlinks safely

### FileReader Integration

All file reads through `FileReader`:
- ✅ Size limit enforcement (1MB per file)
- ✅ Binary file detection
- ✅ Encoding handling
- ✅ Permission checks

**Result:** Context Loader cannot be used to access unauthorized files.

---

## Troubleshooting

### Problem: Empty context returned

**Possible causes:**
1. Invalid `project_root` path
2. Files don't exist
3. Security validation blocking files
4. Size limit too small

**Solutions:**
```python
# Check if DEIA project
if not loader.is_deia_project():
    print("Not a DEIA project - run 'deia init'")

# Check configuration
config = loader.get_config()
print(f"Max size: {config['max_context_size']}")

# Try without size limit
context = loader.load_context(
    include_files=["README.md"],
    max_size_bytes=None  # Use instance default
)
```

---

### Problem: Context truncated unexpectedly

**Cause:** Total size exceeds `max_size_bytes`

**Solutions:**
```python
# Increase size limit
context = loader.load_context(
    include_files=files,
    max_size_bytes=200000  # 200KB instead of 100KB
)

# Or reduce sources
context = loader.load_context(
    include_files=files[:10],  # Fewer files
    include_sessions=1  # Fewer sessions
)

# Or use relevance filtering
context = loader.load_context(
    include_files=files,
    relevance_threshold=0.8  # Only high-relevance sources
)
```

---

### Problem: Slow context assembly

**Possible causes:**
1. Too many files
2. Large files
3. Cache disabled
4. Project structure scanning

**Solutions:**
```python
# Enable caching
loader = ContextLoader(project_root, enable_caching=True)

# Limit file count
context = loader.load_context(
    include_files=files[:20],  # Limit to 20 files
    include_structure=False    # Skip structure scan
)

# Check assembly time
if context.assembly_time_ms > 500:
    print("Slow assembly - consider reducing sources")
```

---

### Problem: Cache not working

**Check cache status:**
```python
stats = loader.get_cache_stats()

if not stats['enabled']:
    print("Caching is disabled")

if stats['hit_rate_percent'] < 10:
    print("Low hit rate - may need longer TTL")
    # Increase TTL
    loader = ContextLoader(project_root, cache_ttl=900)
```

---

## Integration Examples

### Integration with Enhanced BOK Search

```python
from src.deia.services.context_loader import ContextLoader
from src.deia.services.enhanced_bok_search import EnhancedBOKSearch

loader = ContextLoader("/path/to/project")
bok_search = EnhancedBOKSearch("/path/to/index.json")

# Search BOK for relevant patterns
results = bok_search.search("error handling", top_n=5)

# Load patterns into context
pattern_ids = [r.pattern_id for r in results]
context = loader.load_context(include_patterns=pattern_ids)

print(f"Loaded {context.source_count} relevant patterns")
```

---

### Integration with Session Logger

```python
from src.deia.services.context_loader import ContextLoader
from src.deia.services.session_logger import SessionLogger

loader = ContextLoader("/path/to/project")
session_logger = SessionLogger(agent_id="agent-001")

# Load recent session context
context = loader.load_context(include_sessions=3)

# Log context loading event
session_logger.log_tool_call(
    tool_name="context_loader",
    params={"sources": context.source_count},
    duration_ms=context.assembly_time_ms
)
```

---

## Testing

Context Loader has comprehensive test coverage (90%):

**Test categories:**
- Initialization and configuration
- File loading (single, multiple, security)
- Pattern loading
- Session loading
- Preference loading
- Structure loading
- Mixed context assembly
- Caching behavior
- Size limit enforcement
- Edge cases

**Run tests:**
```bash
pytest tests/unit/test_context_loader.py -v --cov=src/deia/services/context_loader
```

---

## Related Documentation

- [PathValidator Security Model](../security/path-validator-security-model.md)
- [FileReader API](FILE-READER.md)
- [Enhanced BOK Search](ENHANCED-BOK-SEARCH.md)
- [Session Logger](SESSION-LOGGER.md)

---

## Version History

**v1.0** (2025-10-18)
- Initial implementation
- Multi-source loading
- Caching with TTL
- Security integration
- 90% test coverage

---

## Support

**Issues:** Report bugs to DEIA project issue tracker
**Questions:** See [FAQ](../FAQ.md)
**Contributing:** See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

**Service:** Context Loader
**Status:** Production-ready
**Coverage:** 90%
**Author:** CLAUDE-CODE-002
**Date:** 2025-10-18
