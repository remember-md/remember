const fs = require('fs');
const path = require('path');
const { getBrainRoot, loadConfig } = require('./scripts/config');
const { formatCompact } = require('./scripts/build-index');

function register(api) {
  // Register hooks from openclaw-hooks directory
  try {
    const { registerPluginHooksFromDir } = require('openclaw/plugin-sdk');
    registerPluginHooksFromDir(api, './openclaw-hooks');
  } catch {
    api.logger.warn('remember: could not register hooks (openclaw/plugin-sdk not available)');
  }

  // Tool: remember_brain_dump_context
  // Returns brain index + processing instructions when the agent needs to save knowledge
  api.registerTool({
    name: 'remember_brain_dump_context',
    description: 'Get brain dump context with index and processing instructions. Call this when the user says "remember this", "save this", "brain dump", or similar.',
    parameters: {
      type: 'object',
      properties: {
        userMessage: {
          type: 'string',
          description: 'The user message that triggered the brain dump',
        },
      },
      required: ['userMessage'],
    },
    async execute(_id, params) {
      const brain = getBrainRoot();
      if (!fs.existsSync(brain)) {
        return { content: [{ type: 'text', text: 'Brain not found. Run /remember:init first.' }] };
      }

      let compactIndex;
      try {
        compactIndex = formatCompact(brain);
      } catch {
        compactIndex = `BRAIN INDEX (${brain})\n(index unavailable)`;
      }

      const pluginRoot = __dirname;
      const templatePath = path.join(pluginRoot, 'assets', 'templates', 'brain-dump-context.md');
      const today = new Date().toISOString().slice(0, 10);
      let instructions;
      try {
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

      const context =
        `BRAIN DUMP — Full processing instructions. Brain: ${brain}. Today: ${today}.\n\n` +
        `${compactIndex}\n\n` +
        `${instructions}` +
        `${rememberContext}`;

      return { content: [{ type: 'text', text: context }] };
    },
  });

  // Tool: remember_brain_index
  // Returns compact brain index for quick lookups
  api.registerTool({
    name: 'remember_brain_index',
    description: 'Get the brain index showing all tracked people, projects, areas, notes, tasks, and journal entries.',
    parameters: {
      type: 'object',
      properties: {},
      additionalProperties: false,
    },
    async execute() {
      const brain = getBrainRoot();
      if (!fs.existsSync(brain)) {
        return { content: [{ type: 'text', text: 'Brain not found. Run /remember:init first.' }] };
      }

      try {
        const index = formatCompact(brain);
        return { content: [{ type: 'text', text: index }] };
      } catch (err) {
        return { content: [{ type: 'text', text: `Error building index: ${err.message}` }] };
      }
    },
  });
}

module.exports = register;
module.exports.default = register;
