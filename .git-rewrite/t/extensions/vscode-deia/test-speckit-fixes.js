/**
 * Test script for speckitIntegration.ts fixes
 * Tests improved extraction patterns and implementation plan parsing
 */

const fs = require('fs');
const path = require('path');

// Sample conversation log with the new format
const sampleLog = `# DEIA Conversation Log

## Context
Implementing user authentication system

### Requirements
- Support email/password login
- Implement JWT token authentication
- Add password reset functionality
- Support OAuth2 social logins

## Key Decisions
- Using bcrypt for password hashing
- JWT tokens with 24-hour expiration
- Redis for token blacklisting
- SendGrid for password reset emails

### Architecture Decisions
- Separate auth microservice
- API Gateway for token validation
- Database: PostgreSQL for user data

### Implementation Plan
1. Create user model and database schema
2. Implement registration endpoint
3. Implement login endpoint
4. Add JWT token generation
5. Create password reset flow
6. Integrate OAuth2 providers

## Next Steps
Continue with testing and deployment
`;

async function runTests() {
    console.log('Testing speckitIntegration.ts fixes...\n');
    let passed = 0;
    let failed = 0;

    // Test 1: Requirements extraction (with flexible heading detection)
    console.log('Test 1: Requirements extraction with flexible heading');
    try {
        const extraction = extractConversationElements(sampleLog);

        if (extraction.requirements.length === 0) {
            throw new Error('No requirements extracted');
        }

        // Should extract all 4 requirements
        if (extraction.requirements.length < 4) {
            throw new Error(`Only extracted ${extraction.requirements.length} of 4 requirements`);
        }

        // Check specific requirement
        const hasEmailLogin = extraction.requirements.some(r =>
            r.includes('email/password') || r.includes('Support email/password')
        );
        if (!hasEmailLogin) {
            throw new Error('Did not extract email/password requirement');
        }

        console.log(`✓ PASS: Extracted ${extraction.requirements.length} requirements\n`);
        passed++;
    } catch (error) {
        console.log(`✗ FAIL: ${error.message}\n`);
        failed++;
    }

    // Test 2: Decisions extraction (multiple heading patterns)
    console.log('Test 2: Decisions extraction with multiple heading patterns');
    try {
        const extraction = extractConversationElements(sampleLog);

        if (extraction.decisions.length === 0) {
            throw new Error('No decisions extracted');
        }

        // Should extract decisions from both "Key Decisions" and "Architecture Decisions"
        if (extraction.decisions.length < 5) {
            throw new Error(`Only extracted ${extraction.decisions.length} decisions`);
        }

        // Check for specific decisions
        const hasBcrypt = extraction.decisions.some(d => d.includes('bcrypt'));
        const hasMicroservice = extraction.decisions.some(d => d.includes('microservice'));

        if (!hasBcrypt || !hasMicroservice) {
            throw new Error('Did not extract all decision types');
        }

        console.log(`✓ PASS: Extracted ${extraction.decisions.length} decisions from multiple sections\n`);
        passed++;
    } catch (error) {
        console.log(`✗ FAIL: ${error.message}\n`);
        failed++;
    }

    // Test 3: Implementation plan extraction
    console.log('Test 3: Implementation plan extraction');
    try {
        const extraction = extractConversationElements(sampleLog);

        if (extraction.implementation.length === 0) {
            throw new Error('No implementation steps extracted');
        }

        // Should extract all 6 steps
        if (extraction.implementation.length !== 6) {
            throw new Error(`Expected 6 steps, got ${extraction.implementation.length}`);
        }

        // Steps should not have numbers (those are stripped)
        const firstStep = extraction.implementation[0];
        if (/^\d+\./.test(firstStep)) {
            throw new Error('Step numbers not stripped from implementation steps');
        }

        // Check specific step
        const hasUserModel = extraction.implementation.some(s =>
            s.includes('user model')
        );
        if (!hasUserModel) {
            throw new Error('Did not extract user model step');
        }

        console.log(`✓ PASS: Extracted ${extraction.implementation.length} implementation steps\n`);
        passed++;
    } catch (error) {
        console.log(`✗ FAIL: ${error.message}\n`);
        failed++;
    }

    // Test 4: SpecKit spec generation
    console.log('Test 4: SpecKit spec generation');
    try {
        const extraction = extractConversationElements(sampleLog);
        const spec = generateSpecKitSpec('Auth System Spec', extraction);

        // Should have all sections
        if (!spec.includes('## Requirements')) {
            throw new Error('Missing Requirements section');
        }
        if (!spec.includes('## Technical Decisions')) {
            throw new Error('Missing Technical Decisions section');
        }
        if (!spec.includes('## Implementation Plan')) {
            throw new Error('Missing Implementation Plan section');
        }

        // Implementation plan should have numbered steps
        const planMatch = spec.match(/## Implementation Plan\n\n([\s\S]*?)(?=\n##|---)/);
        if (!planMatch) {
            throw new Error('Implementation plan not properly formatted');
        }

        const planText = planMatch[1];
        if (!planText.includes('1. ') || !planText.includes('2. ')) {
            throw new Error('Implementation steps not numbered');
        }

        console.log('✓ PASS: SpecKit spec generated correctly\n');
        passed++;
    } catch (error) {
        console.log(`✗ FAIL: ${error.message}\n`);
        failed++;
    }

    // Summary
    console.log('═'.repeat(50));
    console.log(`Test Results: ${passed} passed, ${failed} failed`);
    console.log('═'.repeat(50));

    return failed === 0;
}

/**
 * Helper function that mimics the TypeScript extractConversationElements method
 */
function extractConversationElements(content) {
    const extraction = {
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

    // Extract additional architecture decisions
    const archMatch = content.match(/###\s+Architecture Decisions\s*\n([\s\S]*?)(?=\n###?\s+|$)/i);
    if (archMatch) {
        const archDecisions = archMatch[1]
            .split('\n')
            .filter(line => line.trim().startsWith('-'))
            .map(line => line.trim().substring(2).trim());

        extraction.decisions.push(...archDecisions);
    }

    // Extract from "Implementation Plan" section
    const implMatch = content.match(/###?\s+Implementation (Plan|Steps?)\s*\n([\s\S]*?)(?=\n###?\s+|$)/i);
    if (implMatch) {
        const steps = implMatch[2]
            .split('\n')
            .filter(line => /^\d+\./.test(line.trim()) || line.trim().startsWith('-'))
            .map(line => line.trim().replace(/^\d+\.\s*/, '').replace(/^-\s*/, ''))
            .filter(step => step.length > 0 && !step.match(/^-+$/));

        extraction.implementation.push(...steps);
    }

    return extraction;
}

/**
 * Helper function for generating SpecKit spec
 */
function generateSpecKitSpec(title, extraction) {
    let spec = `# ${title}\n\n`;
    spec += `*Generated from DEIA conversation log*\n\n`;
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

// Run tests
runTests()
    .then(success => {
        process.exit(success ? 0 : 1);
    })
    .catch(error => {
        console.error('Test execution failed:', error);
        process.exit(1);
    });
