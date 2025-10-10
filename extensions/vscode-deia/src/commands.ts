import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { DeiaDetector } from './deiaDetector';
import { DeiaStatusBar } from './statusBar';
import { DeiaLogger, ChatMessage } from './deiaLogger';
import { SpecKitIntegration } from './speckitIntegration';
import { ConversationMonitor } from './conversationMonitor';

/**
 * Register all DEIA commands
 */
export function registerCommands(
    context: vscode.ExtensionContext,
    detector: DeiaDetector,
    statusBar?: DeiaStatusBar,
    monitor?: ConversationMonitor
): void {
    const logger = new DeiaLogger();

    // Command: Log Current Chat
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.logChat', async () => {
            await logCurrentChat(detector, logger);
        })
    );

    // Command: View Session Logs
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.viewLogs', async () => {
            await viewSessionLogs(detector);
        })
    );

    // Command: View Project Resume
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.viewResume', async () => {
            await viewProjectResume(detector);
        })
    );

    // Command: Check Status
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.checkStatus', async () => {
            await checkStatus(detector);
        })
    );

    // Command: Submit Pattern
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.submitPattern', async () => {
            await submitPattern(detector);
        })
    );

    // Command: Toggle Auto-Log
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.toggleAutoLog', async () => {
            await toggleAutoLog(detector, statusBar, monitor);
        })
    );

    // Command: Create SpecKit Spec from Log
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.createSpecFromLog', async () => {
            await createSpecFromLog(detector);
        })
    );

    // Command: Update SpecKit Constitution
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.updateConstitution', async () => {
            await updateConstitution(detector);
        })
    );

    // Command: Save conversation buffer now
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.saveBuffer', async () => {
            await saveBufferNow(monitor);
        })
    );

    // Command: Show monitor status
    context.subscriptions.push(
        vscode.commands.registerCommand('deia.monitorStatus', async () => {
            await showMonitorStatus(monitor);
        })
    );
}

/**
 * Log current chat conversation
 */
async function logCurrentChat(detector: DeiaDetector, logger: DeiaLogger): Promise<void> {
    const workspaceRoot = detector.getDeiaWorkspaceRoot();

    if (!workspaceRoot) {
        vscode.window.showWarningMessage(
            'No DEIA-enabled workspace found. Run "deia init" in your project first.'
        );
        return;
    }

    // Check if DEIA CLI is available
    const cliAvailable = await logger.isDeiaCliAvailable();
    if (!cliAvailable) {
        vscode.window.showErrorMessage(
            'DEIA CLI not found. Install DEIA: pip install -e /path/to/deia'
        );
        return;
    }

    // VSCode doesn't provide API to access chat history from commands
    // Users must use @deia participant instead
    const choice = await vscode.window.showInformationMessage(
        'To log AI conversations, use the @deia chat participant.\n\nType "@deia log" in your chat window to save the conversation.',
        'Got it',
        'Show Help'
    );

    if (choice === 'Show Help') {
        // Show help in a new markdown preview
        const helpContent = `# How to Log Conversations with DEIA

## Using the @deia Chat Participant

1. Open your AI chat (Copilot, Continue, Cody, etc.)
2. Have your conversation with the AI
3. Type: \`@deia log\`
4. DEIA will extract and save the entire conversation

## Available @deia Commands

- \`@deia log\` - Save the current conversation to DEIA
- \`@deia status\` - Check DEIA configuration
- \`@deia help\` - Show available commands

## What Gets Logged?

- All user messages in the conversation
- All AI responses
- Saved to \`.deia/sessions/\` with timestamp
- Automatically updates project resume and index

## Manual Logging

If you prefer, you can also manually save conversations:
1. Copy the chat content
2. Create a file in \`.deia/sessions/\`
3. Use the SpecKit commands to extract specs/decisions
`;

        const doc = await vscode.workspace.openTextDocument({
            content: helpContent,
            language: 'markdown'
        });
        vscode.window.showTextDocument(doc);
    }
}

/**
 * View session logs
 */
async function viewSessionLogs(detector: DeiaDetector): Promise<void> {
    const sessionsPath = detector.getSessionsPath();

    if (!sessionsPath) {
        vscode.window.showWarningMessage(
            'No DEIA-enabled workspace found.'
        );
        return;
    }

    if (!fs.existsSync(sessionsPath)) {
        vscode.window.showInformationMessage(
            'No session logs yet. Start logging conversations!'
        );
        return;
    }

    // Open sessions directory in file explorer
    const uri = vscode.Uri.file(sessionsPath);
    vscode.commands.executeCommand('revealFileInOS', uri);
}

/**
 * View project resume
 */
async function viewProjectResume(detector: DeiaDetector): Promise<void> {
    const resumePath = detector.getProjectResumePath();

    if (!resumePath) {
        vscode.window.showWarningMessage(
            'No DEIA-enabled workspace found.'
        );
        return;
    }

    if (!fs.existsSync(resumePath)) {
        vscode.window.showInformationMessage(
            'No project resume yet. It will be created when you log your first conversation.'
        );
        return;
    }

    // Open project resume
    vscode.workspace.openTextDocument(resumePath).then(doc => {
        vscode.window.showTextDocument(doc);
    });
}

/**
 * Check DEIA status
 */
async function checkStatus(detector: DeiaDetector): Promise<void> {
    const config = detector.getDeiaConfig();

    if (!config) {
        vscode.window.showInformationMessage(
            'No DEIA-enabled workspace. Run "deia init" to get started.',
            'Learn More'
        ).then(selection => {
            if (selection === 'Learn More') {
                vscode.env.openExternal(vscode.Uri.parse('https://github.com/deiasolutions/deia'));
            }
        });
        return;
    }

    const message = `
**DEIA Status**

Project: ${config.project}
User: ${config.user}
Auto-log: ${config.auto_log ? 'ON' : 'OFF'}
Version: ${config.version}

Sessions: ${detector.getSessionsPath()}
    `.trim();

    vscode.window.showInformationMessage(message);
}

/**
 * Submit pattern to community
 */
async function submitPattern(detector: DeiaDetector): Promise<void> {
    const workspaceRoot = detector.getDeiaWorkspaceRoot();

    if (!workspaceRoot) {
        vscode.window.showWarningMessage(
            'No DEIA-enabled workspace found.'
        );
        return;
    }

    // Show coming soon message
    vscode.window.showInformationMessage(
        'Pattern submission coming soon! This will sanitize and submit patterns to the DEIA community.',
        'Learn More'
    ).then(selection => {
        if (selection === 'Learn More') {
            vscode.env.openExternal(vscode.Uri.parse('https://github.com/deiasolutions/deia/blob/master/CONTRIBUTING.md'));
        }
    });
}

/**
 * Toggle auto-logging
 */
async function toggleAutoLog(detector: DeiaDetector, statusBar?: DeiaStatusBar, monitor?: ConversationMonitor): Promise<void> {
    const config = detector.getDeiaConfig();
    const deiaPath = detector.getDeiaPath();

    if (!config || !deiaPath) {
        vscode.window.showWarningMessage(
            'No DEIA-enabled workspace found.'
        );
        return;
    }

    // Toggle the setting
    const newValue = !config.auto_log;
    config.auto_log = newValue;

    // Save to config file
    const configPath = `${deiaPath}/config.json`;
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');

    // Update status bar
    if (statusBar) {
        statusBar.setAutoLog(newValue);
    }

    // Start or stop monitoring
    if (monitor) {
        if (newValue) {
            await monitor.startMonitoring();
            console.log('[DEIA] Auto-logging enabled, monitoring started');
        } else {
            monitor.stopMonitoring();
            console.log('[DEIA] Auto-logging disabled, monitoring stopped');
        }
    }

    vscode.window.showInformationMessage(
        `DEIA auto-logging ${newValue ? 'enabled' : 'disabled'}`
    );
}

/**
 * Create SpecKit specification from DEIA conversation log
 */
async function createSpecFromLog(detector: DeiaDetector): Promise<void> {
    const workspaceRoot = detector.getDeiaWorkspaceRoot();
    const sessionsPath = detector.getSessionsPath();

    if (!workspaceRoot || !sessionsPath) {
        vscode.window.showWarningMessage('No DEIA-enabled workspace found.');
        return;
    }

    // Initialize SpecKit integration
    const speckit = new SpecKitIntegration(workspaceRoot);

    // Check if SpecKit is initialized
    if (!speckit.isSpecKitProject()) {
        const choice = await vscode.window.showInformationMessage(
            'SpecKit not detected in this project. Initialize SpecKit first?',
            'Learn More',
            'Cancel'
        );

        if (choice === 'Learn More') {
            vscode.env.openExternal(vscode.Uri.parse('https://github.com/github/spec-kit'));
        }
        return;
    }

    // Get list of session logs
    const logFiles = fs.readdirSync(sessionsPath)
        .filter(f => f.endsWith('.md'))
        .map(f => path.join(sessionsPath, f));

    if (logFiles.length === 0) {
        vscode.window.showInformationMessage('No conversation logs found.');
        return;
    }

    // Let user pick a log file
    const logFileNames = logFiles.map(f => path.basename(f));
    const selected = await vscode.window.showQuickPick(logFileNames, {
        placeHolder: 'Select a conversation log to convert to spec'
    });

    if (!selected) {
        return;
    }

    const selectedLog = logFiles[logFileNames.indexOf(selected)];

    // Prompt for spec name
    const specName = await vscode.window.showInputBox({
        prompt: 'Enter a name for the specification',
        placeHolder: 'e.g., user-authentication-spec',
        value: path.basename(selected, '.md')
    });

    if (!specName) {
        return;
    }

    try {
        const specPath = await speckit.createSpecFromLog(selectedLog, specName);

        if (specPath) {
            vscode.window.showInformationMessage(
                `Specification created: ${specName}.md`,
                'Open Spec'
            ).then(choice => {
                if (choice === 'Open Spec') {
                    vscode.workspace.openTextDocument(specPath).then(doc => {
                        vscode.window.showTextDocument(doc);
                    });
                }
            });
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to create spec: ${error}`);
    }
}

/**
 * Add decisions from DEIA log to SpecKit constitution
 */
async function updateConstitution(detector: DeiaDetector): Promise<void> {
    const workspaceRoot = detector.getDeiaWorkspaceRoot();
    const sessionsPath = detector.getSessionsPath();

    if (!workspaceRoot || !sessionsPath) {
        vscode.window.showWarningMessage('No DEIA-enabled workspace found.');
        return;
    }

    // Initialize SpecKit integration
    const speckit = new SpecKitIntegration(workspaceRoot);

    // Check if SpecKit is initialized
    if (!speckit.isSpecKitProject()) {
        vscode.window.showInformationMessage(
            'SpecKit not detected in this project. Initialize SpecKit first.',
            'Learn More'
        ).then(choice => {
            if (choice === 'Learn More') {
                vscode.env.openExternal(vscode.Uri.parse('https://github.com/github/spec-kit'));
            }
        });
        return;
    }

    // Get constitution path
    const constitutionPath = speckit.getConstitutionPath();

    if (!constitutionPath) {
        vscode.window.showWarningMessage('SpecKit constitution not found.');
        return;
    }

    // Get list of session logs
    const logFiles = fs.readdirSync(sessionsPath)
        .filter(f => f.endsWith('.md'))
        .map(f => path.join(sessionsPath, f));

    if (logFiles.length === 0) {
        vscode.window.showInformationMessage('No conversation logs found.');
        return;
    }

    // Let user pick a log file
    const logFileNames = logFiles.map(f => path.basename(f));
    const selected = await vscode.window.showQuickPick(logFileNames, {
        placeHolder: 'Select a conversation log to extract decisions from'
    });

    if (!selected) {
        return;
    }

    const selectedLog = logFiles[logFileNames.indexOf(selected)];

    try {
        const suggestion = await speckit.suggestConstitutionUpdate(selectedLog);

        if (!suggestion) {
            vscode.window.showInformationMessage('No decisions found in this conversation.');
            return;
        }

        // Show preview and ask for confirmation
        const choice = await vscode.window.showInformationMessage(
            'Add these decisions to SpecKit constitution?',
            'Preview',
            'Add',
            'Cancel'
        );

        if (choice === 'Preview') {
            // Show suggestion in new document
            const doc = await vscode.workspace.openTextDocument({
                content: suggestion,
                language: 'markdown'
            });
            vscode.window.showTextDocument(doc);
            return;
        }

        if (choice === 'Add') {
            // Append to constitution
            const currentContent = fs.readFileSync(constitutionPath, 'utf-8');
            const newContent = currentContent + '\n' + suggestion;
            fs.writeFileSync(constitutionPath, newContent, 'utf-8');

            vscode.window.showInformationMessage(
                'Constitution updated!',
                'Open Constitution'
            ).then(openChoice => {
                if (openChoice === 'Open Constitution') {
                    vscode.workspace.openTextDocument(constitutionPath).then(doc => {
                        vscode.window.showTextDocument(doc);
                    });
                }
            });
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to update constitution: ${error}`);
    }
}

/**
 * Manually save the conversation buffer
 */
async function saveBufferNow(monitor?: ConversationMonitor): Promise<void> {
    if (!monitor) {
        vscode.window.showWarningMessage('Conversation monitor not available.');
        return;
    }

    const bufferSize = monitor.getBufferSize();

    if (bufferSize === 0) {
        vscode.window.showInformationMessage('No conversation messages in buffer.');
        return;
    }

    // Prompt for context
    const context = await vscode.window.showInputBox({
        prompt: 'Describe what you were working on',
        placeHolder: 'e.g., Implementing auto-logging feature'
    });

    if (!context) {
        return; // User cancelled
    }

    try {
        const logPath = await monitor.saveNow(context);

        if (logPath) {
            vscode.window.showInformationMessage(
                `Saved ${bufferSize} messages to DEIA`,
                'View Log'
            ).then(selection => {
                if (selection === 'View Log') {
                    vscode.workspace.openTextDocument(logPath).then(doc => {
                        vscode.window.showTextDocument(doc);
                    });
                }
            });
        } else {
            vscode.window.showWarningMessage('Failed to save conversation buffer.');
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Error saving buffer: ${error}`);
    }
}

/**
 * Show monitor status
 */
async function showMonitorStatus(monitor?: ConversationMonitor): Promise<void> {
    if (!monitor) {
        vscode.window.showWarningMessage('Conversation monitor not available.');
        return;
    }

    const isActive = monitor.isActive();
    const bufferSize = monitor.getBufferSize();
    const duration = monitor.getSessionDuration();

    const durationMinutes = Math.floor(duration / 60000);
    const durationSeconds = Math.floor((duration % 60000) / 1000);

    const statusMessage = `
**Auto-Logging Monitor**

Status: ${isActive ? '🟢 Active' : '⚫ Inactive'}
Buffer: ${bufferSize} messages
Session Duration: ${durationMinutes}m ${durationSeconds}s

${isActive ? 'Monitoring AI conversations and file changes.' : 'Enable auto-log to start monitoring.'}
    `.trim();

    const action = isActive ? 'Save Buffer Now' : 'Enable Auto-Log';

    vscode.window.showInformationMessage(
        statusMessage,
        action,
        'Close'
    ).then(selection => {
        if (selection === 'Save Buffer Now' && isActive) {
            vscode.commands.executeCommand('deia.saveBuffer');
        } else if (selection === 'Enable Auto-Log' && !isActive) {
            vscode.commands.executeCommand('deia.toggleAutoLog');
        }
    });
}
