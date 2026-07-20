#!/usr/bin/env npx ts-node
/**
 * web-autopilot: Generic Task Runner
 * Lists and executes generated automation tasks.
 * 
 * Copyright (c) 2026 徐柏雄 (xubx4)
 * 反馈/交流：xubx4@midea.com | 13824820932
 */
import * as fs from 'fs';
import * as path from 'path';
import { program } from 'commander';

const TASKS_DIR = path.join(process.env.HOME || process.env.USERPROFILE || require('os').homedir(), '.openclaw/rpa/tasks');

program
  .name('run-task')
  .description('Run a web-autopilot task')
  .argument('[task-name]', 'Task name')
  .option('--list', 'List all available tasks')
  .option('--info <task>', 'Show task info')
  .option('--params <json>', 'Parameters as JSON')
  .option('--mode <mode>', 'Script mode: ui or api (default: api)', 'api')
  .option('--dry-run', 'Show what would run without executing')
  .allowUnknownOption(true)
  .parse();

const opts = program.opts();

async function main() {
  if (opts.list) { listTasks(); return; }
  const taskName = opts.info || program.args[0];
  if (!taskName) { console.log('Usage: run-task <name> [--params json] | --list'); process.exit(1); }

  const taskDir = findTaskDir(taskName);
  if (!taskDir) { console.error(`❌ Task not found: "${taskName}". Use --list.`); process.exit(1); }

  if (opts.info) { showInfo(taskDir); return; }

  let params: Record<string, any> = {};
  if (opts.params) { params = JSON.parse(opts.params); }
  else { const remaining = process.argv.slice(3); for (let i = 0; i < remaining.length; i++) { if (remaining[i].startsWith('--')) { const k = remaining[i].slice(2); const v = remaining[i+1] && !remaining[i+1].startsWith('--') ? remaining[++i] : 'true'; params[k] = v; } } }

  const meta = JSON.parse(fs.readFileSync(path.join(taskDir, 'task-meta.json'), 'utf8'));
  for (const [n, d] of Object.entries<any>(meta.params || {})) { if (d.required && !(n in params) && d.default !== undefined) params[n] = d.default; }

  if (opts.dryRun) { console.log(`🔍 Dry run: ${meta.name}\n   Mode: ${opts.mode}\n   Params: ${JSON.stringify(params, null, 2)}`); return; }

  // Select script based on mode (default: api)
  const mode = opts.mode || 'api';
  const scriptName = mode === 'ui' ? 'run-ui.ts' : 'run-api.ts';
  const tsPath = path.join(taskDir, scriptName);
  
  // Fallback: if selected script doesn't exist, try the other
  let finalPath = tsPath;
  if (!fs.existsSync(tsPath)) {
    const fallback = mode === 'ui' ? 'run-api.ts' : 'run-ui.ts';
    const fallbackPath = path.join(taskDir, fallback);
    if (fs.existsSync(fallbackPath)) {
      console.log(`⚠️  ${scriptName} not found, falling back to ${fallback}`);
      finalPath = fallbackPath;
    } else if (fs.existsSync(path.join(taskDir, 'run.ts'))) {
      // Legacy fallback for old tasks
      console.log(`⚠️  Dual scripts not found, falling back to legacy run.ts`);
      finalPath = path.join(taskDir, 'run.ts');
    } else {
      console.error(`❌ No executable script found in ${taskDir}`);
      process.exit(1);
    }
  }
  
  // v8.4.1: 改用 execFileSync 避免 shell 注入风险
  if (fs.existsSync(finalPath)) { const { execFileSync } = require('child_process'); execFileSync('npx', ['ts-node', finalPath, '--params', JSON.stringify(params)], { stdio: 'inherit' }); }
}

function findTaskDir(name: string): string | null {
  if (!fs.existsSync(TASKS_DIR)) return null;
  for (const dir of fs.readdirSync(TASKS_DIR)) {
    const mp = path.join(TASKS_DIR, dir, 'task-meta.json');
    if (!fs.existsSync(mp)) continue;
    try { const m = JSON.parse(fs.readFileSync(mp, 'utf8')); if (m.name === name || dir === name || dir.toLowerCase() === name.toLowerCase()) return path.join(TASKS_DIR, dir); } catch {}
  }
  return null;
}

function listTasks() {
  if (!fs.existsSync(TASKS_DIR)) { console.log('No tasks found.'); return; }
  const dirs = fs.readdirSync(TASKS_DIR).filter(d => fs.existsSync(path.join(TASKS_DIR, d, 'task-meta.json')));
  if (!dirs.length) { console.log('No tasks found.'); return; }
  console.log(`\n📋 Available Tasks (${dirs.length})\n`);
  for (const dir of dirs) {
    try { const m = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, dir, 'task-meta.json'), 'utf8')); console.log(`  📌 ${m.name}\n     ${m.description}\n     App: ${m.appDomain}  |  Params: ${Object.keys(m.params || {}).join(', ') || '(none)'}\n`); } catch {}
  }
}

function showInfo(taskDir: string) {
  const m = JSON.parse(fs.readFileSync(path.join(taskDir, 'task-meta.json'), 'utf8'));
  console.log(`\n📌 ${m.name}\n   ${m.description}\n   App: ${m.appDomain}\n   SSO: ${m.ssoUrl || 'N/A'}`);
  for (const [n, d] of Object.entries<any>(m.params || {})) { console.log(`   --${n.padEnd(20)} ${d.type.padEnd(8)} ${d.required ? '[required]' : '[optional]'}  ${d.description}`); }
}

main().catch(e => { console.error('Fatal:', e.message); process.exit(1); });
