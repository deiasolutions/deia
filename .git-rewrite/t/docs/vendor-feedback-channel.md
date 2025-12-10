# Save Feedback for AI Vendor

Save this conversation for review by the AI vendor (Anthropic, OpenAI, Google).

**How it works:**
1. Choose vendor (Anthropic/OpenAI/Google)
2. Choose category (awesome/issues/feature-request)
3. Add brief description
4. DEIA saves to `~/.deia-global/vendor-feedback/`
5. Vendor can review (if you've granted access)

**Categories:**
- **awesome** - Model did amazing work, vendor should know
- **issues** - Model struggled, hallucinated, or missed context
- **feature-request** - Wish the model could do something it can't

**Privacy:**
- You control which vendors see your feedback
- Feedback saved to private repo (opt-in)
- You can revoke access anytime

**Example usage:**
```
You: /save-for-vendor
Claude: Which vendor? [1] Anthropic [2] OpenAI [3] Google
You: 1
Claude: Category? [1] Awesome [2] Issues [3] Feature Request
You: 1
Claude: Brief description:
You: Perfectly refactored complex state management
Claude: ✓ Saved to vendor-feedback/anthropic/awesome/20251006-190000.md
```

**This helps vendors improve their models based on real usage.**
