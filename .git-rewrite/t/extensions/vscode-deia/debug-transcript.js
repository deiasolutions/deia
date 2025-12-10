// Debug the transcript formatting

const testMessages = [
    { role: 'user', content: 'Hello! Can you help me with authentication?' },
    { role: 'assistant', content: '✓ Sure! I can help with that. Let me create a test... 🚀' },
    { role: 'user', content: 'Great, thanks!' }
];

function formatTranscript(messages) {
    let transcript = '';

    for (const msg of messages) {
        const speaker = msg.role === 'user' ? 'User' : 'Assistant';
        const cleanContent = msg.content.replace(/[^\x00-\x7F]/g, '');
        transcript += `${speaker}: ${cleanContent}\n\n`;
    }

    return transcript.trim();
}

const result = formatTranscript(testMessages);
console.log('Formatted transcript:');
console.log(result);
console.log('\nContains "User: Hello"?', result.includes('User: Hello'));
console.log('Contains "Assistant: Sure"?', result.includes('Assistant: Sure'));
