import * as vscode from 'vscode';
import { DeiaDetector } from './deiaDetector';
import { DeiaLogger, ChatMessage } from './deiaLogger';

/**
 * @deia chat participant for logging conversations
 */
export class DeiaChatParticipant implements vscode.Disposable {
    private participant: vscode.ChatParticipant;
    private detector: DeiaDetector;
    private logger: DeiaLogger;

    constructor(detector: DeiaDetector) {
        this.detector = detector;
        this.logger = new DeiaLogger();

        // Create chat participant
        this.participant = vscode.chat.createChatParticipant(
            'deia',
            this.handleChatRequest.bind(this)
        );

        this.participant.iconPath = vscode.Uri.parse('$(save)');
    }

    /**
     * Handle chat requests to @deia
     */
    private async handleChatRequest(
        request: vscode.ChatRequest,
        context: vscode.ChatContext,
        stream: vscode.ChatResponseStream,
        token: vscode.CancellationToken
    ): Promise<vscode.ChatResult> {
        const workspaceRoot = this.detector.getDeiaWorkspaceRoot();

        if (!workspaceRoot) {
            stream.markdown('⚠️ No DEIA-enabled workspace found. Run `deia init` in your project first.');
            return { metadata: { command: 'no-workspace' } };
        }

        // Parse command from user's prompt
        const userPrompt = request.prompt.toLowerCase().trim();

        // Command: log this conversation
        if (userPrompt.includes('log')) {
            return await this.handleLogCommand(context, stream, workspaceRoot);
        }

        // Command: status
        if (userPrompt.includes('status')) {
            return await this.handleStatusCommand(stream);
        }

        // Command: help
        if (userPrompt.includes('help') || userPrompt === '') {
            return this.handleHelpCommand(stream);
        }

        // Default: show help
        return this.handleHelpCommand(stream);
    }

    /**
     * Handle log command
     */
    private async handleLogCommand(
        context: vscode.ChatContext,
        stream: vscode.ChatResponseStream,
        workspaceRoot: string
    ): Promise<vscode.ChatResult> {
        stream.markdown('📝 Logging conversation...\n\n');

        // Extract messages from chat history
        const messages: ChatMessage[] = [];

        for (const turn of context.history) {
            if (turn instanceof vscode.ChatRequestTurn) {
                messages.push({
                    role: 'user',
                    content: turn.prompt
                });
            } else if (turn instanceof vscode.ChatResponseTurn) {
                // Extract text from response
                const responseText = this.extractResponseText(turn);
                messages.push({
                    role: 'assistant',
                    content: responseText
                });
            }
        }

        if (messages.length === 0) {
            stream.markdown('⚠️ No conversation history found.');
            return { metadata: { command: 'log', success: false } };
        }

        try {
            // Check DEIA CLI
            const cliAvailable = await this.logger.isDeiaCliAvailable();
            if (!cliAvailable) {
                stream.markdown('❌ DEIA CLI not found. Install DEIA: `pip install -e /path/to/deia`');
                return { metadata: { command: 'log', success: false, error: 'cli-not-found' } };
            }

            // Log interactively
            const logPath = await this.logger.logInteractive(workspaceRoot, messages);

            if (logPath) {
                stream.markdown(`✅ Conversation logged successfully!\n\n`);
                stream.markdown(`📁 Location: \`${logPath}\``);

                return { metadata: { command: 'log', success: true, logPath } };
            } else {
                stream.markdown('⚠️ Logging cancelled.');
                return { metadata: { command: 'log', success: false, error: 'cancelled' } };
            }

        } catch (error) {
            stream.markdown(`❌ Failed to log conversation: ${error}`);
            return { metadata: { command: 'log', success: false, error: String(error) } };
        }
    }

    /**
     * Handle status command
     */
    private async handleStatusCommand(
        stream: vscode.ChatResponseStream
    ): Promise<vscode.ChatResult> {
        const config = this.detector.getDeiaConfig();

        if (!config) {
            stream.markdown('⚠️ DEIA config not found.');
            return { metadata: { command: 'status' } };
        }

        stream.markdown(`## DEIA Status\n\n`);
        stream.markdown(`**Project:** ${config.project}\n\n`);
        stream.markdown(`**User:** ${config.user}\n\n`);
        stream.markdown(`**Auto-log:** ${config.auto_log ? '✅ ON' : '⏸️ OFF'}\n\n`);
        stream.markdown(`**Version:** ${config.version}\n\n`);

        const sessionsPath = this.detector.getSessionsPath();
        if (sessionsPath) {
            stream.markdown(`**Sessions:** \`${sessionsPath}\``);
        }

        return { metadata: { command: 'status' } };
    }

    /**
     * Handle help command
     */
    private handleHelpCommand(stream: vscode.ChatResponseStream): vscode.ChatResult {
        stream.markdown(`## DEIA - AI Conversation Logger\n\n`);
        stream.markdown(`**Available commands:**\n\n`);
        stream.markdown(`- \`@deia log\` - Log this conversation\n`);
        stream.markdown(`- \`@deia status\` - Show DEIA status\n`);
        stream.markdown(`- \`@deia help\` - Show this help message\n\n`);
        stream.markdown(`**Never lose context.** DEIA logs your AI conversations locally for crash recovery and knowledge sharing.`);

        return { metadata: { command: 'help' } };
    }

    /**
     * Extract text from chat response turn
     */
    private extractResponseText(turn: vscode.ChatResponseTurn): string {
        let text = '';

        // Iterate through response parts
        for (const part of turn.response) {
            if (part instanceof vscode.ChatResponseMarkdownPart) {
                text += part.value.value + '\n';
            }
        }

        return text.trim();
    }

    /**
     * Dispose the chat participant
     */
    public dispose(): void {
        this.participant.dispose();
    }
}
