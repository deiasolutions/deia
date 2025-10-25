import * as vscode from 'vscode';
import { exec, spawn } from 'child_process';
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

            // Execute using spawn to properly pipe stdin
            const result = await this.executeWithStdin(cmd, 'y\n', workspaceRoot);

            // Clean up temp file
            fs.unlinkSync(tempFile);

            // Extract log file path from output
            const match = result.match(/Location:\s+(.+\.md)/);
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
            // Remove emojis and non-ASCII characters to avoid encoding issues
            const cleanContent = msg.content.replace(/[^\x00-\x7F]/g, '');
            transcript += `${speaker}: ${cleanContent}\n\n`;
        }

        return transcript.trim();
    }

    /**
     * Execute command with stdin input
     */
    private executeWithStdin(command: string, input: string, cwd: string): Promise<string> {
        return new Promise((resolve, reject) => {
            const child = spawn('powershell.exe', ['-Command', command], {
                cwd,
                env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
            });

            let stdout = '';
            let stderr = '';

            child.stdout.on('data', (data) => {
                stdout += data.toString();
            });

            child.stderr.on('data', (data) => {
                stderr += data.toString();
            });

            child.on('close', (code) => {
                if (code === 0) {
                    resolve(stdout);
                } else {
                    reject(new Error(`Command failed with code ${code}: ${stderr}`));
                }
            });

            // Write input to stdin
            child.stdin.write(input);
            child.stdin.end();
        });
    }

    /**
     * Build the deia log command
     */
    private buildLogCommand(transcriptFile: string, options: LogOptions): string {
        // Use --from-file to log the transcript
        return `${this.deiaCliPath} log --from-file "${transcriptFile}"`;
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
        // Simply log the conversation using the CLI
        // The CLI will handle interactive prompts
        return this.logConversation(workspaceRoot, {
            context: 'Chat conversation',
            messages
        });
    }
}
