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

        // Extract from "Requirements" section (any level heading)
        const requirementsMatch = content.match(/###?\s+Requirements?\s*\n([\s\S]*?)(?=\n###?\s+|$)/i);
        if (requirementsMatch) {
            const requirements = requirementsMatch[1]
                .split('\n')
                .filter(line => line.trim().startsWith('-'))
                .map(line => line.trim().substring(2).trim());

            extraction.requirements.push(...requirements);
        }

        // Extract from "Key Decisions" or "Architecture Decisions" sections
        const decisionsMatch = content.match(/###?\s+(Key Decisions|Architecture Decisions?)\s*\n([\s\S]*?)(?=\n###?\s+|$)/i);
        if (decisionsMatch) {
            const decisions = decisionsMatch[2]
                .split('\n')
                .filter(line => line.trim().startsWith('-'))
                .map(line => line.trim().substring(2).trim());

            extraction.decisions.push(...decisions);
        }

        // Extract from "What We Worked On" section
        const contextMatch = content.match(/##\s+What We Worked On\s*\n([\s\S]*?)(?=\n##|$)/i);
        if (contextMatch) {
            extraction.requirements.push(contextMatch[1].trim());
        }

        // Extract from "Implementation Plan" section
        const implMatch = content.match(/###?\s+Implementation (Plan|Steps?)\s*\n([\s\S]*?)(?=\n###?\s+|$)/i);
        if (implMatch) {
            const steps = implMatch[2]
                .split('\n')
                .filter(line => /^\d+\./.test(line.trim()) || line.trim().startsWith('-'))
                .map(line => line.trim().replace(/^\d+\.\s*/, '').replace(/^-\s*/, ''))
                .filter(step => step.length > 0 && !step.match(/^-+$/)); // Remove empty and separator lines

            extraction.implementation.push(...steps);
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
                spec += `- ${req}\n`;
            }
            spec += `\n`;
        }

        // Technical Decisions
        if (extraction.decisions.length > 0) {
            spec += `## Technical Decisions\n\n`;
            for (const decision of extraction.decisions) {
                spec += `- ${decision}\n`;
            }
            spec += `\n`;
        }

        // Architecture (only if not already in decisions)
        const uniqueArchitecture = extraction.architecture.filter(
            arch => !extraction.decisions.includes(arch)
        );

        if (uniqueArchitecture.length > 0) {
            spec += `## Architecture Notes\n\n`;
            for (const note of uniqueArchitecture) {
                spec += `- ${note}\n`;
            }
            spec += `\n`;
        }

        // Implementation
        if (extraction.implementation.length > 0) {
            spec += `## Implementation Plan\n\n`;
            let stepNum = 1;
            for (const step of extraction.implementation) {
                spec += `${stepNum}. ${step}\n`;
                stepNum++;
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
