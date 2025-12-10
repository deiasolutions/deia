import * as vscode from 'vscode';
import { DeiaLogger, ChatMessage } from './deiaLogger';
import { DeiaDetector } from './deiaDetector';

/**
 * Monitors AI conversations and automatically logs them when auto-log is enabled
 */
export class ConversationMonitor implements vscode.Disposable {
    private detector: DeiaDetector;
    private logger: DeiaLogger;
    private conversationBuffer: ChatMessage[] = [];
    private disposables: vscode.Disposable[] = [];
    private isMonitoring: boolean = false;
    private sessionStartTime: Date | null = null;
    private inactivityTimer: NodeJS.Timeout | null = null;
    private readonly INACTIVITY_THRESHOLD_MS = 5 * 60 * 1000; // 5 minutes of inactivity triggers save

    constructor(detector: DeiaDetector) {
        this.detector = detector;
        this.logger = new DeiaLogger();
    }

    /**
     * Start monitoring AI conversations
     */
    public async startMonitoring(): Promise<void> {
        if (this.isMonitoring) {
            return; // Already monitoring
        }

        const config = this.detector.getDeiaConfig();
        if (!config || !config.auto_log) {
            console.log('[DEIA] Auto-log disabled, not starting monitor');
            return;
        }

        console.log('[DEIA] Starting conversation monitoring...');
        this.isMonitoring = true;
        this.sessionStartTime = new Date();

        // Monitor chat participant interactions (our @deia participant)
        // Note: VS Code doesn't provide a global chat event API yet
        // So we rely on file watchers and periodic saves as fallback

        // Watch for file changes as proxy for activity
        const fileWatcher = vscode.workspace.createFileSystemWatcher('**/*');

        fileWatcher.onDidChange(() => this.onActivity());
        fileWatcher.onDidCreate(() => this.onActivity());

        this.disposables.push(fileWatcher);

        // Listen for text document changes (AI-assisted edits)
        const docChangeListener = vscode.workspace.onDidChangeTextDocument((e) => {
            // Only track changes in workspace files, not output/debug consoles
            if (e.document.uri.scheme === 'file') {
                this.onActivity();
            }
        });

        this.disposables.push(docChangeListener);

        console.log('[DEIA] Monitoring started');
    }

    /**
     * Stop monitoring
     */
    public stopMonitoring(): void {
        if (!this.isMonitoring) {
            return;
        }

        console.log('[DEIA] Stopping conversation monitoring...');
        this.isMonitoring = false;

        // Save any buffered conversation before stopping
        if (this.conversationBuffer.length > 0) {
            this.saveBufferedConversation('Session ended');
        }

        // Clear inactivity timer
        if (this.inactivityTimer) {
            clearTimeout(this.inactivityTimer);
            this.inactivityTimer = null;
        }

        // Dispose all listeners
        this.disposables.forEach(d => d.dispose());
        this.disposables = [];

        console.log('[DEIA] Monitoring stopped');
    }

    /**
     * Add a message to the conversation buffer
     */
    public addMessage(role: 'user' | 'assistant', content: string): void {
        if (!this.isMonitoring) {
            return;
        }

        this.conversationBuffer.push({
            role,
            content
        });

        console.log(`[DEIA] Added ${role} message (buffer: ${this.conversationBuffer.length} messages)`);

        // Reset inactivity timer
        this.resetInactivityTimer();
    }

    /**
     * Add multiple messages at once
     */
    public addMessages(messages: ChatMessage[]): void {
        if (!this.isMonitoring) {
            return;
        }

        this.conversationBuffer.push(...messages);
        console.log(`[DEIA] Added ${messages.length} messages (buffer: ${this.conversationBuffer.length} messages)`);

        this.resetInactivityTimer();
    }

    /**
     * Manually trigger save of current conversation
     */
    public async saveNow(context?: string): Promise<string | undefined> {
        if (this.conversationBuffer.length === 0) {
            console.log('[DEIA] No messages to save');
            return undefined;
        }

        return this.saveBufferedConversation(context || 'Manual save');
    }

    /**
     * Called when user activity is detected
     */
    private onActivity(): void {
        if (!this.isMonitoring) {
            return;
        }

        // Reset inactivity timer on any activity
        this.resetInactivityTimer();
    }

    /**
     * Reset the inactivity timer
     */
    private resetInactivityTimer(): void {
        if (this.inactivityTimer) {
            clearTimeout(this.inactivityTimer);
        }

        this.inactivityTimer = setTimeout(() => {
            this.onInactivityTimeout();
        }, this.INACTIVITY_THRESHOLD_MS);
    }

    /**
     * Called when inactivity threshold is reached
     */
    private async onInactivityTimeout(): Promise<void> {
        console.log('[DEIA] Inactivity detected, saving conversation...');

        if (this.conversationBuffer.length > 0) {
            await this.saveBufferedConversation('Auto-save after inactivity');
        }
    }

    /**
     * Save the buffered conversation to DEIA
     */
    private async saveBufferedConversation(context: string): Promise<string | undefined> {
        const workspaceRoot = this.detector.getDeiaWorkspaceRoot();

        if (!workspaceRoot) {
            console.log('[DEIA] No workspace root, cannot save');
            return undefined;
        }

        if (this.conversationBuffer.length === 0) {
            console.log('[DEIA] No messages in buffer');
            return undefined;
        }

        try {
            console.log(`[DEIA] Saving ${this.conversationBuffer.length} messages...`);

            // Use the logger to save via DEIA CLI
            const logPath = await this.logger.logConversation(workspaceRoot, {
                context,
                messages: [...this.conversationBuffer] // Copy array
            });

            if (logPath) {
                console.log(`[DEIA] Conversation saved: ${logPath}`);

                // Show subtle notification
                vscode.window.showInformationMessage(
                    `DEIA: Conversation auto-logged (${this.conversationBuffer.length} messages)`,
                    'View Log'
                ).then(selection => {
                    if (selection === 'View Log') {
                        vscode.workspace.openTextDocument(logPath).then(doc => {
                            vscode.window.showTextDocument(doc);
                        });
                    }
                });

                // Clear buffer after successful save
                this.conversationBuffer = [];
                this.sessionStartTime = new Date(); // Reset session start time

                return logPath;
            }

            return undefined;

        } catch (error) {
            console.error('[DEIA] Error saving conversation:', error);
            vscode.window.showErrorMessage(`DEIA auto-log failed: ${error}`);
            return undefined;
        }
    }

    /**
     * Get current buffer size
     */
    public getBufferSize(): number {
        return this.conversationBuffer.length;
    }

    /**
     * Check if monitoring is active
     */
    public isActive(): boolean {
        return this.isMonitoring;
    }

    /**
     * Get session duration in milliseconds
     */
    public getSessionDuration(): number {
        if (!this.sessionStartTime) {
            return 0;
        }
        return Date.now() - this.sessionStartTime.getTime();
    }

    /**
     * Dispose the monitor
     */
    public dispose(): void {
        this.stopMonitoring();
    }
}
