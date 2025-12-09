# BOT-004 COMPONENT LIBRARY & DESIGN SYSTEM - WINDOW 2
**From:** Q33N (BEE-000)
**To:** BOT-004
**Issued:** 2025-10-25 16:36 CDT
**Window:** 18:32 - 20:32 CDT (2 hours) - Deploy after Window 1 complete
**Priority:** HIGH - Foundational for consistency

---

## ASSIGNMENT

Document all UI components as a design system. This becomes the source of truth for building additional UIs and maintaining consistency.

---

## DELIVERABLE FILE

**File:** `.deia/docs/COMPONENT-LIBRARY.md`

---

## COMPONENTS TO DOCUMENT

### 1. Buttons (20 min)
- Primary button
  - Color, padding, font, border radius
  - Hover state (color, shadow)
  - Active state (pressed appearance)
  - Disabled state (opacity, cursor)
  - Example code snippet
- Secondary button
- Danger button (red)
- Icon button
- Loading button (with spinner)

### 2. Input Fields (20 min)
- Text input
  - Border, color, focus ring
  - Placeholder styling
  - Disabled state
  - Example code
- Message input (large, tall)
- Search input (with icon)
- Error state (red border, error message)

### 3. Chat Messages (15 min)
- User message bubble
  - Background color, text color
  - Timestamp position
  - Alignment (right for user, left for bot)
- Bot message bubble
  - Different styling than user
- System message
  - Gray, centered, smaller
- Loading message (skeleton)

### 4. Status Indicators (15 min)
- Online indicator (green dot + text)
- Offline indicator (gray dot + text)
- Loading indicator (spinner)
- Error indicator (red)
- Color codes (hex values, CSS classes)

### 5. Modals (20 min)
- Bot launch modal
  - Backdrop styling
  - Modal box styling
  - Title, body, footer
  - Close button (X in corner)
  - Cancel/Submit buttons
- Error modal
- Confirmation modal

### 6. Layout Components (20 min)
- Header/top bar
  - Logo, title, buttons
- Sidebar (bot list)
  - Width, background, item styling
  - Selected/active bot styling
  - Hover states
- Main chat area
  - Message list container
  - Input field area
  - Footer area

### 7. Forms (10 min)
- Form labels
- Form validation messages
- Required field indicators
- Field groups/sections

---

## DOCUMENTATION FORMAT

```markdown
# Component Library

## Button Component

### Primary Button
**Purpose:** Main action button

**Styling:**
- Background: #4a7ff5
- Text color: #ffffff
- Padding: 8px 16px
- Border radius: 4px
- Font: 14px, semibold
- Cursor: pointer

**States:**
```
:default {
  background: #4a7ff5
  box-shadow: none
}

:hover {
  background: #3a65d5
  box-shadow: 0 2px 8px rgba(0,0,0,0.15)
}

:active {
  background: #2a55c5
  transform: translateY(1px)
}

:disabled {
  background: #d1d5db
  cursor: not-allowed
  opacity: 0.5
}
```

**Code Example:**
```html
<button class="btn btn-primary">Click me</button>
```

```css
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #4a7ff5;
  color: #ffffff;
}

.btn-primary:hover {
  background: #3a65d5;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
```

**Accessibility:**
- ✅ Has visible focus ring
- ✅ Has disabled state
- ✅ Text color contrast >= 4.5:1
```

**Repeat this format for all components**

---

## SUCCESS CRITERIA

- ✅ All 7 component categories documented
- ✅ Each component shows: Purpose, Styling, States, Code, Accessibility
- ✅ Color codes (hex values) consistent with design system
- ✅ Code examples copy-paste ready
- ✅ Accessibility notes on each
- ✅ File created: `.deia/docs/COMPONENT-LIBRARY.md`

---

## STATUS REPORT

**Due:** 2025-10-25 20:32 CDT

Create file: `.deia/hive/responses/deiasolutions/BOT-004-COMPONENT-LIBRARY-WINDOW-2-COMPLETE.md`

**Include:**
- All 7 components documented?
- File location
- Any components missing or needing revision
- Ready for Window 3? (YES/NO)

---

**Q33N - BEE-000**
**DOCUMENT COMPONENT LIBRARY - DESIGN SYSTEM FOUNDATION**
