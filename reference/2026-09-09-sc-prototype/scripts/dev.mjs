import { spawn } from 'node:child_process';
const children = ['dev:backend', 'dev:frontend'].map(script => spawn('npm', ['run', script], { stdio: 'inherit', detached: true }));
let closing = false;
function close(code = 0) {
  if (closing) return;
  closing = true;
  for (const child of children) { try { process.kill(-child.pid, 'SIGTERM'); } catch {} }
  process.exitCode = code;
}
children.forEach(child => { child.on('exit', code => close(code || 0)); child.on('error', () => close(1)); });
process.on('SIGINT', () => close());
process.on('SIGTERM', () => close());
