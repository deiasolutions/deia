# VS Code DEIA Extension - Next Steps Specification
**Version:** 0.2.0 (Next Release)
**Current Status:** v0.1.0 - Phases 1-2 Complete (~40%)
**Date:** 2025-10-19
**Author:** DEIA Project Team

---

## Executive Summary

The VS Code extension has completed Phases 1-2 with **1,717 lines of production TypeScript**, 10 working commands, auto-logging, and SpecKit integration. This spec defines the path to **v0.2.0** (Phase 3: Pattern Extraction) and beyond.

---

## Current State (What We Have) ✅

### Files Implemented (8 modules, 1,717 lines TS)

**Location:** `extensions/vscode-deia/src/`

1. **extension.ts** (82 lines) - Main entry point
   - Activates on workspace startup
   - Initializes detector, monitor, chat participant
   - Watches for DEIA workspace changes
   - Lifecycle management

2. **chatParticipant.ts** (200 lines) - @deia chat integration
   - Registers `@deia` participant
   - Commands: help, status, log
   - Conversation buffering for auto-log
   - Context-aware responses

3. **commands.ts** (587 lines) - 10 commands implemented
   - Check Status, Log Chat, View Logs, Read Resume
   - Toggle Auto-Logging, Save Buffer, Monitor Status
   - Submit Pattern (stub), Create Spec, Update Constitution

4. **conversationMonitor.ts** (262 lines) - Auto-logging engine
   - File system watchers
   - Inactivity detection (5 min threshold)
   - Message buffering
   - Auto-save on inactivity

5. **deiaDetector.ts** (115 lines) - Project detection
   - Detects `.deia/` directory
   - Reads `.deia/config.json`
   - Finds workspace root
   - Config validation

6. **deiaLogger.ts** (168 lines) - Conversation logging
   - Calls DEIA CLI (`deia log`)
   - Creates temp transcript files
   - Formats messages
   - Error handling

7. **speckitIntegration.ts** (251 lines) - SpecKit bridge
   - Parse conversation logs
   - Extract requirements, decisions, architecture
   - Generate SpecKit-compatible markdown
   - Update SpecKit constitution

8. **statusBar.ts** (52 lines) - Status bar UI
   - Shows auto-log status
   - Color-coded indicators
   - Click to toggle

### Commands Working (10 total)

1. ✅ `DEIA: Check Status` - Shows config, workspace, CLI path
2. ✅ `DEIA: Log Current Chat` - Manual log trigger
3. ✅ `DEIA: View Session Logs` - Opens `.deia/sessions/`
4. ✅ `DEIA: Read Project Resume` - Opens `project_resume.md`
5. ✅ `DEIA: Toggle Auto-Logging` - Enable/disable monitoring
6. ✅ `DEIA: Save Conversation Buffer Now` - Force save buffer
7. ✅ `DEIA: Monitor Status` - Buffer size, session duration
8. ✅ `DEIA: Submit Pattern to Community` - Stub (not implemented)
9. ✅ `DEIA: Create SpecKit Spec from Conversation` - Generate spec
10. ✅ `DEIA: Update SpecKit Constitution` - Add decisions to constitution

### Features Working

**Core Logging:**
- ✅ Manual conversation logging
- ✅ Auto-logging with file watchers
- ✅ Inactivity-based auto-save (5 min)
- ✅ Crash recovery (buffer persists)
- ✅ Session file creation (`.deia/sessions/`)
- ✅ Index and resume updates

**Chat Integration:**
- ✅ `@deia` chat participant
- ✅ Help, status, log commands in chat
- ✅ Message buffering for auto-log

**SpecKit Integration:**
- ✅ Parse conversation logs
- ✅ Extract requirements/decisions/architecture
- ✅ Generate SpecKit-compatible specs
- ✅ Update SpecKit constitution

**Configuration:**
- ✅ Auto-detect DEIA projects
- ✅ Read `.deia/config.json`
- ✅ Status bar integration
- ✅ Settings UI (3 config options)

### Documentation (6 docs, ~35,000 words)

- `README.md` - User guide (184 lines)
- `STATUS.md` - Build status and features (346 lines)
- `AUTO-LOGGING.md` - Auto-logging documentation (9,476 bytes)
- `UAT-AUTO-LOGGING.md` - User acceptance testing
- `SPECKIT_INTEGRATION.md` - SpecKit workflow (8,642 bytes)
- `TESTING.md` - Testing guide
- `CHANGELOG.md` - Version history

### Packaged Artifact

- ✅ `deia-0.1.0.vsix` - Ready for local install
- ✅ All TypeScript compiled to JavaScript (`out/` directory)
- ✅ 137 npm packages installed
- ✅ Launch config (F5 to test)

---

## What's Missing (Phase 3+)

### Phase 3: Pattern Extraction (NOT STARTED)
- ❌ Code selection → Extract pattern UI
- ❌ Pattern template editor
- ❌ Basic PII detection
- ❌ Save to `.deia/intake/`

### Phase 4: BOK Search (NOT STARTED)
- ❌ Search community patterns command
- ❌ Sidebar with search results
- ❌ Insert pattern into code
- ❌ Contextual suggestions

### Phase 5: Already Complete ✅
- ✅ Auto-logging (DONE in v0.1.0)

### Phase 6: Advanced (NOT STARTED)
- ❌ ML-based PII detection
- ❌ Pattern suggestion AI
- ❌ DEIA API integration
- ❌ Multi-language support

---

## Next Steps: v0.2.0 (Phase 3: Pattern Extraction)

**Goal:** Enable users to extract reusable patterns from code and conversations

**Timeline:** 2-3 weeks

**Effort:** ~20-30 hours

---

## Phase 3 Tasks Breakdown

### Task 1: Pattern Extraction Command (6-8 hours)

**Goal:** Add `DEIA: Extract Pattern from Selection` command

**Files to Create/Modify:**
- Modify: `src/commands.ts` (add new command)
- Create: `src/patternExtractor.ts` (new module, ~200 lines)

**Implementation:**

```typescript
// src/patternExtractor.ts

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export interface PatternMetadata {
  title: string;
  tags: string[];
  urgency: 'low' | 'medium' | 'high' | 'critical';
  platforms: string[];
  audience: string[];
  description: string;
}

export class PatternExtractor {

  /**
   * Extract pattern from current editor selection
   */
  public async extractFromSelection(): Promise<void> {
    const editor = vscode.window.activeTextEditor;

    if (!editor) {
      vscode.window.showErrorMessage('No active editor');
      return;
    }

    const selection = editor.selection;
    if (selection.isEmpty) {
      vscode.window.showErrorMessage('No text selected');
      return;
    }

    const selectedText = editor.document.getText(selection);
    const language = editor.document.languageId;
    const fileName = path.basename(editor.document.fileName);

    // Prompt user for pattern metadata
    const metadata = await this.promptForMetadata(selectedText, language);

    if (!metadata) {
      return; // User cancelled
    }

    // Generate pattern document
    const patternDoc = this.generatePatternDocument(
      metadata,
      selectedText,
      language,
      fileName
    );

    // Save to .deia/intake/pending/
    await this.savePattern(patternDoc, metadata.title);

    vscode.window.showInformationMessage(
      `Pattern "${metadata.title}" saved to .deia/intake/pending/`,
      'Open Pattern'
    ).then(selection => {
      if (selection === 'Open Pattern') {
        // Open the created pattern file
      }
    });
  }

  /**
   * Prompt user for pattern metadata
   */
  private async promptForMetadata(
    code: string,
    language: string
  ): Promise<PatternMetadata | undefined> {

    // Step 1: Pattern title
    const title = await vscode.window.showInputBox({
      prompt: 'Pattern title (short and descriptive)',
      placeHolder: 'e.g., "Safe Print with Unicode Fallback"',
      validateInput: (value) => {
        if (!value || value.trim().length < 5) {
          return 'Title must be at least 5 characters';
        }
        return null;
      }
    });

    if (!title) return undefined;

    // Step 2: Description
    const description = await vscode.window.showInputBox({
      prompt: 'One-sentence description of what this pattern solves',
      placeHolder: 'e.g., "Prevents crashes when printing Unicode to Windows terminals"'
    });

    if (!description) return undefined;

    // Step 3: Tags (multi-select)
    const tags = await vscode.window.showQuickPick(
      [
        'error-handling', 'unicode', 'windows', 'cli', 'python', 'typescript',
        'git', 'testing', 'deployment', 'security', 'performance',
        'multi-agent', 'coordination', 'bug-fix', 'workaround'
      ],
      {
        canPickMany: true,
        placeHolder: 'Select tags (choose 3-5 relevant tags)'
      }
    );

    if (!tags || tags.length === 0) return undefined;

    // Step 4: Urgency
    const urgency = await vscode.window.showQuickPick(
      [
        { label: 'Low', value: 'low' },
        { label: 'Medium', value: 'medium' },
        { label: 'High', value: 'high' },
        { label: 'Critical', value: 'critical' }
      ],
      { placeHolder: 'Pattern urgency' }
    );

    if (!urgency) return undefined;

    // Step 5: Platform (multi-select)
    const platforms = await vscode.window.showQuickPick(
      ['Platform-Agnostic', 'Windows', 'Linux', 'macOS', 'Web', 'Cloud'],
      {
        canPickMany: true,
        placeHolder: 'Select platforms'
      }
    );

    if (!platforms || platforms.length === 0) return undefined;

    // Step 6: Audience (multi-select)
    const audience = await vscode.window.showQuickPick(
      ['developers', 'designers', 'admins', 'devops', 'all'],
      {
        canPickMany: true,
        placeHolder: 'Select audience'
      }
    );

    if (!audience || audience.length === 0) return undefined;

    return {
      title,
      description,
      tags,
      urgency: urgency.value as any,
      platforms,
      audience
    };
  }

  /**
   * Generate pattern document from metadata and code
   */
  private generatePatternDocument(
    metadata: PatternMetadata,
    code: string,
    language: string,
    sourceFile: string
  ): string {
    const date = new Date().toISOString().split('T')[0];

    return `---
title: "Pattern: ${metadata.title}"
tags:
${metadata.tags.map(t => `  - ${t}`).join('\n')}
urgency: ${metadata.urgency}
platforms:
${metadata.platforms.map(p => `  - ${p}`).join('\n')}
audience:
${metadata.audience.map(a => `  - ${a}`).join('\n')}
date_added: ${date}
contributors:
  - VS Code Extension User
status: experimental
version: 1.0
source_file: ${sourceFile}
---

# Pattern: ${metadata.title}

**${metadata.description}**

---

## Context

<!-- When should you use this pattern? -->

**Use this pattern when:**
- TODO: Describe situation A
- TODO: Describe situation B

**NOT for:**
- TODO: When NOT to use this

---

## Problem

<!-- What problem does this solve? -->

TODO: Describe the problem this pattern addresses.

---

## Solution

<!-- How does this pattern solve it? -->

TODO: Explain the solution approach.

### Code

\`\`\`${language}
${code}
\`\`\`

---

## Implementation

<!-- Step-by-step guide -->

**Step 1:** TODO
**Step 2:** TODO
**Step 3:** TODO

---

## Gotchas

<!-- What to watch out for -->

- TODO: Common mistakes
- TODO: Edge cases
- TODO: Performance considerations

---

## Related Patterns

<!-- Link to similar patterns -->

- TODO: Related pattern 1
- TODO: Related pattern 2

---

## Submission Checklist

Before submitting to BOK, ensure:

- [ ] All TODO sections filled in
- [ ] Code tested and working
- [ ] No PII or secrets in code
- [ ] Tags are accurate
- [ ] Examples are clear
- [ ] Gotchas documented

---

**Extracted by:** DEIA VS Code Extension
**Date:** ${date}
**Source:** ${sourceFile}
`;
  }

  /**
   * Save pattern to .deia/intake/pending/
   */
  private async savePattern(content: string, title: string): Promise<string> {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;

    if (!workspaceRoot) {
      throw new Error('No workspace folder');
    }

    // Create .deia/intake/pending/ if it doesn't exist
    const intakeDir = path.join(workspaceRoot, '.deia', 'intake', 'pending');

    if (!fs.existsSync(intakeDir)) {
      fs.mkdirSync(intakeDir, { recursive: true });
    }

    // Generate filename (slugify title)
    const slug = title
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');

    const filename = `pattern-${slug}.md`;
    const filepath = path.join(intakeDir, filename);

    // Write file
    fs.writeFileSync(filepath, content, 'utf8');

    return filepath;
  }

  /**
   * Extract pattern from conversation log
   */
  public async extractFromConversation(logPath: string): Promise<void> {
    // TODO: Implement conversation-based pattern extraction
    // Parse conversation log, identify code blocks and solutions
    // Use similar metadata prompting as extractFromSelection
  }
}
```

**Add to commands.ts:**

```typescript
// In registerCommands():

context.subscriptions.push(
  vscode.commands.registerCommand('deia.extractPattern', async () => {
    const extractor = new PatternExtractor();
    await extractor.extractFromSelection();
  })
);
```

**Add to package.json:**

```json
{
  "command": "deia.extractPattern",
  "title": "DEIA: Extract Pattern from Selection",
  "icon": "$(lightbulb)"
}
```

---

### Task 2: PII Detection (4-6 hours)

**Goal:** Warn users before saving patterns with PII/secrets

**Files to Create:**
- Create: `src/piiDetector.ts` (new module, ~150 lines)

**Implementation:**

```typescript
// src/piiDetector.ts

export interface PIIMatch {
  type: 'api_key' | 'password' | 'email' | 'ip_address' | 'ssh_key' | 'jwt' | 'credit_card';
  value: string;
  line: number;
  column: number;
}

export class PIIDetector {

  private patterns = {
    api_key: [
      /AKIA[0-9A-Z]{16}/g, // AWS
      /AIza[0-9A-Za-z\-_]{35}/g, // Google
      /sk-[a-zA-Z0-9]{32,}/g, // OpenAI
      /xox[baprs]-[0-9a-zA-Z]{10,}/g, // Slack
      /ghp_[a-zA-Z0-9]{36}/g // GitHub Personal Access Token
    ],

    password: [
      /password\s*[=:]\s*["']([^"']+)["']/gi,
      /pwd\s*[=:]\s*["']([^"']+)["']/gi,
      /passwd\s*[=:]\s*["']([^"']+)["']/gi
    ],

    email: [
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g
    ],

    ip_address: [
      /\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b/g
    ],

    ssh_key: [
      /-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----/g
    ],

    jwt: [
      /eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+/g
    ],

    credit_card: [
      /\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13})\b/g
    ]
  };

  /**
   * Scan text for PII/secrets
   */
  public scan(text: string): PIIMatch[] {
    const matches: PIIMatch[] = [];
    const lines = text.split('\n');

    for (const [type, patterns] of Object.entries(this.patterns)) {
      for (const pattern of patterns) {
        lines.forEach((line, lineIndex) => {
          const lineMatches = [...line.matchAll(pattern)];

          for (const match of lineMatches) {
            matches.push({
              type: type as any,
              value: match[0],
              line: lineIndex + 1,
              column: match.index || 0
            });
          }
        });
      }
    }

    return matches;
  }

  /**
   * Show PII warning dialog
   */
  public async showWarning(matches: PIIMatch[]): Promise<boolean> {
    const typeCount = this.groupByType(matches);
    const message = `⚠️ Potential PII/secrets detected:\n\n${
      Object.entries(typeCount)
        .map(([type, count]) => `  - ${count} ${type}(s)`)
        .join('\n')
    }\n\nReview and redact before submitting to community.`;

    const result = await vscode.window.showWarningMessage(
      message,
      { modal: true },
      'Review Pattern',
      'Cancel'
    );

    return result === 'Review Pattern';
  }

  private groupByType(matches: PIIMatch[]): Record<string, number> {
    return matches.reduce((acc, match) => {
      acc[match.type] = (acc[match.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
  }
}
```

**Integration with PatternExtractor:**

```typescript
// In PatternExtractor.savePattern():

// Before saving, scan for PII
const piiDetector = new PIIDetector();
const piiMatches = piiDetector.scan(content);

if (piiMatches.length > 0) {
  const proceed = await piiDetector.showWarning(piiMatches);
  if (!proceed) {
    return; // User cancelled
  }
}

// Continue with save...
```

---

### Task 3: Pattern Template Editor (3-4 hours)

**Goal:** Provide guided editor for filling in pattern templates

**Files to Create:**
- Create: `src/patternEditor.ts` (new module, ~100 lines)

**Implementation:**

```typescript
// src/patternEditor.ts

import * as vscode from 'vscode';
import * as path from 'path';

export class PatternEditor {

  /**
   * Open pattern file with inline hints
   */
  public async openWithHints(patternPath: string): Promise<void> {
    const doc = await vscode.workspace.openTextDocument(patternPath);
    const editor = await vscode.window.showTextDocument(doc);

    // Add diagnostic hints for TODO sections
    this.addTODOHints(editor);

    vscode.window.showInformationMessage(
      'Fill in the TODO sections to complete your pattern',
      'Show Template Help'
    ).then(selection => {
      if (selection === 'Show Template Help') {
        this.showTemplateHelp();
      }
    });
  }

  /**
   * Add inline hints for TODO sections
   */
  private addTODOHints(editor: vscode.TextEditor): void {
    const doc = editor.document;
    const diagnostics: vscode.Diagnostic[] = [];

    for (let i = 0; i < doc.lineCount; i++) {
      const line = doc.lineAt(i);

      if (line.text.includes('TODO:')) {
        const diagnostic = new vscode.Diagnostic(
          line.range,
          'Complete this section before submitting pattern',
          vscode.DiagnosticSeverity.Information
        );
        diagnostics.push(diagnostic);
      }
    }

    // Create diagnostic collection
    const collection = vscode.languages.createDiagnosticCollection('deia-pattern');
    collection.set(doc.uri, diagnostics);
  }

  /**
   * Show template help panel
   */
  private showTemplateHelp(): void {
    const panel = vscode.window.createWebviewPanel(
      'deiaPatternHelp',
      'DEIA Pattern Template Help',
      vscode.ViewColumn.Beside,
      {}
    );

    panel.webview.html = this.getHelpHTML();
  }

  private getHelpHTML(): string {
    return `<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    h2 { color: #0066cc; }
    code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
  </style>
</head>
<body>
  <h1>Pattern Template Guide</h1>

  <h2>Context Section</h2>
  <p>Describe <strong>when</strong> to use this pattern:</p>
  <ul>
    <li>What situation does it address?</li>
    <li>What are the prerequisites?</li>
    <li>When should you NOT use it?</li>
  </ul>

  <h2>Problem Section</h2>
  <p>Explain the specific problem this pattern solves.</p>

  <h2>Solution Section</h2>
  <p>Describe your approach and show the code.</p>

  <h2>Implementation Section</h2>
  <p>Step-by-step instructions.</p>

  <h2>Gotchas Section</h2>
  <p>Common mistakes, edge cases, performance notes.</p>

  <h2>Related Patterns</h2>
  <p>Link to similar BOK patterns.</p>
</body>
</html>`;
  }
}
```

---

### Task 4: Submit to Intake Command (2-3 hours)

**Goal:** Implement the "Submit Pattern" command (currently a stub)

**Files to Modify:**
- Modify: `src/commands.ts` (replace stub)

**Implementation:**

```typescript
// In commands.ts, replace the stub:

context.subscriptions.push(
  vscode.commands.registerCommand('deia.submitPattern', async () => {
    // List patterns in .deia/intake/pending/
    const workspaceRoot = detector.getDeiaWorkspaceRoot();

    if (!workspaceRoot) {
      vscode.window.showErrorMessage('No DEIA workspace found');
      return;
    }

    const pendingDir = path.join(workspaceRoot, '.deia', 'intake', 'pending');

    if (!fs.existsSync(pendingDir)) {
      vscode.window.showInformationMessage('No pending patterns to submit');
      return;
    }

    const patterns = fs.readdirSync(pendingDir)
      .filter(f => f.endsWith('.md'))
      .map(f => ({ label: f, path: path.join(pendingDir, f) }));

    if (patterns.length === 0) {
      vscode.window.showInformationMessage('No pending patterns to submit');
      return;
    }

    // Let user pick a pattern
    const selected = await vscode.window.showQuickPick(patterns, {
      placeHolder: 'Select pattern to submit'
    });

    if (!selected) return;

    // Read pattern file
    const content = fs.readFileSync(selected.path, 'utf8');

    // Check for TODOs
    if (content.includes('TODO:')) {
      const proceed = await vscode.window.showWarningMessage(
        'Pattern still contains TODO sections. Submit anyway?',
        'Complete TODOs First',
        'Submit Anyway'
      );

      if (proceed === 'Complete TODOs First') {
        // Open pattern for editing
        const doc = await vscode.workspace.openTextDocument(selected.path);
        await vscode.window.showTextDocument(doc);
        return;
      }
    }

    // Scan for PII one more time
    const piiDetector = new PIIDetector();
    const piiMatches = piiDetector.scan(content);

    if (piiMatches.length > 0) {
      const proceed = await piiDetector.showWarning(piiMatches);
      if (!proceed) return;
    }

    // Move to .deia/intake/ (ready for review)
    const targetPath = path.join(
      workspaceRoot,
      '.deia',
      'intake',
      path.basename(selected.path)
    );

    fs.renameSync(selected.path, targetPath);

    vscode.window.showInformationMessage(
      `Pattern submitted for review: ${path.basename(targetPath)}`,
      'View Pattern'
    ).then(selection => {
      if (selection === 'View Pattern') {
        vscode.workspace.openTextDocument(targetPath).then(doc => {
          vscode.window.showTextDocument(doc);
        });
      }
    });
  })
);
```

---

## Phase 3 Summary

**New Files:**
1. `src/patternExtractor.ts` (~200 lines)
2. `src/piiDetector.ts` (~150 lines)
3. `src/patternEditor.ts` (~100 lines)

**Modified Files:**
1. `src/commands.ts` (add extraction + submission commands)
2. `package.json` (add new commands to contributes)

**New Commands:**
1. `DEIA: Extract Pattern from Selection`
2. `DEIA: Submit Pattern to Community` (implement stub)

**Total Effort:** ~15-21 hours coding + ~5-9 hours testing/docs = **20-30 hours**

**Timeline:** 2-3 weeks part-time

---

## Phase 4: BOK Search (Future)

**Goal:** Search and browse community patterns from within VS Code

**Features:**
1. Command: `DEIA: Search Patterns`
2. Sidebar view with search results
3. Preview patterns in webview
4. Insert pattern into code
5. Contextual suggestions (AI-powered)

**Effort:** ~30-40 hours

**Timeline:** 1-2 months

---

## Phase 6: Advanced Features (Future)

**Features:**
1. ML-based PII detection (using local model)
2. Pattern suggestion AI (analyze code, suggest patterns)
3. DEIA API integration (cloud sync, optional)
4. Multi-language support (i18n)

**Effort:** ~60-80 hours

**Timeline:** 3-4 months

---

## Testing Strategy

### Manual Testing (v0.2.0)

**Test Pattern Extraction:**
1. Select code in editor
2. Run `DEIA: Extract Pattern from Selection`
3. Fill in metadata prompts
4. Verify pattern created in `.deia/intake/pending/`
5. Check PII detection triggers for API keys

**Test Pattern Submission:**
1. Run `DEIA: Submit Pattern to Community`
2. Select pending pattern
3. Verify moved to `.deia/intake/`
4. Check PII warning shows for secrets

**Test Pattern Editor:**
1. Extract pattern
2. Open pattern file
3. Verify TODO hints appear
4. Complete TODO sections
5. Submit pattern

### Automated Testing (Future)

- Unit tests for `PatternExtractor` class
- Unit tests for `PIIDetector` regex patterns
- Integration tests for command workflows
- Mock file system for pattern saving

---

## Documentation Updates (v0.2.0)

**Files to Update:**
1. `README.md` - Add Phase 3 features
2. `STATUS.md` - Update to Phase 3 complete
3. `CHANGELOG.md` - Add v0.2.0 entry
4. Create: `PATTERN-EXTRACTION.md` - Pattern extraction guide

**Documentation Effort:** ~4-6 hours

---

## Success Criteria (v0.2.0)

**Must Have:**
- [x] Extract pattern from code selection
- [x] PII detection and warnings
- [x] Pattern saved to `.deia/intake/pending/`
- [x] Submit pattern to `.deia/intake/`
- [x] Pattern template with TODO hints

**Nice to Have:**
- [ ] Extract pattern from conversation log
- [ ] Guided template editor with inline help
- [ ] Auto-detect pattern type (bug-fix, workaround, best-practice)

**Success Metrics:**
- 10+ patterns extracted by users in first month
- 0 PII leaks (detector catches all secrets)
- User feedback: "Pattern extraction saves time"

---

## File Reference

**Current Files:**
- `src/extension.ts` (extensions/vscode-deia/src/extension.ts:1)
- `src/chatParticipant.ts` (extensions/vscode-deia/src/chatParticipant.ts:1)
- `src/commands.ts` (extensions/vscode-deia/src/commands.ts:1)
- `src/conversationMonitor.ts` (extensions/vscode-deia/src/conversationMonitor.ts:1)
- `src/deiaDetector.ts` (extensions/vscode-deia/src/deiaDetector.ts:1)
- `src/deiaLogger.ts` (extensions/vscode-deia/src/deiaLogger.ts:1)
- `src/speckitIntegration.ts` (extensions/vscode-deia/src/speckitIntegration.ts:1)
- `src/statusBar.ts` (extensions/vscode-deia/src/statusBar.ts:1)

**Files to Create:**
- `src/patternExtractor.ts` (NEW)
- `src/piiDetector.ts` (NEW)
- `src/patternEditor.ts` (NEW)
- `docs/PATTERN-EXTRACTION.md` (NEW)

**Pattern Template Reference:**
- `templates/pattern-template.md` (../../templates/pattern-template.md:1)

---

## Related Specifications

- Master Librarian Spec: `.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md`
- Pattern Submission Guide: `docs/guides/PATTERN-SUBMISSION-GUIDE.md`
- BOK Usage Guide: `docs/guides/BOK-USAGE-GUIDE.md`

---

**Next Action:** Start with Task 1 (Pattern Extraction Command) - estimated 6-8 hours

**Questions?** See existing code in `src/commands.ts` for command registration examples
