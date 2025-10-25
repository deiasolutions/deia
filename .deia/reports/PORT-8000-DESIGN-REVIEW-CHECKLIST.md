# Port 8000 Design Review Checklist
**Reviewer:** BOT-004 (Design Architect)
**For Implementation By:** BOT-003
**Date:** 2025-10-25 16:13 CDT
**Reference:** PORT-8000-VISUAL-REDESIGN.md

---

## CHECKLIST: Visual Design Compliance

As BOT-003 implements design fixes, use this checklist to verify each element meets visual design specifications.

---

## SECTION 1: COLOR SYSTEM

### Accent Colors
- [ ] **Primary Accent:** #4a7ff5 (blue, not purple)
  - Used for: Button backgrounds, input focus, selected states
  - Check: Launch button, send button, bot selection highlight
  - Visual: Cooler blue tone, professional Anthropic brand

- [ ] **Secondary Accent:** #3d5cb7 (darker blue)
  - Used for: Button hover state (darker), gradient end
  - Check: Buttons appear to darken on hover
  - Visual: Clear depth/interaction feedback

- [ ] **Backgrounds:**
  - [ ] Main bg: #1a1a1a (dark gray, not black)
  - [ ] Panel bg: #222 (slightly lighter)
  - [ ] Input/message bg: #2a2a2a (card level)
  - Visual: Layered depth feeling, not flat black

### Status Indicator Colors
- [ ] **Running Status:** #28a745 (green) - bot is active
- [ ] **Busy Status:** #ffc107 (amber) - processing
- [ ] **Error Status:** #dc3545 (red) - failed/offline
- [ ] **Stopped Status:** #666 (gray) - not running

Check in:
- Bot list status dot
- Status panel items
- Message routing feedback (if offline)

### Text Colors
- [ ] **Primary Text:** #e0e0e0 (light gray)
- [ ] **Secondary Text:** #aaa (medium gray)
  - Status text, timestamps, bot status
- [ ] **Button Text:** #ffffff (white) on colored backgrounds
- [ ] **Success Message:** Use #28a745 green
- [ ] **Error Message:** Use #dc3545 red

**Contrast Check:** All text ≥4.5:1 ratio (WCAG AA)

---

## SECTION 2: TYPOGRAPHY

### Font Family
- [ ] Body: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- [ ] Code/Messages: `'Monaco', 'Menlo', 'Courier New', monospace`
- Visual: Clean, modern sans-serif. No serif fonts.

### Font Sizes
- [ ] **H1 (Chat Header):** 24px, weight 700
- [ ] **H2 (Panel Headers):** 18px, weight 600
- [ ] **Body Text:** 14px, weight 400 (default)
- [ ] **Bot ID/Labels:** 14px, weight 600 (bold)
- [ ] **Status Text:** 12px, weight 400
- [ ] **Timestamps:** 11px, weight 400
- [ ] **Chat Messages:** 14px, weight 400, font-family: monospace

Check: No more than 4 distinct sizes in use.

### Line Height
- [ ] Default: 1.5 (all text)
- [ ] Messages: pre-wrap preserves manual breaks
- [ ] Visual: Readable, not cramped

### Text Styling
- [ ] Buttons: Font weight 600 (semi-bold)
- [ ] Headers: Font weight 700 (bold)
- [ ] Body: Font weight 400 (regular)
- [ ] No all-caps styling (use bold weight instead)

---

## SECTION 3: SPACING & GRID

### Grid System
- [ ] All spacing based on 4px grid
- [ ] Allowed values: 4px, 8px, 12px, 16px, 20px, 24px, 32px

### Padding
- [ ] Buttons: 12px vertical, 16px horizontal (44px min touch target)
- [ ] Input field: 12px vertical, 16px horizontal
- [ ] Chat messages: 12px vertical, 16px horizontal (inside bubble)
- [ ] Panel headers: 20px (all sides)
- [ ] Bot list items: 12px (padding inside item)
- [ ] Status items: 12px (padding inside item)

### Margins
- [ ] Between items in list: 8px
- [ ] Between sections: 16px-20px
- [ ] Between panels: 1px border (gap)
- [ ] Between chat messages: 15px (below message)
- [ ] Input container padding: 20px (all sides)

### Gaps (flex/grid)
- [ ] Input + Button: 10px gap
- [ ] Bot list items: 8px margin-bottom
- [ ] Status items: 8px margin-bottom
- [ ] No excessive white space (avoid gaps > 20px)

---

## SECTION 4: COMPONENTS

### Buttons

#### Launch Button (`.launch-btn`)
- [ ] Background: Linear gradient #667eea → #764ba2 (update to #4a7ff5 → #3d5cb7)
- [ ] Text color: #ffffff
- [ ] Padding: 10px 16px (minimum)
- [ ] Border radius: 6px
- [ ] Font weight: 600
- [ ] Hover: Background darkens, transform translateY(-1px)
- [ ] Transition: all 0.2s (smooth)
- [ ] Visual: Professional gradient, subtle lift on hover

#### Send Button (`.send-button`)
- [ ] Background: Same gradient as launch button
- [ ] Text color: #ffffff
- [ ] Padding: 12px 24px
- [ ] Border radius: 6px
- [ ] Font weight: 600
- [ ] Hover: Transform translateY(-2px) (lift higher than launch button)
- [ ] Disabled: Opacity 0.6 OR darker gradient + lighter text
- [ ] Transition: transform 0.2s
- [ ] Visual: Prominent, clearly clickable

#### Action Buttons (`.bot-action-btn`)
- [ ] Background: #3a3a3a
- [ ] Text color: #ccc (default), #ffffff (hover)
- [ ] Padding: 4px (small size)
- [ ] Border radius: 3px (subtle)
- [ ] Font size: 11px
- [ ] Hover: Background #444, text white
- [ ] Transition: all 0.2s
- [ ] Visual: Secondary actions, lower prominence

### Input Fields

#### Chat Input (`.chat-input`)
- [ ] Background: #2a2a2a
- [ ] Text color: #e0e0e0
- [ ] Border: 1px solid #333
- [ ] Border radius: 6px
- [ ] Padding: 12px 16px
- [ ] Font size: 16px
- [ ] Placeholder color: #999
- [ ] Focus: Border color #667eea (update to #4a7ff5)
- [ ] Focus: Box shadow: 0 0 0 3px rgba(102, 126, 234, 0.1)  (blue glow)
- [ ] Transition: border-color 0.3s
- [ ] Visual: Clear focus state, not disabled by default

#### Disabled Input State
- [ ] If disabled: opacity 0.5 OR background #1a1a1a
- [ ] Cursor: not-allowed
- [ ] Visual indication clear that interaction unavailable

### Chat Messages

#### User Message (`.message.user .message-content`)
- [ ] Background: #667eea (update to #4a7ff5)
- [ ] Text color: #ffffff
- [ ] Padding: 12px 16px
- [ ] Border radius: 12px
- [ ] Max width: 70%
- [ ] Font: monospace 14px
- [ ] Alignment: Right side of chat
- [ ] Visual: Blue bubble, clear attribution

#### Assistant Message (`.message.assistant .message-content`)
- [ ] Background: #2a2a2a
- [ ] Text color: #e0e0e0
- [ ] Border: 1px solid #333
- [ ] Padding: 12px 16px
- [ ] Border radius: 12px
- [ ] Max width: 70%
- [ ] Font: monospace 14px
- [ ] Alignment: Left side of chat
- [ ] Visual: Gray bubble, clear attribution

#### Message Attribution
- [ ] User messages: Show "You" label (or user ID)
- [ ] Bot messages: Show bot ID (e.g., "BOT-001")
- [ ] Attribution text: 11px, color #999, above/below message
- [ ] Visual: Clear who sent each message

### Status Panel

#### Status Item (`.status-item`)
- [ ] Background: #2a2a2a
- [ ] Border-left: 3px solid #666 (default)
- [ ] Border-left.running: #28a745 (green)
- [ ] Border-left.busy: #ffc107 (amber)
- [ ] Border-left.error: #dc3545 (red)
- [ ] Padding: 12px
- [ ] Border radius: 4px
- [ ] Margin-bottom: 8px
- [ ] Font size: 12px

#### Status Label (`.status-label`)
- [ ] Font weight: 600
- [ ] Color: #e0e0e0
- [ ] Margin-bottom: 4px

#### Status Values (`.status-value`)
- [ ] Color: #e5e7eb (update from #999 for contrast)
- [ ] Margin-bottom: 4px
- [ ] Font size: 12px

### Modal Dialog (if implemented)
- [ ] Backdrop: Dark overlay, semi-transparent (rgba(0,0,0,0.7))
- [ ] Modal content: #222 background
- [ ] Modal border: 1px solid #333
- [ ] Border radius: 8px
- [ ] Box shadow: 0 20px 25px rgba(0,0,0,0.5)
- [ ] Input inside modal: Same as chat input
- [ ] Buttons: 12px padding, 6px radius
- [ ] Visual: Centered, clear visual separation

---

## SECTION 5: INTERACTIVE STATES

### Hover States
- [ ] All buttons: Visual feedback on hover
- [ ] Bot list item: Background #333 (darker)
- [ ] Bot item.active: Border-left #28a745 (green)
- [ ] Bot action buttons: Background #444, text white
- [ ] Status items: Maybe slight bg change or not (read-only items)
- [ ] Input focus: Blue border + glow shadow

### Active/Selected States
- [ ] Bot item.active: Background #333, border-left green
- [ ] Selected bot: Visual indication in header ("Connected to BOT-001")
- [ ] Pressed buttons: Subtle color shift (slightly darker)

### Disabled States
- [ ] Disabled buttons: Opacity 0.6 OR darker color
- [ ] Disabled inputs: Opacity 0.5 OR grayed background
- [ ] Cursor: not-allowed on disabled elements

### Focus States (Keyboard Navigation)
- [ ] Buttons: White outline 3px, outline-offset 2px
- [ ] Input field: Blue border + glow (already good)
- [ ] Tab order: Clear visual progression
- [ ] No focus traps

### Loading/Pending States
- [ ] Sending button: Text "Sending..." + maybe spinner icon
- [ ] Typing indicator: "Bot thinking..." animated
- [ ] Status updating: Maybe pulse animation on status items

---

## SECTION 6: LAYOUT & RESPONSIVENESS

### Main Layout
- [ ] 3-panel layout: Left (250px) | Center (flex) | Right (280px)
- [ ] Heights: All panels full viewport height
- [ ] Gaps: 1px between panels (dark separator)
- [ ] Background: #0a0a0a (darkest, shows through gaps)

### Panel Widths
- [ ] Left panel: 250px fixed
- [ ] Center panel: flex (remaining space)
- [ ] Right panel: 280px fixed

### Breakpoint: 1024px
- [ ] Hide status panel (right)
- [ ] Center panel becomes flex: 1 (full width except left)
- [ ] Left panel stays 250px

### Breakpoint: 768px
- [ ] Left panel: 200px (narrower)
- [ ] Gap: 0 (no separator)
- [ ] Might stack vertically on very small (but not required for current scope)

### Scrolling
- [ ] Bot list: overflow-y: auto (scrollbar if needed)
- [ ] Chat messages: overflow-y: auto (scrollbar if needed)
- [ ] Status list: overflow-y: auto (scrollbar if needed)

---

## SECTION 7: ANIMATIONS & TRANSITIONS

### Button Transitions
- [ ] All: `transition: all 0.2s` (smooth)
- [ ] Hover lift: `transform: translateY(-1px)` or `(-2px)`
- [ ] No jarring changes

### Input Transitions
- [ ] Border color: `transition: border-color 0.3s`
- [ ] Focus appears smooth, not sudden

### No Animation Issues
- [ ] No flickering
- [ ] No lag on hover
- [ ] Performance: 60fps target

---

## SECTION 8: DARK THEME DEPTH

### Layering (Darkest to Lightest)
- [ ] Layer 0 (Darkest): #0a0a0a (separator background)
- [ ] Layer 1: #1a1a1a (main background)
- [ ] Layer 2: #222 (panel headers, panels)
- [ ] Layer 3: #2a2a2a (card level - messages, status items)
- [ ] Layer 4: #333+ (interactive elements, hover states)
- [ ] Text: #e0e0e0 (light gray on layers 1-3)

### Visual Depth
- [ ] Headers: Solid color with gradient option
- [ ] Cards/Items: Slightly raised (background change, maybe subtle shadow)
- [ ] No flat appearance
- [ ] Good contrast without being harsh

---

## SECTION 9: OVERALL POLISH

### Professional Appearance
- [ ] No browser defaults showing (inputs, buttons)
- [ ] Consistent styling throughout
- [ ] No misaligned elements
- [ ] Proper padding/margins maintained
- [ ] Clean code (no debug text, console.logs removed)

### Visual Hierarchy
- [ ] Headers prominent (24px, 18px)
- [ ] Body text clear (14px)
- [ ] Labels visible (12px)
- [ ] Proper weight differences

### Accessibility Polish
- [ ] Focus outlines visible
- [ ] Color contrast adequate
- [ ] Buttons clearly buttons (not text links)
- [ ] Inputs clearly inputs (border, background)

### Performance
- [ ] Smooth interactions
- [ ] No jank on button clicks
- [ ] Transitions smooth
- [ ] No visual glitches

---

## FINAL VERIFICATION

### Checklist Completion
- [ ] All color checks passed
- [ ] All typography checks passed
- [ ] All spacing checks passed
- [ ] All components check passed
- [ ] Interactive states working
- [ ] Layout correct at all breakpoints
- [ ] Animations smooth
- [ ] Dark theme has depth
- [ ] Overall professional appearance

### Visual Inspection (Manual)
1. Open http://localhost:8000 in fresh browser
2. Walk through each section visually
3. Check each checkbox above
4. Take screenshots of:
   - Launch dialog (modal)
   - Bot selection
   - Chat messages (user + bot)
   - Status panel
   - Error state

### Comparison to Specs
- [ ] Compare colors against spec (use color picker)
- [ ] Compare spacing against 4px grid
- [ ] Compare typography against size/weight list
- [ ] Compare component styling against specs

---

## SIGN-OFF

**Design Review Status:** [PENDING / APPROVED / APPROVED WITH NOTES]

**Reviewed By:** BOT-004

**Review Date:** 2025-10-25 16:13 CDT

**Notes:** (To be filled during review)

---

**This checklist is live during BOT-003 implementation.**
**BOT-004 will verify each item as changes are made.**

Generated by BOT-004
