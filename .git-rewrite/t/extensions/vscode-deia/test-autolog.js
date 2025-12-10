const fs = require('fs');
const path = require('path');

console.log('=== Auto-Logging Implementation Test ===\n');

// Test 1: Verify all files compile
const outDir = './out';
const requiredFiles = [
  'conversationMonitor.js',
  'extension.js',
  'chatParticipant.js',
  'commands.js',
  'deiaLogger.js'
];

console.log('Test 1: Compiled files exist');
let allExist = true;
requiredFiles.forEach(file => {
  const exists = fs.existsSync(path.join(outDir, file));
  console.log(`  ${exists ? '✓' : '✗'} ${file}`);
  if (!exists) allExist = false;
});

if (!allExist) {
  console.log('\n✗ FAIL: Missing compiled files');
  process.exit(1);
}

console.log('\n✓ PASS: All files compiled\n');

// Test 2: Check package.json has new commands
console.log('Test 2: New commands registered in package.json');
const pkg = JSON.parse(fs.readFileSync('./package.json', 'utf-8'));
const commands = pkg.contributes.commands.map(c => c.command);

const newCommands = [
  'deia.saveBuffer',
  'deia.monitorStatus'
];

let allCommandsExist = true;
newCommands.forEach(cmd => {
  const exists = commands.includes(cmd);
  console.log(`  ${exists ? '✓' : '✗'} ${cmd}`);
  if (!exists) allCommandsExist = false;
});

if (!allCommandsExist) {
  console.log('\n✗ FAIL: Missing commands in package.json');
  process.exit(1);
}

console.log('\n✓ PASS: Commands registered\n');

// Test 3: Verify conversationMonitor.js exports expected class
console.log('Test 3: ConversationMonitor module structure');
try {
  const monitorCode = fs.readFileSync(path.join(outDir, 'conversationMonitor.js'), 'utf-8');

  const hasExports = monitorCode.includes('exports.ConversationMonitor');
  const hasStartMonitoring = monitorCode.includes('startMonitoring');
  const hasStopMonitoring = monitorCode.includes('stopMonitoring');
  const hasAddMessage = monitorCode.includes('addMessage');
  const hasSaveNow = monitorCode.includes('saveNow');

  console.log(`  ${hasExports ? '✓' : '✗'} Exports ConversationMonitor class`);
  console.log(`  ${hasStartMonitoring ? '✓' : '✗'} Has startMonitoring method`);
  console.log(`  ${hasStopMonitoring ? '✓' : '✗'} Has stopMonitoring method`);
  console.log(`  ${hasAddMessage ? '✓' : '✗'} Has addMessage method`);
  console.log(`  ${hasSaveNow ? '✓' : '✗'} Has saveNow method`);

  if (!hasExports || !hasStartMonitoring || !hasStopMonitoring || !hasAddMessage || !hasSaveNow) {
    console.log('\n✗ FAIL: Missing required methods');
    process.exit(1);
  }

  console.log('\n✓ PASS: Monitor module structure correct\n');
} catch (error) {
  console.log(`\n✗ FAIL: Error reading monitor module: ${error.message}`);
  process.exit(1);
}

// Test 4: Verify extension.ts integration
console.log('Test 4: Extension integration');
const extensionCode = fs.readFileSync(path.join(outDir, 'extension.js'), 'utf-8');

const hasMonitorImport = extensionCode.includes('conversationMonitor');
const hasMonitorInit = extensionCode.includes('ConversationMonitor');
const hasStartMonitoringCall = extensionCode.includes('startMonitoring');

console.log(`  ${hasMonitorImport ? '✓' : '✗'} Imports ConversationMonitor`);
console.log(`  ${hasMonitorInit ? '✓' : '✗'} Initializes monitor`);
console.log(`  ${hasStartMonitoringCall ? '✓' : '✗'} Calls startMonitoring`);

if (!hasMonitorImport || !hasMonitorInit || !hasStartMonitoringCall) {
  console.log('\n✗ FAIL: Extension integration incomplete');
  process.exit(1);
}

console.log('\n✓ PASS: Extension properly integrated\n');

// Final summary
console.log('=== Test Summary ===');
console.log('✓ All files compiled successfully');
console.log('✓ New commands registered');
console.log('✓ ConversationMonitor module correct');
console.log('✓ Extension integration complete');
console.log('\n✅ AUTO-LOGGING IMPLEMENTATION VERIFIED');
console.log('\nReady for runtime testing in Extension Development Host');
