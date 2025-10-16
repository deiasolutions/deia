# Claude Knowledge Pipeline - Start Here

## Project Overview

This is a **self-improving knowledge extraction system** for Claude Code development sessions. The goal is to capture, analyze, and synthesize learnings from human-AI collaboration to:

1. Build a reusable Book of Knowledge (BOK) for Claude
2. Document meta-learnings about human/AI capabilities
3. Create publishable whitepapers to benefit the broader dev community

## Workflow Pipeline

```
intake/ → raw/ → reviewed/ → [logdump/ + bok/ + wisdom/]
```

### Directory Structure

- **intake/** - Raw conversation logs and files arrive here (unprocessed)
- **raw/** - Files after initial review
- **reviewed/** - Markdown files annotated with insights and learnings
- **logdump/** - Process logs documenting review work and BOK expansion
- **bok/** - Book of Knowledge - extracted knowledge bits for Claude to reference
- **wisdom/** - Meta-findings about human/AI collaboration for whitepapers

## How to Start a Session

1. **Read this file first** - You're doing it now!
2. **Check intake/** - Are there files waiting to be processed?
3. **Review BOK/** - Check for relevant knowledge from previous sessions
4. **Ask the human** - What are we working on today?

## How to End a Session

1. **Save the conversation** - Use `/save-session` command or manually export
2. **Update logs** - Document what was accomplished in logdump/
3. **Extract knowledge** - Add new learnings to bok/ if applicable

## Connected Projects

- **parentchildcontactsolutions/** - Primary development project that feeds logs into this pipeline

## Vision

Build a standardized approach for Claude Code sessions to:
- Automatically capture development insights
- Share sanitized findings with the community (GitHub)
- Create a collective knowledge base for better AI-assisted development

## Quick Commands

- `/save-session` - Save current conversation to intake folder

---

*Last updated: 2025-10-05*
