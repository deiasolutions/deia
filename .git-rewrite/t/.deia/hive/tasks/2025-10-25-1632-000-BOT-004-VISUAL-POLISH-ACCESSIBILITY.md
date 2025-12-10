# BOT-004 VISUAL POLISH + ACCESSIBILITY AUDIT - PORT 8000
**From:** Q33N (BEE-000)
**To:** BOT-004 (Designer/Visual QA)
**Issued:** 2025-10-25 16:32 CDT
**Due:** 2025-10-25 18:32 CDT (2 hours)
**Priority:** HIGH - User experience and compliance

---

## PRIMARY TASK: VISUAL POLISH

Apply design system changes from your design review to the port 8000 interface.

---

## VISUAL POLISH DELIVERABLES

### 1. Color System Update (from PORT-8000-VISUAL-REDESIGN.md)
**File:** `src/deia/adapters/web/static/style.css` (or wherever styles are)

**Changes:**
- Replace purple gradient with blue #4a7ff5
  - Old: `#8b5cf6` (purple) → New: `#4a7ff5` (blue)
  - All gradient references updated
  - Status indicators, buttons, highlights use new blue
- Neutral grays: `#f3f4f6` (light), `#1f2937` (dark)
- Accent colors: Green `#10b981` (success), Red `#ef4444` (error), Yellow `#f59e0b` (warning)

**What to update:**
- Primary button color
- Link/hover colors
- Active/selected states
- Loading indicators
- Status dashboard backgrounds
- Chart/graph colors (if any)

### 2. Typography Hierarchy
**File:** CSS styling

**Implementation:**
- H1: 32px, bold, #1f2937
- H2: 24px, semibold, #374151
- H3: 18px, semibold, #4b5563
- Body: 14px, regular, #6b7280
- Small: 12px, regular, #9ca3af
- Monospace (code/logs): 13px, 'Monaco' or 'Courier New'

**Apply to:**
- Page titles
- Section headers
- Chat messages
- Status text
- Command outputs

### 3. Component Refinement
**Components to Polish:**
- Buttons: Add hover, active, disabled states with visual feedback
  - Hover: Slightly darker blue, shadow
  - Active: Darker blue, pressed effect
  - Disabled: Grayed out, cursor: not-allowed
- Input fields: Border, focus ring, placeholder text
  - Border: 1px solid #e5e7eb
  - Focus: Blue border + glow, #4a7ff5
  - Placeholder: #9ca3af
- Messages: Consistent padding, clear spacing, rounded corners
- Bot status indicators: Color-coded (green=running, red=stopped, yellow=loading)
- Chat history: Clean list view, alternating background rows (optional)

### 4. Spacing & Layout
- Consistent 4px, 8px, 12px, 16px, 20px, 24px spacing
- Clear visual hierarchy
- Breathing room in chat interface
- Proper margins around sections

### 5. Dark Mode Support (if applicable)
- All colors adapted for dark mode
- Text contrast maintained (WCAG AA minimum)
- Dark background: #111827
- Card background: #1f2937

---

## PARALLEL TASK: ACCESSIBILITY AUDIT

While applying visual polish, also conduct a comprehensive accessibility audit.

**File to Create:** `.deia/reports/PORT-8000-ACCESSIBILITY-AUDIT.md`

---

## ACCESSIBILITY AUDIT CHECKLIST

### 1. Color Contrast (WCAG AA Compliance)
**Test Every Element:**
- Text on background: Minimum 4.5:1 ratio
- Large text (18px+): Minimum 3:1 ratio
- UI components: Minimum 3:1 ratio

**Tools:**
- Browser DevTools: Use contrast checker
- Online: https://www.tpgi.com/color-contrast-checker/

**Elements to Check:**
- All button text
- All link text
- Chat message text
- Status labels
- Error messages
- Form labels

**Report:**
- ✅ Pass (ratio shown) or ❌ Fail (issue noted)
- If fail: Suggest fix (change text color, background color, or both)

### 2. Keyboard Navigation
**Test Without Mouse:**
- Can you navigate to all interactive elements using Tab key?
- Can you activate buttons using Enter/Space?
- Can you send messages using Enter?
- Can you clear inputs with keyboard?
- Is focus visible (outline or highlight)?
- Is focus order logical (left-to-right, top-to-bottom)?

**Elements to Test:**
- Bot launch button → launch dialog → form fields → submit button
- Select bot dropdown → selects bot
- Message input field → send button → message appears
- History scroll → load more button
- All interactive elements

**Report:**
- ✅ Element can be accessed by keyboard
- ❌ Element cannot be accessed (accessibility issue)

### 3. Screen Reader Compatibility
**Test with:**
- NVDA (free, Windows)
- JAWS (commercial, Windows)
- VoiceOver (Mac/iOS)
- Or read the code to verify accessibility attributes

**Check:**
- Do elements have `aria-label` or text labels?
- Do buttons have descriptive text (not just icons)?
- Do form fields have associated `<label>` tags?
- Do error messages have role="alert"?
- Is DOM order logical?

**Elements to Test:**
- Bot selector: Does screen reader say which bot is selected?
- Message input: Does it say "Message input field"?
- Send button: Does it say "Send"?
- Status indicators: Do they describe what they mean?
- Chat messages: Are sender and message clear?

**Report:**
- ✅ Element is accessible to screen readers
- ❌ Missing: aria-label, role, etc. (fix noted)

### 4. Focus Indicators
**Check:**
- All interactive elements have visible focus indicator
- Focus outline is visible (not removed by CSS)
- Focus style contrasts with background (minimum 3:1)

**Elements:**
- Buttons
- Links
- Input fields
- Bot selector
- History items

**Report:**
- ✅ Visible focus indicator (what style?)
- ❌ Missing focus indicator (add CSS outline or box-shadow)

### 5. Form & Input Accessibility
**Check:**
- All inputs have associated labels
- Error messages are linked to inputs (aria-describedby)
- Required fields are marked (aria-required or * symbol)
- Input types are correct (text, password, email, etc.)

**Elements:**
- Bot launch form
- Message input
- Search/filter (if any)

**Report:**
- ✅ Form is accessible
- ❌ Issues found (what to fix?)

---

## AUDIT REPORT FORMAT

**File:** `.deia/reports/PORT-8000-ACCESSIBILITY-AUDIT.md`

```markdown
# Port 8000 Accessibility Audit
**Date:** 2025-10-25
**Tested By:** BOT-004
**Status:** WCAG AA Compliance Check

## Summary
- Total Elements Tested: X
- Passing: Y (✅)
- Failing: Z (❌)
- Compliance: XX%

## Color Contrast Results
### Passing ✅
- Button text on blue background: 4.8:1 ✅
- Chat message text: 5.2:1 ✅
- [more...]

### Failing ❌
- Status label on yellow: 2.1:1 ❌ (needs 4.5:1)
  - Fix: Change yellow to darker color
- [more...]

## Keyboard Navigation Results
- ✅ All buttons accessible via Tab
- ✅ Send message works with Enter
- ❌ History scroll not accessible (no scrollable container)
  - Fix: Add keyboard support to history

## Screen Reader Results
- ✅ Bot selector announces "Select bot: [name]"
- ❌ Message input missing aria-label
  - Fix: Add aria-label="Message input"

## Focus Indicators
- ✅ All interactive elements have visible focus outline
- ✅ Focus contrast meets 3:1 minimum

## Recommendations
1. [Priority] Fix color contrast issues (3 elements)
2. [Medium] Add keyboard navigation to history
3. [Low] Improve focus indicator styling

## Sign-Off
BOT-004 confirms accessibility testing complete.
Ready for implementation fixes in next phase.
```

---

## SUCCESS CRITERIA

**Visual Polish:**
- ✅ Color system updated (purple → blue throughout)
- ✅ Typography hierarchy applied
- ✅ Components refined (hover/active/disabled states)
- ✅ Spacing consistent
- ✅ Dark mode colors (if applicable)
- ✅ Tested visually in browser (all UI looks good)

**Accessibility Audit:**
- ✅ All elements color contrast checked
- ✅ Keyboard navigation verified
- ✅ Screen reader compatibility assessed
- ✅ Focus indicators verified
- ✅ Form accessibility checked
- ✅ Audit report written (file created)

**Overall:**
- ✅ All CSS changes committed/saved
- ✅ Accessibility audit report uploaded
- ✅ Status report submitted
- ✅ Ready for Batch 1 (Component Library documentation)

---

## STATUS REPORT LOCATION

**Due:** 2025-10-25 18:32 CDT

Create file: `.deia/hive/responses/deiasolutions/BOT-004-VISUAL-ACCESSIBILITY-WINDOW-1-COMPLETE.md`

**Include:**
- Visual polish completion (all 5 items?)
- Screenshots of updated design (if possible)
- Accessibility audit results (% passing)
- Key accessibility issues found and recommendations
- Accessibility audit report file location
- Any blockers encountered
- Time spent on polish vs. audit
- Ready for Batch 1? (YES/NO)

---

## RESOURCES

- Your design specs: `.deia/hive/responses/deiasolutions/PORT-8000-VISUAL-REDESIGN.md`
- UX fixes reference: `.deia/hive/responses/deiasolutions/PORT-8000-UX-FIXES.md`
- WCAG Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Accessibility Tools: NVDA (free), Browser DevTools Accessibility panel

---

## NOTES

- Design polish first (30-60 min) then audit (30-60 min)
- Audit is pass/fail on compliance - be thorough
- Visual polish should be done by 17:45 (audit finishes by 18:32)
- Autologging required: Update every 5-10 minutes
- Screenshots of before/after helpful for documentation
- Next task: Component Library (Batch 1 at 18:32)

---

**Q33N - BEE-000**
**POLISH THE VISUALS, AUDIT ACCESSIBILITY, REPORT AT 18:32**
