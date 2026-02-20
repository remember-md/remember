#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { getBrainRoot, loadConfig } = require('./config');

const BRAIN_ROOT = getBrainRoot();
const PROCESSED_FILE = path.join(BRAIN_ROOT, '.processed_sessions');
const CLAUDE_PROJECTS_DIR = path.join(os.homedir(), '.claude', 'projects');
const MAX_ASSISTANT_TEXT_LEN = loadConfig().extract?.max_assistant_text_len || 500;
const MIN_SESSION_SIZE = loadConfig().extract?.min_session_size || 500;

// --- Session tracking ---

function getProcessedSessions() {
  try {
    return new Set(fs.readFileSync(PROCESSED_FILE, 'utf-8').trim().split('\n').filter(Boolean));
  } catch {
    return new Set();
  }
}

function markSessionProcessed(sessionId) {
  fs.mkdirSync(path.dirname(PROCESSED_FILE), { recursive: true });
  fs.appendFileSync(PROCESSED_FILE, sessionId + '\n', 'utf-8');
}

// --- Transcript discovery ---

function findAllTranscripts() {
  const transcripts = [];
  if (!fs.existsSync(CLAUDE_PROJECTS_DIR)) return transcripts;
  for (const projDir of fs.readdirSync(CLAUDE_PROJECTS_DIR)) {
    const projPath = path.join(CLAUDE_PROJECTS_DIR, projDir);
    let stat;
    try { stat = fs.statSync(projPath); } catch { continue; }
    if (!stat.isDirectory()) continue;
    for (const file of fs.readdirSync(projPath)) {
      if (file.endsWith('.jsonl')) {
        transcripts.push(path.join(projPath, file));
      }
    }
  }
  return transcripts;
}

function getSessionId(filePath) {
  return path.basename(filePath, '.jsonl');
}

function getProjectName(filePath) {
  const parent = path.basename(path.dirname(filePath));
  const parts = parent.split('-');
  const idx = parts.indexOf('projects');
  if (idx !== -1) {
    const projectParts = parts.slice(idx + 1).filter(Boolean);
    if (projectParts.length) return projectParts.join('/');
  }
  const meaningful = parts.filter(Boolean);
  return meaningful.length >= 2 ? meaningful.slice(-2).join('/') : parent;
}

// --- Content extraction ---

const NOISE_PREFIXES = [
  '<local-command-',
  '<command-name>',
  '<system-',
  '<user-prompt-submit-hook>',
];

function isNoiseContent(content) {
  if (typeof content !== 'string') return false;
  const trimmed = content.trim();
  return NOISE_PREFIXES.some(p => trimmed.startsWith(p));
}

function extractUserText(message) {
  const content = message.content;
  if (typeof content === 'string') {
    if (isNoiseContent(content)) return null;
    const text = content.trim();
    return text || null;
  }
  if (Array.isArray(content)) {
    const texts = [];
    for (const block of content) {
      if (typeof block === 'object' && block?.type === 'text') {
        const t = block.text?.trim();
        if (t && !isNoiseContent(t)) texts.push(t);
      } else if (typeof block === 'string') {
        if (!isNoiseContent(block)) texts.push(block.trim());
      }
    }
    return texts.length ? texts.join('\n') : null;
  }
  return null;
}

function extractAssistantText(message) {
  const content = message.content;
  if (typeof content === 'string') {
    return content.length <= MAX_ASSISTANT_TEXT_LEN ? content.trim() || null : null;
  }
  if (!Array.isArray(content)) return null;

  const texts = [];
  let hasToolUse = false;
  for (const block of content) {
    if (typeof block !== 'object' || !block) continue;
    if (block.type === 'tool_use') hasToolUse = true;
    else if (block.type === 'text') {
      const t = block.text?.trim();
      if (t) texts.push(t);
    }
  }
  if (!texts.length) return null;
  const combined = texts.join('\n');
  if (combined.length > MAX_ASSISTANT_TEXT_LEN) return null;
  if (hasToolUse && combined.length < 20) return null;
  return combined;
}

// --- Timestamp helpers ---

function parseTimestamp(tsStr) {
  if (!tsStr) return null;
  try {
    const d = new Date(tsStr);
    return isNaN(d.getTime()) ? null : d;
  } catch {
    return null;
  }
}

function formatTimestamp(tsStr, includeDate = false) {
  const dt = parseTimestamp(tsStr);
  if (!dt) return '';
  if (includeDate) {
    return dt.toISOString().slice(0, 16).replace('T', ' ');
  }
  return dt.toISOString().slice(11, 16);
}

function formatDateOnly(tsStr) {
  const dt = parseTimestamp(tsStr);
  return dt ? dt.toISOString().slice(0, 10) : '';
}

// --- Session extraction ---

function extractSession(filePath) {
  const sessionId = getSessionId(filePath);
  const project = getProjectName(filePath);
  const messages = [];
  let sessionCwd = null;
  let firstTs = null;
  let lastTs = null;

  const text = fs.readFileSync(filePath, 'utf-8');
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    let entry;
    try { entry = JSON.parse(line); } catch { continue; }

    const ts = entry.timestamp || '';
    if (!firstTs && ts) firstTs = ts;
    if (ts) lastTs = ts;
    if (!sessionCwd && entry.cwd) sessionCwd = entry.cwd;

    if (entry.type === 'user') {
      if (entry.isMeta) continue;
      const msg = entry.message || {};
      const text = extractUserText(msg);
      if (text) {
        messages.push({ role: 'user', text, time: formatTimestamp(ts), timestamp: ts });
      }
    } else if (entry.type === 'assistant') {
      const msg = entry.message || {};
      const text = extractAssistantText(msg);
      if (text) {
        messages.push({ role: 'assistant', text, time: formatTimestamp(ts), timestamp: ts });
      }
    }
  }

  let spansMultipleDays = false;
  if (firstTs && lastTs) {
    const firstDate = formatDateOnly(firstTs);
    const lastDate = formatDateOnly(lastTs);
    if (firstDate && lastDate && firstDate !== lastDate) spansMultipleDays = true;
  }

  return {
    session_id: sessionId,
    project,
    cwd: sessionCwd,
    first_ts: firstTs,
    last_ts: lastTs,
    spans_multiple_days: spansMultipleDays,
    session_date: firstTs,
    messages,
  };
}

// --- Formatting ---

function formatSessionMarkdown(session) {
  const lines = [];
  const dateStr = formatDateOnly(session.first_ts);
  const endDateStr = formatDateOnly(session.last_ts);
  const spans = session.spans_multiple_days;

  lines.push(`# Session: ${session.project}`);
  if (dateStr) {
    lines.push(spans && endDateStr && dateStr !== endDateStr
      ? `**Date:** ${dateStr} to ${endDateStr}`
      : `**Date:** ${dateStr}`);
  }
  lines.push(`**Session date (use for journal/tasks):** ${dateStr}`);
  if (session.cwd) lines.push(`**Working dir:** \`${session.cwd}\``);
  lines.push(`**Session ID:** \`${session.session_id}\``);
  lines.push('');

  if (!session.messages.length) {
    lines.push('*(empty session)*');
    return lines.join('\n');
  }

  let currentDay = null;
  for (const msg of session.messages) {
    if (spans && msg.timestamp) {
      const msgDay = formatDateOnly(msg.timestamp);
      if (msgDay && msgDay !== currentDay) {
        currentDay = msgDay;
        lines.push(`### ${msgDay}`);
        lines.push('');
      }
    }
    const timePrefix = msg.time ? `[${msg.time}] ` : '';
    if (msg.role === 'user') {
      lines.push(`**${timePrefix}User:** ${msg.text}`);
    } else {
      lines.push(`*${timePrefix}Claude: ${msg.text}*`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

// --- CLI commands ---

function cmdExtract(filePath) {
  if (!fs.existsSync(filePath)) {
    process.stderr.write(`Error: file not found: ${filePath}\n`);
    process.exit(1);
  }
  const session = extractSession(filePath);
  console.log(formatSessionMarkdown(session));
}

function cmdListUnprocessed(projectFilter) {
  const processed = getProcessedSessions();
  const transcripts = findAllTranscripts();

  const unprocessed = [];
  for (const t of transcripts) {
    const sid = getSessionId(t);
    if (processed.has(sid)) continue;
    const project = getProjectName(t);
    if (projectFilter && !project.toLowerCase().includes(projectFilter.toLowerCase())) continue;
    let size;
    try { size = fs.statSync(t).size; } catch { continue; }
    if (size < MIN_SESSION_SIZE) continue;
    unprocessed.push({ path: t, project, size });
  }

  unprocessed.sort((a, b) => {
    try {
      return fs.statSync(a.path).mtimeMs - fs.statSync(b.path).mtimeMs;
    } catch { return 0; }
  });

  if (!unprocessed.length) {
    console.log('No unprocessed sessions found.');
    return;
  }

  console.log(`Found ${unprocessed.length} unprocessed session(s):\n`);
  for (const u of unprocessed) {
    const sid = getSessionId(u.path);
    let mtime;
    try {
      const mt = fs.statSync(u.path).mtime;
      mtime = mt.toISOString().slice(0, 16).replace('T', ' ');
    } catch {
      mtime = 'unknown';
    }
    const sizeKb = (u.size / 1024).toFixed(0);
    console.log(`  ${sid}`);
    console.log(`    Project: ${u.project}`);
    console.log(`    Modified: ${mtime}`);
    console.log(`    Size: ${sizeKb}KB`);
    console.log(`    Path: ${u.path}`);
    console.log();
  }
}

function cmdMarkProcessed(sessionId) {
  markSessionProcessed(sessionId);
  console.log(`Marked as processed: ${sessionId}`);
}

// --- Main ---

function main() {
  const args = process.argv.slice(2);
  if (!args.length) {
    console.log('Usage:');
    console.log('  node extract.js <transcript.jsonl>');
    console.log('  node extract.js --unprocessed [--project <name>]');
    console.log('  node extract.js --mark-processed <session_id>');
    process.exit(1);
  }

  if (args[0] === '--unprocessed') {
    const projIdx = args.indexOf('--project');
    const projectFilter = projIdx !== -1 && args[projIdx + 1] ? args[projIdx + 1] : null;
    cmdListUnprocessed(projectFilter);
  } else if (args[0] === '--mark-processed') {
    if (!args[1]) {
      process.stderr.write('Usage: extract.js --mark-processed <session-id>\n');
      process.exit(1);
    }
    cmdMarkProcessed(args[1]);
  } else {
    cmdExtract(args[0]);
  }
}

main();
