# Book of Knowledge (BOK)

Community-contributed patterns, anti-patterns, and platform-specific solutions from AI-assisted development.

## Organization

### `platforms/`

Platform-specific workarounds, solutions, and best practices.

#### AI Models (`platforms/ai-models/`)
Best practices for different AI models - what makes each one shine:
- **[claude/](platforms/ai-models/claude/)** - Iterative refinement, Constitutional AI, nuanced reasoning
- **[gpt/](platforms/ai-models/gpt/)** - Function calling, speed, o1 reasoning
- **[gemini/](platforms/ai-models/gemini/)** - Massive context (1M tokens), multimodal, code execution
- **[copilot/](platforms/ai-models/copilot/)** - Inline completion, IDE integration, test generation

#### Deployment Platforms (`platforms/deployment/`)
Deployment platform workarounds and patterns:
- **[railway/](platforms/deployment/railway/)** - Railway deployment patterns, HTTPS redirects
- **[vercel/](platforms/deployment/vercel/)** - Vercel preview and production deployments
- Future: AWS, Azure, GCP, etc.

#### Tools (`platforms/tools/`)
AI-assisted development tools:
- **[claude-code/](platforms/tools/claude-code/)** - Slash commands, hooks, logging integration
- Future: Cursor, VS Code extensions, etc.

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
