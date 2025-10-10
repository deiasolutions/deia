import * as vscode from 'vscode';
import { DeiaDetector } from './deiaDetector';
import { DeiaStatusBar } from './statusBar';
import { registerCommands } from './commands';
import { DeiaChatParticipant } from './chatParticipant';
import { ConversationMonitor } from './conversationMonitor';

let statusBar: DeiaStatusBar | undefined;
let detector: DeiaDetector | undefined;
let chatParticipant: DeiaChatParticipant | undefined;
let conversationMonitor: ConversationMonitor | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('DEIA extension activating...');

    // Initialize DEIA detector
    detector = new DeiaDetector();

    // Initialize conversation monitor (always available)
    conversationMonitor = new ConversationMonitor(detector);
    context.subscriptions.push(conversationMonitor);

    // Initialize chat participant (always available, even without DEIA workspace)
    chatParticipant = new DeiaChatParticipant(detector, conversationMonitor);
    context.subscriptions.push(chatParticipant);

    // Check if current workspace has DEIA
    const hasDeiaWorkspace = detector.hasDeiaInWorkspace();

    if (hasDeiaWorkspace) {
        console.log('DEIA-enabled workspace detected');

        // Initialize status bar
        const config = detector.getDeiaConfig();
        statusBar = new DeiaStatusBar(config?.auto_log ?? false);
        context.subscriptions.push(statusBar);

        // Start monitoring if auto-log is enabled
        if (config?.auto_log) {
            conversationMonitor.startMonitoring();
        }
    }

    // Register commands (always available)
    registerCommands(context, detector, statusBar, conversationMonitor);

    // Watch for workspace folder changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeWorkspaceFolders(() => {
            const nowHasDeia = detector?.hasDeiaInWorkspace() ?? false;

            if (nowHasDeia && !statusBar) {
                // DEIA was added to workspace
                const config = detector?.getDeiaConfig();
                statusBar = new DeiaStatusBar(config?.auto_log ?? false);
                context.subscriptions.push(statusBar);

                // Start monitoring if auto-log is enabled
                if (config?.auto_log && conversationMonitor) {
                    conversationMonitor.startMonitoring();
                }

                vscode.window.showInformationMessage('DEIA detected in workspace!');
            } else if (!nowHasDeia && statusBar) {
                // DEIA was removed
                statusBar.dispose();
                statusBar = undefined;

                // Stop monitoring
                if (conversationMonitor) {
                    conversationMonitor.stopMonitoring();
                }
            }
        })
    );

    console.log('DEIA extension activated');
}

export function deactivate() {
    console.log('DEIA extension deactivated');
}
