# Project Browser - DEIA Project Structure Navigator

**Service:** `src/deia/services/project_browser.py`
**Version:** 1.0
**Status:** Production-ready
**Test Coverage:** 89% (19 tests, all passing ✅)

---

## Overview

The **Project Browser** provides a safe, JSON-serializable API for navigating DEIA project structure. Designed for web interface integration with comprehensive filtering and search capabilities.

---

## Quick Start

```python
from deia.services.project_browser import ProjectBrowser

# Initialize (auto-detects project root)
browser = ProjectBrowser()

# Get tree view
tree = browser.get_tree(max_depth=3)
print(tree)

# Search for files
results = browser.search("pattern")
for result in results:
    print(f"{result['name']}: {result['path']}")

# Filter by extension
md_files = browser.filter_by_extension(['.md', '.txt'])
```

---

## API Reference

### `ProjectBrowser(project_root=None)`

Initialize Project Browser.

**Args:**
- `project_root` - Root directory of DEIA project (auto-detected if None)

**Raises:**
- `ValueError` - If `.deia/` directory not found

---

### `get_tree(path=None, max_depth=5, show_hidden=False)`

Generate tree view of project structure.

**Args:**
- `path` - Relative path from project root (None = entire project)
- `max_depth` - Maximum directory depth to traverse (default: 5)
- `show_hidden` - Include hidden files/directories (default: False)

**Returns:** Tree structure as nested dict

**Example:**
```python
tree = browser.get_tree(path=".deia", max_depth=2)
# {
#   "name": ".deia",
#   "type": "directory",
#   "children": [...],
#   "child_count": 8
# }
```

---

### `filter_by_extension(extensions, path=None)`

Find all files with specified extensions.

**Args:**
- `extensions` - List of extensions (e.g., `['.md', '.py']`)
- `path` - Relative path to search within (None = entire project)

**Returns:** List of file metadata dicts

**Example:**
```python
# Find all markdown and Python files
files = browser.filter_by_extension(['.md', '.py'])
# [
#   {"name": "README.md", "path": "README.md", "type": "file", "size": 1234, ...},
#   ...
# ]
```

---

### `search(query, file_types=None)`

Search for files/directories by name.

**Args:**
- `query` - Search string (case-insensitive, partial match)
- `file_types` - Optional list of extensions to limit search

**Returns:** List of matching items with metadata

**Example:**
```python
# Search for files containing "test"
results = browser.search("test")

# Search only Python test files
py_tests = browser.search("test", file_types=['.py'])
```

---

### `get_deia_structure()`

Get standardized `.deia/` directory structure with status.

**Returns:** Dict with directory status and contents

**Example:**
```python
structure = browser.get_deia_structure()
# {
#   "root": "/path/to/project",
#   "valid": True,
#   "directories": {
#     "bot-logs": {"exists": True, "file_count": 15, ...},
#     "federalist": {"exists": True, "file_count": 30, ...},
#     ...
#   }
# }
```

---

### `get_stats()`

Get project statistics.

**Returns:** Dict with file counts, sizes, and types

**Example:**
```python
stats = browser.get_stats()
# {
#   "total_files": 245,
#   "total_size": 1048576,
#   "by_extension": {
#     ".md": {"count": 45, "size": 123456},
#     ".py": {"count": 67, "size": 456789}
#   },
#   "by_directory": {...}
# }
```

---

### `to_json(obj, indent=2)`

Serialize to JSON string.

**Args:**
- `obj` - Object to serialize (tree, search results, etc.)
- `indent` - JSON indentation level

**Returns:** JSON string

**Example:**
```python
tree = browser.get_tree(max_depth=2)
json_str = browser.to_json(tree)
```

---

## Features

### Security
- ✅ Path validation (prevents directory traversal)
- ✅ Project boundary enforcement
- ✅ Permission error handling
- ✅ Safe for web interface use

### Performance
- ✅ Efficient traversal with depth limits
- ✅ Sorted results
- ✅ Handles large projects (100+ files tested)

### Flexibility
- ✅ Multiple search/filter methods
- ✅ Case-insensitive search
- ✅ Extension normalization (`.md` or `md` both work)
- ✅ JSON serialization for API use

---

## Use Cases

### Web Dashboard
```python
# API endpoint for project tree
@app.get("/api/project/tree")
def get_project_tree():
    browser = ProjectBrowser()
    tree = browser.get_tree(max_depth=3)
    return browser.to_json(tree)
```

### File Discovery
```python
# Find all patterns in BOK
browser = ProjectBrowser()
patterns = browser.filter_by_extension(['.md'], path='bok/patterns')
```

### Project Health Check
```python
# Verify .deia structure
browser = ProjectBrowser()
structure = browser.get_deia_structure()

missing = [name for name, info in structure['directories'].items()
           if not info['exists']]
if missing:
    print(f"Missing directories: {missing}")
```

---

## Test Coverage

**Coverage:** 89% (exceeds >80% requirement)
**Tests:** 19 comprehensive tests
**Status:** All passing ✅

**Test Coverage Includes:**
- Initialization and project root detection
- Tree generation with depth control
- Hidden file handling
- Extension filtering (single and multiple)
- Search functionality (basic and with file types)
- Case-insensitive search
- DEIA structure analysis
- JSON serialization
- Statistics generation
- Path validation and security
- Permission error handling
- Large directory handling
- Empty project handling

---

## File Metadata Format

All file operations return metadata in this format:

```python
{
    "name": "file.md",
    "path": "docs/file.md",  # Relative to project root
    "type": "file",  # or "directory"
    "size": 1234,  # bytes
    "extension": ".md",
    "modified": 1698765432.0  # Unix timestamp
}
```

---

## Error Handling

### Path Not Found
```python
try:
    tree = browser.get_tree(path="nonexistent")
except ValueError as e:
    print(f"Error: {e}")  # "Path does not exist: nonexistent"
```

### Outside Project Boundary
```python
try:
    tree = browser.get_tree(path="../outside")
except ValueError as e:
    print(f"Error: {e}")  # "Path does not exist: ../outside"
```

### Permission Denied
```python
tree = browser.get_tree()
# Permission errors are handled gracefully
# Node will have: {"error": "permission_denied"}
```

---

## Configuration

### Auto-Detection
```python
# Automatically finds project root by searching for .deia/
browser = ProjectBrowser()
```

### Explicit Root
```python
from pathlib import Path
browser = ProjectBrowser(project_root=Path("/custom/path"))
```

---

## Related Services

- **Enhanced BOK Search** - Advanced BOK pattern search
- **Master Librarian** - BOK curation and organization
- **Query Router** - Intelligent query distribution

---

## Future Enhancements

Potential improvements for future versions:

1. **Caching Layer** - Cache tree/search results with TTL
2. **Watch Mode** - File system watching for real-time updates
3. **Advanced Filtering** - Predicate-based filtering, size/date filters
4. **Performance** - Lazy loading for very large projects
5. **Export** - Export tree to various formats (XML, YAML)

Current implementation prioritizes **correctness and test coverage** over premature optimization.

---

## Troubleshooting

### "Not a DEIA project" error
**Solution:** Ensure `.deia/` directory exists in project root or parent directories.

### Search returns no results
**Solution:**
- Check spelling
- Try broader keywords
- Verify files exist: `browser.get_stats()`

### Tree is too deep
**Solution:** Adjust `max_depth` parameter to limit recursion.

---

**Last Updated:** 2025-10-19
**Status:** Production-ready
**Test Coverage:** 89%
