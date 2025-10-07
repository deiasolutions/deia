import * as vscode from 'vscode';
import { DeiaDetector } from './deiaDetector';
import { DeiaStatusBar } from './statusBar';
import { registerCommands } from './commands';
import { DeiaChatParticipant } from './chatParticipant';

let statusBar: DeiaStatusBar | undefined;
let detector: DeiaDetector | undefined;
let chatParticipant: DeiaChatParticipant | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('DEIA extension activating...');

    // Initialize DEIA detector
    detector = new DeiaDetector();

    // Check if current workspace has DEIA
    const hasDeiaWorkspace = detector.hasDeiaInWorkspace();

    if (hasDeiaWorkspace) {
        console.log('DEIA-enabled workspace detected');

        // Initialize status bar
        const config = detector.getDeiaConfig();
        statusBar = new DeiaStatusBar(config?.auto_log ?? false);
        context.subscriptions.push(statusBar);

        // Initialize chat participant
        chatParticipant = new DeiaChatParticipant(detector);
        context.subscriptions.push(chatParticipant);
    }

    // Register commands (always available)
    registerCommands(context, detector, statusBar);

    // Watch for workspace folder changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeWorkspaceFolders(() => {
            const nowHasDeia = detector?.hasDeiaInWorkspace() ?? false;

            if (nowHasDeia && !statusBar) {
                // DEIA was added to workspace
                const config = detector?.getDeiaConfig();
                statusBar = new DeiaStatusBar(config?.auto_log ?? false);
                context.subscriptions.push(statusBar);

                vscode.window.showInformationMessage('DEIA detected in workspace!');
            } else if (!nowHasDeia && statusBar) {
                // DEIA was removed
                statusBar.dispose();
                statusBar = undefined;
            }
        })
    );

    console.log('DEIA extension activated');
}

export function deactivate() {
    console.log('DEIA extension deactivated');
}
