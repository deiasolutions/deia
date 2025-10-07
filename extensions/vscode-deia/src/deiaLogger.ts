import * as vscode from 'vscode';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';
import * as path from 'path';

const execAsync = promisify(exec);

export interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
}

export interface LogOptions {
    context: string;
    messages: ChatMessage[];
    decisions?: string[];
    actionItems?: string[];
    filesModified?: string[];
    nextSteps?: string;
}

/**
 * Logs conversations using the DEIA CLI
 */
export class DeiaLogger {
    private deiaCliPath: string;

    constructor() {
        const config = vscode.workspace.getConfiguration('deia');
        this.deiaCliPath = config.get('deiaCliPath', 'deia');
    }

    /**
     * Check if DEIA CLI is available
     */
    public async isDeiaCliAvailable(): Promise<boolean> {
        try {
            await execAsync(`${this.deiaCliPath} --version`);
            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * Log a conversation using DEIA CLI
     */
    public async logConversation(
        workspaceRoot: string,
        options: LogOptions
    ): Promise<string | undefined> {
        // Convert messages to transcript format
        const transcript = this.formatTranscript(options.messages);

        // Create temp file with transcript
        const tempDir = path.join(workspaceRoot, '.deia', 'temp');
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir, { recursive: true });
        }

        const tempFile = path.join(tempDir, `transcript_${Date.now()}.txt`);
        fs.writeFileSync(tempFile, transcript, 'utf-8');

        try {
            // Build command
            const cmd = this.buildLogCommand(tempFile, options);

            // Execute
            const { stdout, stderr } = await execAsync(cmd, {
                cwd: workspaceRoot
            });

            // Clean up temp file
            fs.unlinkSync(tempFile);

            if (stderr) {
                console.error('DEIA CLI stderr:', stderr);
            }

            // Extract log file path from output
            const match = stdout.match(/Logged to: (.+)/);
            return match ? match[1].trim() : undefined;

        } catch (error) {
            // Clean up temp file
            if (fs.existsSync(tempFile)) {
                fs.unlinkSync(tempFile);
            }
            throw error;
        }
    }

    /**
     * Format chat messages as transcript
     */
    private formatTranscript(messages: ChatMessage[]): string {
        let transcript = '';

        for (const msg of messages) {
            const speaker = msg.role === 'user' ? 'User' : 'Assistant';
            transcript += `${speaker}: ${msg.content}\n\n`;
        }

        return transcript.trim();
    }

    /**
     * Build the deia log command
     */
    private buildLogCommand(transcriptFile: string, options: LogOptions): string {
        let cmd = `${this.deiaCliPath} log conversation`;
        cmd += ` --context "${this.escapeQuotes(options.context)}"`;
        cmd += ` --transcript "${transcriptFile}"`;

        if (options.decisions && options.decisions.length > 0) {
            const decisions = options.decisions.join(',');
            cmd += ` --decisions "${this.escapeQuotes(decisions)}"`;
        }

        if (options.actionItems && options.actionItems.length > 0) {
            const items = options.actionItems.join(',');
            cmd += ` --action-items "${this.escapeQuotes(items)}"`;
        }

        if (options.filesModified && options.filesModified.length > 0) {
            const files = options.filesModified.join(',');
            cmd += ` --files "${this.escapeQuotes(files)}"`;
        }

        if (options.nextSteps) {
            cmd += ` --next-steps "${this.escapeQuotes(options.nextSteps)}"`;
        }

        return cmd;
    }

    /**
     * Escape quotes in strings for shell commands
     */
    private escapeQuotes(str: string): string {
        return str.replace(/"/g, '\\"');
    }

    /**
     * Manual logging with user prompts
     */
    public async logInteractive(
        workspaceRoot: string,
        messages: ChatMessage[]
    ): Promise<string | undefined> {
        // Prompt for context
        const context = await vscode.window.showInputBox({
            prompt: 'What were you working on?',
            placeHolder: 'e.g., Implementing user authentication'
        });

        if (!context) {
            return undefined;
        }

        // Prompt for decisions
        const decisionsInput = await vscode.window.showInputBox({
            prompt: 'Key decisions made (comma-separated, or leave blank)',
            placeHolder: 'e.g., Used JWT tokens, Added password hashing'
        });

        const decisions = decisionsInput
            ? decisionsInput.split(',').map(d => d.trim())
            : undefined;

        // Prompt for action items
        const actionItemsInput = await vscode.window.showInputBox({
            prompt: 'Action items (comma-separated, or leave blank)',
            placeHolder: 'e.g., Test auth flow, Add password reset'
        });

        const actionItems = actionItemsInput
            ? actionItemsInput.split(',').map(a => a.trim())
            : undefined;

        // Prompt for next steps
        const nextSteps = await vscode.window.showInputBox({
            prompt: 'Next steps',
            placeHolder: 'e.g., Continue with authorization'
        });

        // Log it
        return this.logConversation(workspaceRoot, {
            context,
            messages,
            decisions,
            actionItems,
            nextSteps: nextSteps || 'Continue from this conversation'
        });
    }
}
