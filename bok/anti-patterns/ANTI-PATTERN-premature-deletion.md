
# Anti-Pattern: Premature Deletion

**Version:** 1.0
**Effective Date:** 2025-10-29
**Authority:** Q33N (BEE-000)
**Status:** DRAFT - Awaiting User Approval

## 1. Name

Premature Deletion

## 2. Problem

The impulse to delete incorrect, outdated, or mistaken information rather than archiving it. This is often driven by a desire to erase a mistake or to create a "clean slate."

## 3. Context

This anti-pattern is most likely to occur when an agent, particularly a new one, makes a mistake and wants to correct it immediately. It can also occur when a process or document is superseded and an agent believes the old version is no longer needed.

## 4. Forces

*   **Desire for a clean slate:** The belief that removing incorrect information is the best way to avoid confusion.
*   **Fear of judgment:** The desire to erase a mistake to avoid criticism or negative feedback.
*   **Misunderstanding of the value of historical context:** A failure to recognize that even mistakes and outdated information have value as learning opportunities.

## 5. Solution

The principle of **"we don't delete stuff."**

All artifacts, even mistakes, should be archived and marked as deprecated. The process is as follows:

1.  **Identify the outdated or incorrect artifact.**
2.  **Create a new, corrected version.**
3.  **Move the old artifact to the `.deia/archive/` directory.**
4.  **Rename the old artifact to indicate that it is deprecated (e.g., `DEPRECATED-old-file.md`).**
5.  **Add a notice to the top of the archived file that points to the new, authoritative version.**

## 6. Rationale

*   **Preserves Institutional Memory:** Archiving mistakes and outdated information provides a complete historical record of the hive's evolution. This is essential for understanding why things are the way they are.
*   **Creates Learning Opportunities:** Mistakes are valuable learning opportunities. By preserving them, we can analyze them, learn from them, and create new anti-patterns to prevent them from happening again.
*   **Encourages Psychological Safety:** A culture that does not punish mistakes, but instead learns from them, encourages psychological safety. This makes agents more likely to take risks, innovate, and self-report their own errors.
*   **Provides a Revert Path:** In the event that a new process or document is found to be flawed, the archived version provides an easy way to revert to the previous state.
