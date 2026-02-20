#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { getBrainRoot, parseFrontmatter } = require('./config');

function scanPeople(brain) {
  const dir = path.join(brain, 'People');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .sort()
    .map(f => {
      const m = parseFrontmatter(path.join(dir, f));
      const stem = f.slice(0, -3);
      return {
        file: stem,
        name: m._title || stem.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        role: m.role || '',
        org: m.org || m.organization || '',
        last_contact: m.last_contact || m.updated || '',
        tags: m.tags || '',
      };
    });
}

function scanProjects(brain) {
  const dir = path.join(brain, 'Projects');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(d => {
      try { return fs.statSync(path.join(dir, d)).isDirectory(); } catch { return false; }
    })
    .sort()
    .map(d => {
      const dirPath = path.join(dir, d);
      let mainFile = path.join(dirPath, `${d}.md`);
      if (!fs.existsSync(mainFile)) {
        const mds = fs.readdirSync(dirPath).filter(f => f.endsWith('.md'));
        mainFile = mds.length ? path.join(dirPath, mds[0]) : null;
      }
      if (!mainFile) return null;
      const m = parseFrontmatter(mainFile);
      const subCount = fs.readdirSync(dirPath).filter(f => f.endsWith('.md')).length - 1;
      return {
        file: d,
        name: m._title || d.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        status: m.status || '',
        tags: m.tags || '',
        updated: m.updated || '',
        sub_notes: Math.max(0, subCount),
      };
    })
    .filter(Boolean);
}

function scanAreas(brain) {
  const dir = path.join(brain, 'Areas');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .sort()
    .map(f => {
      const m = parseFrontmatter(path.join(dir, f));
      const stem = f.slice(0, -3);
      return {
        file: stem,
        name: m._title || stem.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        updated: m.updated || '',
      };
    });
}

function scanNotes(brain) {
  const dir = path.join(brain, 'Notes');
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.md'))
    .sort()
    .map(f => {
      const m = parseFrontmatter(path.join(dir, f));
      const stem = f.slice(0, -3);
      return {
        file: stem,
        name: m._title || stem.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        tags: m.tags || '',
        created: m.created || '',
      };
    });
}

function scanTasks(brain) {
  const tasksFile = path.join(brain, 'Tasks', 'tasks.md');
  const counts = { focus: 0, next_up: 0, backlog: 0, done: 0 };
  let text;
  try { text = fs.readFileSync(tasksFile, 'utf-8'); } catch { return counts; }

  let current = null;
  for (const line of text.split('\n')) {
    const lower = line.trim().toLowerCase();
    if (lower.startsWith('## focus')) current = 'focus';
    else if (lower.startsWith('## next up')) current = 'next_up';
    else if (lower.startsWith('## backlog')) current = 'backlog';
    else if (lower.startsWith('## done') || lower.startsWith('## completed')) current = 'done';
    else if (lower.startsWith('## ')) current = null;
    else if (current && /^-\s*\[.\]/.test(line.trim())) counts[current]++;
  }
  return counts;
}

function scanJournal(brain) {
  const dir = path.join(brain, 'Journal');
  if (!fs.existsSync(dir)) return { count: 0, latest: '' };
  const entries = fs.readdirSync(dir).filter(f => f.endsWith('.md')).sort();
  return {
    count: entries.length,
    latest: entries.length ? entries[entries.length - 1].slice(0, -3) : '',
  };
}

function formatFull(brain) {
  const lines = [`# Knowledge Index\n**Brain:** \`${brain}\`\n`];

  const people = scanPeople(brain);
  if (people.length) {
    lines.push('## People\n| Name | Role/Org | Last Contact | Tags |');
    lines.push('|------|----------|--------------|------|');
    for (const p of people) {
      const org = p.role + (p.org ? ` @ ${p.org}` : '');
      lines.push(`| [[People/${p.file}\\|${p.name}]] | ${org} | ${p.last_contact} | ${p.tags} |`);
    }
  } else {
    lines.push('## People\n*None yet*');
  }
  lines.push('');

  const projects = scanProjects(brain);
  if (projects.length) {
    lines.push('## Projects\n| Name | Status | Updated | Sub-notes | Tags |');
    lines.push('|------|--------|---------|-----------|------|');
    for (const p of projects) {
      lines.push(`| [[Projects/${p.file}/${p.file}\\|${p.name}]] | ${p.status} | ${p.updated} | ${p.sub_notes} | ${p.tags} |`);
    }
  } else {
    lines.push('## Projects\n*None yet*');
  }
  lines.push('');

  const areas = scanAreas(brain);
  if (areas.length) {
    lines.push('## Areas\n| Name | Updated |');
    lines.push('|------|---------|');
    for (const a of areas) {
      lines.push(`| [[Areas/${a.file}\\|${a.name}]] | ${a.updated} |`);
    }
  } else {
    lines.push('## Areas\n*None yet*');
  }
  lines.push('');

  const notes = scanNotes(brain);
  if (notes.length) {
    lines.push(`## Notes (${notes.length} total)\n| Name | Tags | Created |`);
    lines.push('|------|------|---------|');
    for (const n of notes) {
      lines.push(`| [[Notes/${n.file}\\|${n.name}]] | ${n.tags} | ${n.created} |`);
    }
  } else {
    lines.push('## Notes\n*None yet*');
  }
  lines.push('');

  const tasks = scanTasks(brain);
  lines.push(`## Tasks\n- **Focus:** ${tasks.focus} items`);
  lines.push(`- **Next Up:** ${tasks.next_up} items`);
  lines.push(`- **Backlog:** ${tasks.backlog} items`);
  lines.push(`- **Done:** ${tasks.done} items`);
  lines.push('');

  const journal = scanJournal(brain);
  lines.push(`## Journal\n- **Entries:** ${journal.count}`);
  if (journal.latest) lines.push(`- **Latest:** ${journal.latest}`);

  return lines.join('\n');
}

function formatCompact(brain) {
  const people = scanPeople(brain).map(p => p.file);
  const projects = scanProjects(brain).map(p => p.file);
  const areas = scanAreas(brain).map(a => a.file);
  const notes = scanNotes(brain).map(n => n.file);
  const tasks = scanTasks(brain);
  const journal = scanJournal(brain);

  return [
    `BRAIN INDEX (${brain})`,
    `People: ${people.join(', ') || 'none'}`,
    `Projects: ${projects.join(', ') || 'none'}`,
    `Areas: ${areas.join(', ') || 'none'}`,
    `Notes (${notes.length}): ${notes.slice(0, 20).join(', ') || 'none'}${notes.length > 20 ? '...' : ''}`,
    `Tasks: ${tasks.focus} focus, ${tasks.next_up} next, ${tasks.backlog} backlog`,
    `Journal: ${journal.count} entries, latest ${journal.latest}`,
  ].join('\n');
}

module.exports = { scanPeople, scanProjects, scanAreas, scanNotes, scanTasks, scanJournal, formatFull, formatCompact };

if (require.main === module) {
  const brain = getBrainRoot();
  if (!fs.existsSync(brain)) {
    process.stderr.write(`Brain not found at ${brain}. Run /remember:init first.\n`);
    process.exit(1);
  }
  const compact = process.argv.includes('--compact');
  console.log(compact ? formatCompact(brain) : formatFull(brain));
}
