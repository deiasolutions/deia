# Railway Platform Patterns

Platform-specific solutions for Railway deployment issues.

## Known Issues & Solutions

### HTTPS Redirect Issues
- **Problem:** Railway edge proxy rewrites HTTPS to HTTP in redirect Location headers
- **Solution:** [https-redirect-middleware.md](./https-redirect-middleware.md)
- **Applies to:** FastAPI, Django, any framework generating redirects

## Contributing

Found a Railway-specific issue and solution? Contribute it here!

See `docs/bok-format-spec.md` for format guidelines.
