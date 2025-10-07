import * as vscode from 'vscode';

/**
 * Status bar item showing DEIA status
 */
export class DeiaStatusBar implements vscode.Disposable {
    private statusBarItem: vscode.StatusBarItem;
    private autoLog: boolean;

    constructor(autoLog: boolean) {
        this.autoLog = autoLog;

        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );

        this.statusBarItem.command = 'deia.checkStatus';
        this.updateDisplay();
        this.statusBarItem.show();
    }

    /**
     * Update the status display
     */
    public updateDisplay(): void {
        if (this.autoLog) {
            this.statusBarItem.text = '$(record) DEIA: Auto-log ON';
            this.statusBarItem.tooltip = 'DEIA auto-logging is enabled. Click for status.';
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        } else {
            this.statusBarItem.text = '$(save) DEIA: Manual';
            this.statusBarItem.tooltip = 'DEIA manual logging. Click for status.';
            this.statusBarItem.backgroundColor = undefined;
        }
    }

    /**
     * Set auto-log status
     */
    public setAutoLog(enabled: boolean): void {
        this.autoLog = enabled;
        this.updateDisplay();
    }

    /**
     * Dispose the status bar item
     */
    public dispose(): void {
        this.statusBarItem.dispose();
    }
}
