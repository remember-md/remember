#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { getBrainRoot } = require('./config');

const MAX_EVIDENCE_LINES = 10;

const brain = getBrainRoot();
if (!fs.existsSync(brain)) process.exit(0);

const personaPath = path.join(brain, 'Persona.md');
let persona;
try { persona = fs.readFileSync(personaPath, 'utf-8'); } catch { process.exit(0); }
if (!persona.trim()) process.exit(0);

// Truncate evidence log to last N entries to prevent context bloat
const evidenceHeader = /^###?\s*Evidence\s*Log/im;
const match = persona.match(evidenceHeader);
if (match) {
  const headerIdx = persona.indexOf(match[0]);
  const beforeEvidence = persona.slice(0, headerIdx + match[0].length);
  const afterHeader = persona.slice(headerIdx + match[0].length);

  // Find where next section starts (or end of file)
  const nextSection = afterHeader.match(/^##\s/m);
  const evidenceBlock = nextSection ? afterHeader.slice(0, nextSection.index) : afterHeader;
  const afterEvidence = nextSection ? afterHeader.slice(nextSection.index) : '';

  const evidenceLines = evidenceBlock.split('\n').filter(l => l.trim().startsWith('-') || l.trim().startsWith('['));
  if (evidenceLines.length > MAX_EVIDENCE_LINES) {
    const truncated = evidenceLines.slice(-MAX_EVIDENCE_LINES);
    persona = beforeEvidence + '\n' + truncated.join('\n') + '\n\n' + afterEvidence;
  }
}

process.stdout.write(
  `REMEMBER BRAIN LOADED. Brain: ${brain}\n\n` +
  `PERSONA (apply throughout session):\n${persona}\n\n` +
  `Commands: /remember:process, /remember:status, 'remember this: ...'\n`
);
