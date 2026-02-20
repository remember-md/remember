#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { getBrainRoot, loadConfig } = require('./config');
const { formatCompact } = require('./build-index');

if (process.env.REMEMBER_PROCESSING === '1') process.exit(0);

// Read stdin
let input = '';
try {
  input = fs.readFileSync(0, 'utf-8');
} catch {
  process.exit(0);
}

const pluginRoot = process.env.CLAUDE_PLUGIN_ROOT || path.resolve(__dirname, '..');
const brain = getBrainRoot();

if (!fs.existsSync(brain)) process.exit(0);

const config = loadConfig();
const keywords = config.session?.brain_dump_keywords || [
  'save this', 'remember this', 'brain dump', 'note to self',
  'capture this', 'save to brain', 'write to brain', 'add to brain',
  'salvează', 'notează', 'reține',
];

const inputLower = input.toLowerCase();
if (!keywords.some(k => inputLower.includes(k))) process.exit(0);

// Build compact index (inline, no subprocess)
let compactIndex;
try {
  compactIndex = formatCompact(brain);
} catch {
  compactIndex = `BRAIN INDEX (${brain})\n(index unavailable)`;
}

// Read template
const templatePath = path.join(pluginRoot, 'assets', 'templates', 'brain-dump-context.md');
let instructions;
try {
  const today = new Date().toISOString().slice(0, 10);
  instructions = fs.readFileSync(templatePath, 'utf-8').replace(/\{\{TODAY\}\}/g, today);
} catch {
  instructions = '(template missing)';
}

// Load REMEMBER.md — cascading: global (brain) + project (cwd)
const sectionsToExtract = ['Capture Rules', 'Processing', 'Custom Types', 'Language'];

function extractSections(filePath, sections) {
  let text;
  try { text = fs.readFileSync(filePath, 'utf-8'); } catch { return {}; }
  const result = {};
  for (const name of sections) {
    const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp(`^## ${escaped}\\s*\\n(.*?)(?=^## |$)`, 'ms');
    const match = text.match(re);
    if (match) {
      const content = match[1].trim();
      if (content) result[name] = content;
    }
  }
  return result;
}

const globalSections = extractSections(path.join(brain, 'REMEMBER.md'), sectionsToExtract);
const projectSections = extractSections(path.join(process.cwd(), 'REMEMBER.md'), sectionsToExtract);

// Merge: project appends to global
const merged = {};
for (const name of sectionsToExtract) {
  const parts = [];
  if (globalSections[name]) parts.push(globalSections[name]);
  if (projectSections[name]) parts.push(projectSections[name]);
  if (parts.length) merged[name] = parts.join('\n\n');
}

let rememberContext = '';
if (Object.keys(merged).length) {
  const extracted = Object.entries(merged).map(([name, content]) => `## ${name}\n${content}`);
  rememberContext = '\n\nUSER OVERRIDES (these take precedence over defaults above):\n' + extracted.join('\n\n');
}

const today = new Date().toISOString().slice(0, 10);
const context =
  `BRAIN DUMP — Full processing instructions. Brain: ${brain}. Today: ${today}.\n\n` +
  `${compactIndex}\n\n` +
  `${instructions}` +
  `${rememberContext}`;

const output = {
  hookSpecificOutput: {
    hookEventName: 'UserPromptSubmit',
    additionalContext: context,
  },
};

console.log(JSON.stringify(output, null, 0));
