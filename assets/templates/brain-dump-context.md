1. ROUTING:
- Person interaction → People/name.md
- Task/TODO → Tasks/tasks.md
- Project work → Projects/name/name.md
- Technical learning → Notes/topic.md
- Decision → Notes/decision-topic.md
- Daily log → Journal/{{TODAY}}.md
- Area (career/health/family/finances) → Areas/area.md
- Link/article → Resources/
- Unclear → Inbox/

2. PROCESSING:
- READ existing file FIRST — match style, append don't replace
- YAML frontmatter: created, updated (today), tags
- Use [[wikilinks]] everywhere — Obsidian handles backlinks automatically
- File names: kebab-case.md
- People files: firstname.md or firstname-lastname.md
- Link format: [[People/name]] or [[Projects/name/name|Display Name]]

3. LINKING (Obsidian-native):
- Link FORWARD from where you write. Obsidian shows backlinks automatically.
- Do NOT manually create reverse links — Obsidian's Backlinks panel handles that.
- Use [[wikilinks]] to connect: [[People/name]], [[Projects/name/name|Name]], [[Notes/topic]]
- In frontmatter use related: ["[[Notes/topic]]", "[[Projects/name/name]]"]

4. WHEN TO WRITE CONTENT IN MULTIPLE FILES (not just links):
- Only update multiple files when adding ACTUAL CONTENT, not just backlinks:
- People/name.md → Add meaningful interaction entry to ## Interactions, update last_contact
- Projects/name/name.md → Add work log entry to ## Log with what was done
- Journal/date.md → Daily summary grouped by project with [[wikilinks]] to everything
- Tasks/tasks.md → New tasks with [[Projects/name/name|Name]] and date
- Persona.md → New evidence line if behavioral pattern observed

5. FORMAT:
- People: frontmatter (created, updated, tags, role, relationship, last_contact), sections: ## Who, ## Notes to Remember, ## Interactions
- Projects: sections: ## Overview, ## Active Tasks, ## Log
- Journal: sections grouped by ## Project Name (not chronological)
- Tasks: - [ ] Description [[Projects/name/name|Name]] (YYYY-MM-DD)
- Notes: frontmatter with related: wikilinks array

6. AFTER SAVE — Report:
- List all files created/updated
- Confirm [[wikilinks]] added (Obsidian will handle backlinks)
