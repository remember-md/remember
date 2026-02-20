const fs = require('fs');
const path = require('path');
const { getBrainRoot } = require('../../scripts/config');

const MAX_EVIDENCE_LINES = 10;

function truncateEvidence(persona) {
  const evidenceHeader = /^###?\s*Evidence\s*Log/im;
  const match = persona.match(evidenceHeader);
  if (!match) return persona;

  const headerIdx = persona.indexOf(match[0]);
  const beforeEvidence = persona.slice(0, headerIdx + match[0].length);
  const afterHeader = persona.slice(headerIdx + match[0].length);

  const nextSection = afterHeader.match(/^##\s/m);
  const evidenceBlock = nextSection ? afterHeader.slice(0, nextSection.index) : afterHeader;
  const afterEvidence = nextSection ? afterHeader.slice(nextSection.index) : '';

  const lines = evidenceBlock.split('\n').filter(l => l.trim().startsWith('-') || l.trim().startsWith('['));
  if (lines.length <= MAX_EVIDENCE_LINES) return persona;

  const truncated = lines.slice(-MAX_EVIDENCE_LINES);
  return beforeEvidence + '\n' + truncated.join('\n') + '\n\n' + afterEvidence;
}

const handler = async (event) => {
  if (event.type !== 'command' || event.action !== 'new') return;

  const brain = getBrainRoot();
  if (!fs.existsSync(brain)) return;

  const personaPath = path.join(brain, 'Persona.md');
  let persona;
  try { persona = fs.readFileSync(personaPath, 'utf-8'); } catch { return; }
  if (!persona.trim()) return;

  persona = truncateEvidence(persona);

  event.messages.push(
    `REMEMBER BRAIN LOADED. Brain: ${brain}\n\n` +
    `PERSONA (apply throughout session):\n${persona}\n\n` +
    `Commands: /remember:process, /remember:status, 'remember this: ...'`
  );
};

module.exports = handler;
module.exports.default = handler;
