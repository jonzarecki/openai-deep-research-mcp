#!/usr/bin/env node
const { spawn } = require('child_process');

const child = spawn('deep-research-mcp', { stdio: 'inherit' });
child.on('close', code => process.exit(code));
