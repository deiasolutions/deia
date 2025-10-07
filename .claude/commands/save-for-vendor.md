# Save Feedback for AI Vendor

Save this conversation for review by AI vendor (Anthropic, OpenAI, Google).

## Steps:

1. Ask user which vendor:
   - [1] Anthropic (Claude)
   - [2] OpenAI (GPT)
   - [3] Google (Gemini)

2. Ask for category:
   - [1] Awesome - Model did great work
   - [2] Issues - Model struggled or made mistakes
   - [3] Feature Request - Missing capability

3. Ask for brief description (1-2 sentences)

4. Save using vendor_feedback.py:
```python
python -c "
from deia.vendor_feedback import quick_feedback
quick_feedback(
    vendor='anthropic',  # or 'openai', 'google'
    category='awesome',  # or 'issues', 'feature-request'
    description='Your description here',
    conversation='[Full conversation log]'
)
"
```

5. Confirm saved and check if vendor has access

## Privacy Note:
- Feedback saved to `~/.deia-global/vendor-feedback/`
- Vendors only see it if you've granted access
- Use `deia vendor-feedback allow <vendor>` to grant
- Use `deia vendor-feedback revoke <vendor>` to revoke

## This helps vendors improve their models based on real usage.
