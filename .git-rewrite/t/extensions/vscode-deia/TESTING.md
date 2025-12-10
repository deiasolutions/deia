# Testing the DEIA VSCode Extension

## Quick Start

### 1. Compile the Extension

```bash
cd extensions/vscode-deia
npm install
npm run compile
```

### 2. Test in VSCode

**Method A: Launch from VSCode**
1. Open `extensions/vscode-deia` folder in VSCode
2. Press `F5` (or Run → Start Debugging)
3. A new "Extension Development Host" window opens
4. The DEIA extension is loaded in this window

**Method B: Command Line**
```bash
code --extensionDevelopmentPath=./extensions/vscode-deia
```

### 3. Create a Test Project

In the Extension Development Host window:

```bash
# Create test project
mkdir ~/deia-test
cd ~/deia-test

# Initialize DEIA (if you have CLI installed)
deia init

# Or manually create structure
mkdir -p .deia/sessions
echo '{"project": "test", "auto_log": false}' > .deia/config.json
echo "# Session Index" > .deia/sessions/INDEX.md
echo "# Project Resume" > project_resume.md
```

### 4. Test Commands

Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`):

- `DEIA: Check Status` - Should show DEIA detected
- `DEIA: Read Project Resume` - Opens `project_resume.md`
- `DEIA: View Session Logs` - Opens `.deia/sessions/` directory
- `DEIA: Toggle Auto-Logging` - Toggles auto-log on/off

### 5. Test Chat Participant

If you have a chat extension (Copilot, Continue, etc.):

1. Open chat panel
2. Type `@deia help`
3. Should show DEIA help message
4. Type `@deia status`
5. Should show configuration status
6. Type `@deia log`
7. Should log the conversation

---

## Testing Checklist

### Core Functionality

- [ ] **Extension Activation**
  - [ ] Extension activates on VSCode startup
  - [ ] No errors in Developer Console (`Help > Toggle Developer Tools`)
  - [ ] Status bar shows "DEIA: Manual" or "DEIA: Auto-log ON"

- [ ] **DEIA Detection**
  - [ ] Detects `.deia/` directory when present
  - [ ] Status bar shows correctly
  - [ ] `DEIA: Check Status` shows correct config
  - [ ] Works when opening workspace with DEIA
  - [ ] Works when adding DEIA to workspace

- [ ] **Manual Logging**
  - [ ] `DEIA: Log Current Chat` command exists
  - [ ] Creates file in `.deia/sessions/`
  - [ ] Updates `INDEX.md`
  - [ ] Updates `project_resume.md`
  - [ ] Filename has timestamp

- [ ] **Resume Reading**
  - [ ] `DEIA: Read Project Resume` opens file
  - [ ] Shows current project context
  - [ ] Creates file if missing

- [ ] **Session Viewing**
  - [ ] `DEIA: View Session Logs` opens directory
  - [ ] Shows all session files
  - [ ] Opens in VSCode explorer

- [ ] **Auto-Log Toggle**
  - [ ] `DEIA: Toggle Auto-Logging` command works
  - [ ] Updates `.deia/config.json`
  - [ ] Status bar updates immediately
  - [ ] Change persists across VSCode restarts

### Chat Participant

- [ ] **@deia Commands**
  - [ ] `@deia help` shows help text
  - [ ] `@deia status` shows config
  - [ ] `@deia log` logs conversation
  - [ ] Error handling when DEIA not initialized

### SpecKit Integration

- [ ] **Create Spec from Conversation**
  - [ ] Command appears in palette
  - [ ] Prompts to select conversation log
  - [ ] Prompts for spec name
  - [ ] Creates file in `specs/` directory
  - [ ] Spec format is valid
  - [ ] Extracts requirements/decisions/architecture

- [ ] **Update Constitution**
  - [ ] Command appears in palette
  - [ ] Prompts to select conversation log
  - [ ] Shows preview of extracted decisions
  - [ ] Updates `.specify/memory/constitution.md`
  - [ ] Preserves existing constitution content
  - [ ] Creates file if missing

### Error Handling

- [ ] **No DEIA Project**
  - [ ] Commands show helpful error message
  - [ ] Suggests running `deia init`
  - [ ] Doesn't crash extension

- [ ] **Missing Files**
  - [ ] Handles missing `config.json` gracefully
  - [ ] Creates `INDEX.md` if missing
  - [ ] Creates `project_resume.md` if missing

- [ ] **Permission Errors**
  - [ ] Shows error if can't write to `.deia/`
  - [ ] Doesn't crash extension

---

## Manual Test Scenarios

### Scenario 1: First-Time User

```
1. User installs extension
2. Opens project without DEIA
3. Runs "DEIA: Check Status"
   → Should show "No DEIA-enabled workspace"
   → Should suggest running "deia init"
4. User runs "deia init" in terminal
5. Extension detects new .deia/ folder
   → Status bar appears
6. User runs "DEIA: Log Current Chat"
   → Creates first session log
   → Success!
```

### Scenario 2: Existing DEIA User

```
1. User opens existing DEIA project
2. Extension auto-detects .deia/
   → Status bar shows "DEIA: Manual"
3. User reads project_resume.md
   → Sees where they left off
4. User works, has chat conversation
5. User runs "@deia log"
   → Conversation saved
6. User checks .deia/sessions/
   → New log file exists
```

### Scenario 3: SpecKit Workflow

```
1. User has conversation about architecture
2. DEIA logs it
3. User runs "Create SpecKit Spec from Conversation"
   → Picks recent log
   → Names it "api-design"
4. Check specs/api-design.md
   → Spec exists with extracted content
5. User runs "Add Decisions to SpecKit Constitution"
   → Picks same log
   → Previews decisions
   → Confirms
6. Check .specify/memory/constitution.md
   → Decisions added
```

### Scenario 4: Crash Recovery

```
1. User working with AI
2. "@deia log" periodically
3. VSCode crashes
4. User reopens VSCode
5. User runs "DEIA: Read Project Resume"
   → Sees last session summary
6. User checks .deia/sessions/
   → All logs preserved
   → Context recovered
```

---

## Debugging

### View Extension Logs

1. `Help > Toggle Developer Tools`
2. Click "Console" tab
3. Look for "DEIA" messages

### Common Issues

**"Cannot find module 'vscode'"**
- Run `npm install` in `extensions/vscode-deia`

**"Command not found: deia.logChat"**
- Check `package.json` - command IDs must match
- Reload window: `Ctrl+R` / `Cmd+R`

**"Extension not activating"**
- Check `activationEvents` in `package.json`
- Check console for errors
- Try `Ctrl+R` to reload

**"Status bar not showing"**
- Check `deia.showStatusBar` setting
- Ensure `.deia/` directory exists
- Check extension activation in console

### Enable Verbose Logging

Add to `extension.ts`:

```typescript
export function activate(context: vscode.ExtensionContext) {
    console.log('[DEIA] Extension activating...');
    console.log('[DEIA] Workspace folders:', vscode.workspace.workspaceFolders);
    // ...
}
```

---

## Automated Testing (TODO)

### Unit Tests

```bash
npm run test
```

**Test files to create:**
- `test/suite/deiaDetector.test.ts`
- `test/suite/deiaLogger.test.ts`
- `test/suite/commands.test.ts`
- `test/suite/speckitIntegration.test.ts`

### Integration Tests

Test full workflows:
- Initialize DEIA → Log conversation → Verify file created
- Create spec → Verify SpecKit format
- Update constitution → Verify content added

---

## Performance Testing

### Startup Time

Measure extension activation:

```typescript
const startTime = Date.now();
// ... activation code ...
console.log(`DEIA activated in ${Date.now() - startTime}ms`);
```

**Target:** < 500ms activation time

### File Operations

Test with large conversation logs:
- 100 KB log file
- 1000 session files
- Should remain responsive

---

## Pre-Release Checklist

Before publishing to marketplace:

- [ ] All commands work
- [ ] No console errors
- [ ] README.md is complete
- [ ] CHANGELOG.md exists
- [ ] package.json metadata correct
- [ ] Icon and images added
- [ ] Tested on Windows, macOS, Linux
- [ ] Tested with different AI assistants
- [ ] SpecKit integration tested (if SpecKit installed)
- [ ] Version number updated
- [ ] Git tag created

---

## Packaging for Distribution

### Create VSIX Package

```bash
npm install -g @vscode/vsce
cd extensions/vscode-deia
vsce package
```

Creates `deia-0.1.0.vsix`

### Install Locally

```bash
code --install-extension deia-0.1.0.vsix
```

### Publish to Marketplace

```bash
vsce publish
```

(Requires publisher account and PAT from Visual Studio Marketplace)

---

## Continuous Testing

### During Development

```bash
npm run watch
```

Leave this running - it recompiles on file changes.

In VSCode Extension Development Host:
- Press `Ctrl+R` / `Cmd+R` to reload extension after changes

### Before Each Commit

1. `npm run compile` - Ensure no TypeScript errors
2. `npm run lint` - Check code style
3. Test key commands manually
4. Check Developer Console for errors

---

## Reporting Issues

If you find bugs during testing:

1. Note the steps to reproduce
2. Check Developer Console for errors
3. Create GitHub issue with:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Console errors (if any)
   - VSCode version
   - Extension version

---

**Happy Testing!** 🧪
