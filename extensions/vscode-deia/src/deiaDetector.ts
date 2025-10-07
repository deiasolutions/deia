import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

export interface DeiaConfig {
    project: string;
    user: string;
    auto_log: boolean;
    version: string;
}

/**
 * Detects DEIA-enabled workspaces and reads configuration
 */
export class DeiaDetector {
    /**
     * Check if any workspace folder has a .deia directory
     */
    public hasDeiaInWorkspace(): boolean {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            return false;
        }

        return workspaceFolders.some(folder => {
            const deiaPath = path.join(folder.uri.fsPath, '.deia');
            return fs.existsSync(deiaPath) && fs.statSync(deiaPath).isDirectory();
        });
    }

    /**
     * Get the first DEIA directory found in workspace
     */
    public getDeiaPath(): string | undefined {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            return undefined;
        }

        for (const folder of workspaceFolders) {
            const deiaPath = path.join(folder.uri.fsPath, '.deia');
            if (fs.existsSync(deiaPath) && fs.statSync(deiaPath).isDirectory()) {
                return deiaPath;
            }
        }

        return undefined;
    }

    /**
     * Get the workspace root containing DEIA
     */
    public getDeiaWorkspaceRoot(): string | undefined {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            return undefined;
        }

        for (const folder of workspaceFolders) {
            const deiaPath = path.join(folder.uri.fsPath, '.deia');
            if (fs.existsSync(deiaPath) && fs.statSync(deiaPath).isDirectory()) {
                return folder.uri.fsPath;
            }
        }

        return undefined;
    }

    /**
     * Read DEIA config.json
     */
    public getDeiaConfig(): DeiaConfig | undefined {
        const deiaPath = this.getDeiaPath();
        if (!deiaPath) {
            return undefined;
        }

        const configPath = path.join(deiaPath, 'config.json');
        if (!fs.existsSync(configPath)) {
            return undefined;
        }

        try {
            const content = fs.readFileSync(configPath, 'utf-8');
            return JSON.parse(content) as DeiaConfig;
        } catch (error) {
            console.error('Failed to read DEIA config:', error);
            return undefined;
        }
    }

    /**
     * Get sessions directory path
     */
    public getSessionsPath(): string | undefined {
        const deiaPath = this.getDeiaPath();
        if (!deiaPath) {
            return undefined;
        }

        return path.join(deiaPath, 'sessions');
    }

    /**
     * Get project resume path
     */
    public getProjectResumePath(): string | undefined {
        const workspaceRoot = this.getDeiaWorkspaceRoot();
        if (!workspaceRoot) {
            return undefined;
        }

        return path.join(workspaceRoot, 'project_resume.md');
    }
}
