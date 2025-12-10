# Port 8000 Chat Controller - Visual Design Specifications
**Date:** 2025-10-25
**Reviewer:** BOT-00004
**Reference:** Anthropic Claude Code Interface (Professional Standard)
**Target:** Claude Code-level polish and professionalism

---

## Color System

### Primary Palette

```
Background Colors:
  --bg-primary: #0f0f0f      (Darkest: Main background)
  --bg-secondary: #1a1a1a    (Dark: Panels, cards)
  --bg-tertiary: #2a2a2a     (Lighter: Input, hover)
  --bg-hover: #333333         (Interactive: Button hover)

Current colors:
  --bg-primary: #1a1a1a   ← TOO LIGHT
  --bg-secondary: #222    ← TOO LIGHT
  Need darker, more sophisticated palette
```

### Accent Color

```
Current: Purple gradient (#667eea, #764ba2)
  Problem: Generic, not distinctive to DEIA

New: Professional Blue (Claude Code style)
  --accent-primary: #4a7ff5    (Bright blue for interactive elements)
  --accent-dark: #2d5cd4       (Dark blue for active state)
  --accent-light: #7ba7ff      (Light blue for hover)

Rationale:
  • Distinctive blue matches Claude Code
  • Professional, not trendy
  • Accessible contrast ratios
  • Consistent with DEIA brand
```

### Status Colors (Use Consistently)

```
--status-success: #10b981   (Green) - ✓ Running, success
--status-warning: #f59e0b  (Amber) - ⚠ Busy, warning
--status-error: #ef4444    (Red)   - ✗ Error, offline
--status-info: #3b82f6     (Blue)  - ℹ Info, neutral
--status-neutral: #6b7280  (Gray)  - Disabled, offline

Apply to:
  • Status indicator dots
  • Border colors for panels
  • Message attribution
  • Success/error messages
```

### Color Contrast (WCAG AA minimum)

```
Text on --bg-primary:
  Text color: #e5e7eb (Light gray, not pure white)
  Contrast ratio: 13.1:1 ✓

Accent buttons on --bg-secondary:
  Button: --accent-primary (#4a7ff5)
  Text: white
  Contrast ratio: 5.2:1 ✓

All colors must pass contrast tests
```

---

## Typography

### Font Stack

```
Font Family:
  Headings: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif
  Body: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
  Monospace (code): 'Monaco', 'Menlo', 'Ubuntu Mono', monospace

Current: Generic system fonts
Problem: Not distinctive
New: Use SF Pro (matches Apple/Claude)
```

### Type Scale (8px base)

```
Heading 1 (h1): 32px, bold (600), line-height 1.2    [Page titles]
Heading 2 (h2): 24px, bold (600), line-height 1.3    [Panel headers]
Heading 3 (h3): 18px, bold (600), line-height 1.4    [Card titles]

Body Large:     16px, regular (400), line-height 1.5 [Input fields, buttons]
Body Normal:    14px, regular (400), line-height 1.6 [Body text, messages]
Body Small:     12px, regular (400), line-height 1.5 [Captions, help text]

Label:          12px, medium (500), line-height 1.4  [Form labels]
Mono:           13px, regular (400), line-height 1.6 [Code, command output]

Current: Mixed sizes (18px, 14px, 11px, 12px)
Problem: No clear hierarchy
New: Consistent scale, obvious importance
```

---

## Spacing System (4px grid)

### Spacing Scale

```
xs:  4px    [Tightest spacing]
sm:  8px    [Button padding, small gaps]
md: 12px    [Card content padding]
lg: 16px    [Panel padding, message gaps]
xl: 20px    [Panel headers, major sections]
xxl: 24px   [Top-level sections]

Apply consistently:
  Buttons: padding lg (16px) × sm (8px)
  Cards: padding md (12px)
  Panel header: padding xl (20px)
  Message margin: md (12px) bottom
  Section gap: xl (20px)
```

### Border Radius

```
--radius-none: 0px       [Panels, full-width elements]
--radius-sm: 4px         [Small buttons, status dots]
--radius-md: 8px         [Input fields, message bubbles]
--radius-lg: 12px        [Large buttons, modals]
--radius-full: 9999px    [Circular elements (avatars)]

Current: Random (6px, 3px, 4px, 12px)
New: Consistent, predictable
```

---

## Component Specifications

### Buttons

#### Primary Button (Launch, Send)
```
Size: Large
  Padding: 12px × 16px
  Font: Body Large (16px, bold)
  Border radius: 8px

States:
  Default: bg-accent-primary, white text
  Hover: bg-accent-dark, lift (+2px shadow)
  Active: bg-accent-dark, no lift
  Disabled: opacity 50%, cursor not-allowed

Shadow (hover):
  0 4px 12px rgba(74, 127, 245, 0.3)

Icon: Add ↓ arrow for expand, ✓ for confirm
```

#### Secondary Button (Select, Options)
```
Size: Normal
  Padding: 8px × 12px
  Font: Body Normal (14px)
  Border: 1px solid --bg-tertiary
  Border radius: 6px

States:
  Default: transparent, --text-secondary
  Hover: bg-hover, --text-primary
  Active: --accent-primary text

No shadow (subtle)
```

### Input Fields

```
Size: Large (like buttons)
  Padding: 12px × 16px
  Font: Body Normal (14px)
  Border: 1px solid --bg-tertiary
  Border radius: 6px

States:
  Default: bg-tertiary, border --bg-tertiary
  Hover: border --bg-hover
  Focus: border --accent-primary, box-shadow accent
  Disabled: opacity 50%, cursor not-allowed
  Error: border --status-error, bg tint red

Placeholder: --text-tertiary (lighter gray)

Focus shadow:
  0 0 0 3px rgba(74, 127, 245, 0.1)  [Blue glow]
```

### Message Bubbles

#### User Message
```
Alignment: Right
Background: --accent-primary
Text color: white
Padding: 12px 16px
Border radius: 12px (rounded except bottom-right: 4px)
Max width: 70%
Font: Body Normal (14px)

Example: ┐
        User: list files
        └┐
```

#### Assistant Message
```
Alignment: Left
Background: --bg-tertiary
Text color: --text-primary
Border: 1px solid --bg-hover
Padding: 12px 16px
Border radius: 12px (rounded except bottom-left: 4px)
Max width: 70%
Font: Body Normal, mono for code

Example: ┌
        Bot-001: files: a.txt, b.txt...
        └┘
```

#### Message Attribution
```
Size: 12px, --text-secondary
Position: Above message
Format: "You" or "BOT-001"
Icon: Avatar (emoji or SVG) before name

User avatar: 👤 or initials in circle
Bot avatar: 🤖 or bot icon with number
```

### Status Indicators

#### Status Dot
```
Size: 10px × 10px
Border radius: 50% (circle)
Variants:
  Running: --status-success (#10b981)
  Busy: --status-warning (#f59e0b)
  Error: --status-error (#ef4444)
  Offline: --status-neutral (#6b7280)

Animation: Pulse on "busy" state
  Opacity: 1 → 0.6 → 1
  Duration: 1.5s, loop
```

#### Status Label
```
Format: Icon + Text
  ✓ Running
  ⚠ Busy
  ✗ Error

Font: 12px, medium (500)
Color: Match icon color
```

### Modal Dialogs

#### Modal Container
```
Position: Centered, fullscreen overlay
Backdrop: rgba(0, 0, 0, 0.5)
Animation: Fade in + slide down (200ms)
Border radius: 12px
Padding: 24px

Header:
  Font: Heading 2 (24px, bold)
  Margin bottom: 16px

Body:
  Font: Body Normal (14px)
  Max height: 60vh (scrollable)

Footer:
  Border top: 1px solid --bg-tertiary
  Padding top: 16px
  Margin top: 16px
  Buttons: Flex, gap 12px

Close button: Top right, × symbol
```

---

## Layout Specifications

### Three-Panel Layout

```
┌────────────────────────────────────────────────────────┐
│ Sidebar     │ Main Chat        │ Status Panel          │
│ 250px       │ Flex             │ 280px                 │
├─────────────┼──────────────────┼───────────────────────┤
│ Header      │ Header           │ Header                │
│ 60px        │ 60px             │ 60px                  │
├─────────────┼──────────────────┼───────────────────────┤
│             │                  │                       │
│ Bot List    │ Chat Messages    │ Status Items          │
│ Flex        │ Flex             │ Flex                  │
│             │                  │                       │
├─────────────┼──────────────────┼───────────────────────┤
│             │ Input Area       │                       │
│             │ 80px             │                       │
└─────────────┴──────────────────┴───────────────────────┘

Gutters (1px border): #333333
Dividers: Clean, subtle

Responsive:
  >1400px: 3 panels (shown above)
  1024-1400px: 2 panels (hide status)
  768-1024px: Single panel (slide navigation)
  <768px: Mobile layout (vertical stack)
```

### Dark Theme Refinement

```
Current: Flat #1a1a1a everywhere
Problem: Lack of depth, hard to distinguish elements

New: Layered depth
  Layer 0 (Deepest):  #0f0f0f  [Page background]
  Layer 1:            #1a1a1a  [Panel background]
  Layer 2:            #2a2a2a  [Card background]
  Layer 3:            #333333  [Input/hover state]

Add subtle shadows to create depth:
  Layer 1 on Layer 0: drop-shadow(0 2px 4px rgba(0,0,0,0.3))
  Layer 2 on Layer 1: drop-shadow(0 1px 2px rgba(0,0,0,0.2))

Result: Professional, easy to scan, not flat
```

---

## Animations & Transitions

### Entrance Animations

```
Message arrival: Fade in + slide up (150ms)
  from opacity 0, transform translateY(4px)
  to opacity 1, transform none

Panel open: Slide in from left (200ms)
  from transform translateX(-100%)
  to transform none

Modal appear: Fade + zoom (200ms)
  from opacity 0, transform scale(0.95)
  to opacity 1, transform none
```

### Interaction Feedback

```
Button press: Instant visual feedback
  Hover: opacity 90%, lift 2px
  Active: opacity 100%, no lift

Input focus: Border color change + glow
  Duration: 150ms
  Shadow: 0 0 0 3px rgba(accent, 0.1)

Loading: Spinner animation
  Rotation: 360° over 1s, infinite
  Stroke width: 2px, accent color
```

### Hover States

```
All interactive elements must have clear hover:

Buttons: Darker bg, lift effect
Links: Underline appear, color brighten
Cards: Bg lighten, shadow appear
Input: Border color change, focus shadow
Tabs: Underline appear, color change

No hover on: Non-interactive text, read-only elements
```

---

## Dark Mode Implementation

### CSS Variables Approach

```css
:root {
  /* Colors */
  --color-bg-primary: #0f0f0f;
  --color-bg-secondary: #1a1a1a;
  --color-text-primary: #e5e7eb;
  --color-text-secondary: #9ca3af;
  --color-accent: #4a7ff5;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;

  /* Typography */
  --font-sans: 'SF Pro Text', system-ui, sans-serif;
  --font-mono: 'Monaco', monospace;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.4);
}

/* Enable future light mode if needed */
[data-theme="light"] {
  --color-bg-primary: #ffffff;
  --color-text-primary: #1f2937;
  /* ... etc ... */
}
```

---

## Responsive Breakpoints

```
Desktop (>1400px):
  • 3-panel layout
  • Full typography scale
  • All features visible

Tablet (1024-1400px):
  • Hide status panel
  • 2-panel layout
  • Reduced font sizes

Mobile (768-1024px):
  • Single panel + drawer
  • Stacked layout
  • Compressed spacing

Small Mobile (<768px):
  • Mobile-first approach
  • Vertical layout
  • Touch targets ≥44px
```

---

## Visual Comparison

### Current vs. New

| Aspect | Current | New | Improvement |
|--------|---------|-----|-------------|
| Colors | Purple (generic) | Blue (distinctive) | Professional |
| Contrast | Some issues | WCAG AA+ | Accessible |
| Spacing | Inconsistent | 4px grid | Organized |
| Typography | Mixed sizes | Clear scale | Scannable |
| Depth | Flat | Layered shadows | Professional |
| Animations | Abrupt | Smooth | Polished |
| Dark mode | Basic | Refined | Premium |

---

## Implementation Checklist

### Phase 1: Color & Typography (2 hours)
- [ ] Define CSS variable system
- [ ] Update color palette
- [ ] Implement typography scale
- [ ] Test contrast ratios

### Phase 2: Spacing & Layout (2 hours)
- [ ] Implement 4px grid
- [ ] Update button/input sizes
- [ ] Refine message bubbles
- [ ] Test responsive breakpoints

### Phase 3: Refinement (2 hours)
- [ ] Add subtle shadows for depth
- [ ] Implement smooth animations
- [ ] Polish hover states
- [ ] Test on multiple browsers

### Phase 4: Accessibility (1 hour)
- [ ] Verify all contrast ratios
- [ ] Test keyboard navigation
- [ ] Check screen reader compatibility
- [ ] Test on mobile devices

---

Generated by BOT-00004
