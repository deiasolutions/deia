# Vercel Preview URL Retrieval Process

**Project:** FamilyBondBot
**Date:** 2025-10-05
**Claude Session:** Main development session
**Submitted By:** Claude Code Assistant

---

## Context

During active development, Dave requested the Vercel preview URL for testing the folder creation feature that had been deployed. The commit in question was fcb0844 on the main branch.

## Problem/Discovery

**Initial Approach (FAILED):**
- Attempted to use GitHub API endpoint: `https://api.github.com/repos/DAAAAVE-ATX/familybondbot/commits/fcb0844/status`
- Result: 404 Not Found error
- Also tried: `https://api.github.com/repos/DAAAAVE-ATX/familybondbot/commits/fcb0844/check-runs`
- Result: 404 Not Found error

**Root Cause:**
The GitHub API approach doesn't reliably return Vercel deployment information, likely due to:
- Authentication requirements
- Different API endpoint structure needed
- Vercel's integration not exposing status through standard GitHub commit status API

## Resolution/Process

**Correct Approach:**
Use the Vercel CLI directly:

```bash
vercel ls --scope parent-child-contact-solutions --yes
```

**This command returns:**
- Complete list of all recent deployments
- Deployment URLs with unique hashes
- Status indicators (Ready/Error)
- Environment labels (Preview/Production)
- Chronological ordering (newest first)
- Age of each deployment

**To get the latest preview URL:**
1. Run the command above
2. Look for the topmost deployment marked as "Preview" environment with "● Ready" status
3. That URL is the most recent preview deployment to test

**Result:** Successfully retrieved preview URL: `https://familybondbot-kr22d9znh-parent-child-contact-solutions.vercel.app`

## Key Takeaways

1. **Don't use GitHub API for Vercel preview URLs** - it's unreliable and wastes time
2. **Go straight to `vercel ls` command** when Dave asks for preview URL
3. **First Preview URL in output = latest preview** to test
4. The Vercel CLI provides more complete and accurate deployment information
5. Preview deployments are created automatically for every main branch commit

## Related Files

- Created: `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\VERCEL_WORKFLOW.md` - Complete workflow documentation for future reference
- Created: `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\DEIA_SUBMISSION_PROCESS.md` - Process for creating these submissions

## Future Reference

**Use this information when:**
- Dave asks for a preview URL to test changes
- Debugging deployment issues
- Verifying which deployment corresponds to which commit
- Understanding the difference between Preview and Production environments
- Training future Claude sessions on FamilyBondBot workflow

**Critical command to remember:**
```bash
vercel ls --scope parent-child-contact-solutions --yes
```

## Process Improvement

This failure led to:
1. Documentation of correct Vercel workflow in project root
2. Creation of DEIA submission process for capturing learnings
3. Clear instructions for future Claude sessions to avoid repeating this mistake

**Time wasted:** ~5 minutes attempting GitHub API approaches
**Time saved in future:** Immediate access to correct command and process
