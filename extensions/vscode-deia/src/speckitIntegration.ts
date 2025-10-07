import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * Integration with GitHub SpecKit for spec-driven development
 */
export class SpecKitIntegration {
    private workspaceRoot: string;

    constructor(workspaceRoot: string) {
        this.workspaceRoot = workspaceRoot;
    }

    /**
     * Check if SpecKit is initialized in this project
     */
    public isSpecKitProject(): boolean {
        const specifyDir = path.join(this.workspaceRoot, '.specify');
        return fs.existsSync(specifyDir) && fs.statSync(specifyDir).isDirectory();
    }

    /**
     * Check if specify CLI is available
     */
    public async isSpecifyCliAvailable(): Promise<boolean> {
        try {
            await execAsync('specify check');
            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * Get constitution file path
     */
    public getConstitutionPath(): string | undefined {
        if (!this.isSpecKitProject()) {
            return undefined;
        }

        const constitutionPath = path.join(this.workspaceRoot, '.specify', 'memory', 'constitution.md');
        return fs.existsSync(constitutionPath) ? constitutionPath : undefined;
    }

    /**
     * Get specification directory
     */
    public getSpecsDirectory(): string | undefined {
        if (!this.isSpecKitProject()) {
            return undefined;
        }

        const specsDir = path.join(this.workspaceRoot, 'specs');
        return fs.existsSync(specsDir) ? specsDir : undefined;
    }

    /**
     * Extract specification from DEIA conversation
     *
     * This analyzes a conversation log and extracts:
     * - Requirements mentioned
     * - Technical decisions
     * - Architecture discussions
     */
    public async extractSpecFromConversation(
        conversationPath: string
    ): Promise<SpecExtraction | undefined> {
        if (!fs.existsSync(conversationPath)) {
            return undefined;
        }

        const content = fs.readFileSync(conversationPath, 'utf-8');

        // Parse DEIA log format
        const extraction: SpecExtraction = {
            requirements: [],
            decisions: [],
            architecture: [],
            implementation: []
        };

        // Extract from "Key Decisions" section
        const decisionsMatch = content.match(/## Key Decisions\n\n([\s\S]*?)(?=\n##|$)/);
        if (decisionsMatch) {
            const decisions = decisionsMatch[1]
                .split('\n')
                .filter(line => line.trim().startsWith('-'))
                .map(line => line.trim().substring(2));

            extraction.decisions.push(...decisions);
        }

        // Extract from "What We Worked On" section
        const contextMatch = content.match(/## What We Worked On\n\n([\s\S]*?)(?=\n##|$)/);
        if (contextMatch) {
            extraction.requirements.push(contextMatch[1].trim());
        }

        // Extract from transcript for architecture discussions
        const transcriptMatch = content.match(/## Full Transcript\n\n([\s\S]*?)(?=\n##|$)/);
        if (transcriptMatch) {
            const transcript = transcriptMatch[1];

            // Look for architecture keywords
            const archKeywords = ['architecture', 'design', 'pattern', 'structure', 'system'];
            const lines = transcript.split('\n');

            for (const line of lines) {
                const lowerLine = line.toLowerCase();
                if (archKeywords.some(keyword => lowerLine.includes(keyword))) {
                    extraction.architecture.push(line.trim());
                }
            }
        }

        return extraction;
    }

    /**
     * Create SpecKit specification from DEIA log
     */
    public async createSpecFromLog(
        conversationPath: string,
        specName: string
    ): Promise<string | undefined> {
        const extraction = await this.extractSpecFromConversation(conversationPath);

        if (!extraction) {
            return undefined;
        }

        // Create specification document
        const specContent = this.formatAsSpec(specName, extraction);

        // Save to specs directory
        const specsDir = this.getSpecsDirectory() || path.join(this.workspaceRoot, 'specs');
        if (!fs.existsSync(specsDir)) {
            fs.mkdirSync(specsDir, { recursive: true });
        }

        const specPath = path.join(specsDir, `${specName}.md`);
        fs.writeFileSync(specPath, specContent, 'utf-8');

        return specPath;
    }

    /**
     * Format extraction as SpecKit specification
     */
    private formatAsSpec(name: string, extraction: SpecExtraction): string {
        const timestamp = new Date().toISOString().split('T')[0];

        let spec = `# ${name}\n\n`;
        spec += `**Generated from DEIA conversation log**\n`;
        spec += `**Date:** ${timestamp}\n\n`;

        spec += `---\n\n`;

        // Requirements
        if (extraction.requirements.length > 0) {
            spec += `## Requirements\n\n`;
            for (const req of extraction.requirements) {
                spec += `${req}\n\n`;
            }
        }

        // Technical Decisions
        if (extraction.decisions.length > 0) {
            spec += `## Technical Decisions\n\n`;
            for (const decision of extraction.decisions) {
                spec += `- ${decision}\n`;
            }
            spec += `\n`;
        }

        // Architecture
        if (extraction.architecture.length > 0) {
            spec += `## Architecture Notes\n\n`;
            for (const note of extraction.architecture) {
                spec += `- ${note}\n`;
            }
            spec += `\n`;
        }

        spec += `---\n\n`;
        spec += `*This specification was extracted from a DEIA conversation log and may need refinement.*\n`;

        return spec;
    }

    /**
     * Suggest adding conversation context to SpecKit constitution
     */
    public async suggestConstitutionUpdate(conversationPath: string): Promise<string | undefined> {
        const constitutionPath = this.getConstitutionPath();

        if (!constitutionPath) {
            return undefined;
        }

        const extraction = await this.extractSpecFromConversation(conversationPath);

        if (!extraction || extraction.decisions.length === 0) {
            return undefined;
        }

        // Create suggested addition to constitution
        let suggestion = `\n## Project Principles (from conversation ${new Date().toISOString().split('T')[0]})\n\n`;

        for (const decision of extraction.decisions) {
            suggestion += `- ${decision}\n`;
        }

        return suggestion;
    }
}

export interface SpecExtraction {
    requirements: string[];
    decisions: string[];
    architecture: string[];
    implementation: string[];
}
