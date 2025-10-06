# Book of Knowledge (BOK)

Community-contributed patterns, anti-patterns, and platform-specific solutions from AI-assisted development.

## Organization

### `platforms/`
Platform-specific workarounds and solutions for vendor issues:
- **railway/** - Railway deployment patterns
- **vercel/** - Vercel preview and production deployments
- Future: AWS, Azure, GCP, etc.

### `patterns/`
General patterns that work across platforms:
- **collaboration/** - Human-AI collaboration patterns
- **governance/** - Project governance and safety
- **security/** - Security best practices
- **performance/** - Performance optimization patterns

### `anti-patterns/`
What NOT to do - documented mistakes and boundary violations

## How to Use

1. **Search by platform:** Need Railway help? Check `platforms/railway/`
2. **Search by category:** Need collaboration patterns? Check `patterns/collaboration/`
3. **Learn from mistakes:** Check `anti-patterns/` for what to avoid

## Contributing

All BOK entries use YAML frontmatter with:
- `title` - Entry name
- `platform` - Platform-Agnostic or specific (Railway, Vercel, etc.)
- `category` - Pattern, Anti-Pattern, etc.
- `tags` - Searchable keywords
- `confidence` - Validated, Experimental, etc.
- `date` - When pattern was discovered
- `source_project` - Where it came from

See `docs/bok-format-spec.md` for full format specification.

## License

All BOK entries: CC0-1.0 (Public Domain) - freely usable by anyone
