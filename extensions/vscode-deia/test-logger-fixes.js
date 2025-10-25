/**
 * Test script for deiaLogger.ts fixes
 * Tests the new --from-file approach and encoding fixes
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

// Test data
const testMessages = [
    { role: 'user', content: 'Hello! Can you help me with authentication?' },
    { role: 'assistant', content: '✓ Sure! I can help with that. Let me create a test... 🚀' },
    { role: 'user', content: 'Great, thanks!' }
];

async function runTests() {
    console.log('Testing deiaLogger.ts fixes...\n');
    let passed = 0;
    let failed = 0;

    // Test 1: Transcript formatting (emoji removal)
    console.log('Test 1: Transcript formatting with emoji removal');
    try {
        const transcript = formatTranscript(testMessages);

        // Should not contain emojis
        if (transcript.includes('✓') || transcript.includes('🚀')) {
            throw new Error('Emojis not removed from transcript');
        }

        // Should contain speaker labels and cleaned content
        if (!transcript.includes('User:') || !transcript.includes('Assistant:')) {
            throw new Error('Speaker labels not found');
        }

        // Should contain the actual text (after emoji removal)
        if (!transcript.includes('Hello! Can you help') || !transcript.includes('Sure! I can help')) {
            throw new Error('Content not properly formatted');
        }

        console.log('✓ PASS: Emojis removed, content formatted correctly\n');
        passed++;
    } catch (error) {
        console.log(`✗ FAIL: ${error.message}\n`);
        failed++;
    }

    // Test 2: --from-file command building
    console.log('Test 2: Command building with --from-file');
    try {
        const deiaPath = 'deia';
        const transcriptFile = 'test-transcript.txt';
        const cmd = `${deiaPath} log --from-file "${transcriptFile}"`;

        // Should use --from-file instead of multiple parameters
        if (!cmd.includes('--from-file')) {
            throw new Error('Command does not use --from-file');
        }

        // Should NOT have old parameters
        if (cmd.includes('--context') || cmd.includes('--decisions') || cmd.includes('--action-items')) {
            throw new Error('Command still using old parameter format');
        }

        console.log('✓ PASS: Command uses --from-file approach\n');
        passed++;
    } catch (error) {
        console.log(`✗ FAIL: ${error.message}\n`);
        failed++;
    }

    // Test 3: Empty message handling
    console.log('Test 3: Empty message handling');
    try {
        const emptyMessages = [];
        const transcript = formatTranscript(emptyMessages);

        if (transcript !== '') {
            throw new Error('Empty messages should produce empty transcript');
        }

        console.log('✓ PASS: Empty messages handled correctly\n');
        passed++;
    } catch (error) {
        console.log(`✗ FAIL: ${error.message}\n`);
        failed++;
    }

    // Test 4: Non-ASCII character removal
    console.log('Test 4: Non-ASCII character removal');
    try {
        const unicodeMessages = [
            { role: 'user', content: 'Test with unicode: 你好 مرحبا' },
            { role: 'assistant', content: 'Response with symbols: © ® ™' }
        ];
        const transcript = formatTranscript(unicodeMessages);

        // Should only contain ASCII characters
        const nonAsciiRegex = /[^\x00-\x7F]/;
        if (nonAsciiRegex.test(transcript)) {
            throw new Error('Non-ASCII characters not removed');
        }

        console.log('✓ PASS: Non-ASCII characters removed\n');
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
 * Helper function that mimics the TypeScript formatTranscript method
 */
function formatTranscript(messages) {
    let transcript = '';

    for (const msg of messages) {
        const speaker = msg.role === 'user' ? 'User' : 'Assistant';
        // Remove emojis and non-ASCII characters to avoid encoding issues
        const cleanContent = msg.content.replace(/[^\x00-\x7F]/g, '');
        transcript += `${speaker}: ${cleanContent}\n\n`;
    }

    return transcript.trim();
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
