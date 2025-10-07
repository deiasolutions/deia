import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { DeiaDetector } from './deiaDetector';
import { DeiaStatusBar } from './statusBar';
import { DeiaLogger, ChatMessage } from './deiaLogger';
import { SpecKitIntegration } from './speckitIntegration';

/**
 * Register all DEIA commands
 */
export function registerCommands(
    context: vscode.ExtensionContext,
    detector: DeiaDetector,
    statusBar?: DeiaStatusBar
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
            await toggleAutoLog(detector, statusBar);
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

    // TODO: Extract chat messages from current chat window
    // For now, show a message that this requires chat API access
    vscode.window.showInformationMessage(
        'Chat extraction coming soon! For now, use the @deia chat participant or manual logging.'
    );

    // Placeholder: Manual interactive logging
    const messages: ChatMessage[] = [
        { role: 'user', content: 'Placeholder conversation' },
        { role: 'assistant', content: 'This is a placeholder. Chat extraction will be implemented with Chat API.' }
    ];

    try {
        const logPath = await logger.logInteractive(workspaceRoot, messages);

        if (logPath) {
            vscode.window.showInformationMessage(
                `Conversation logged to: ${logPath}`,
                'Open Log'
            ).then(selection => {
                if (selection === 'Open Log') {
                    vscode.workspace.openTextDocument(logPath).then(doc => {
                        vscode.window.showTextDocument(doc);
                    });
                }
            });
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to log conversation: ${error}`);
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
async function toggleAutoLog(detector: DeiaDetector, statusBar?: DeiaStatusBar): Promise<void> {
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
