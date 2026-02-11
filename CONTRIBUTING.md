# Contributing to Remember

Thanks for your interest in contributing to Remember! 🎉

## Ways to Contribute

- 🐛 **Report bugs** — Open an issue with steps to reproduce
- 💡 **Suggest features** — Share your ideas in Discussions or Issues
- 📖 **Improve documentation** — Fix typos, add examples, clarify instructions
- 🔧 **Submit pull requests** — Code contributions welcome!

## Development Setup

```bash
git clone https://github.com/remember-md/remember.git
cd remember

# Test the plugin locally
cp -r . ~/.claude/plugins/remember
```

## Pull Request Guidelines

1. **Fork** the repo
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** with clear commit messages
4. **Test** your changes (run manual tests, check hooks work)
5. **Push** to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request** with a clear description of what you changed and why

## Code Style

- **Shell scripts:** Follow existing style, use `set -euo pipefail`, quote variables
- **Python:** Follow PEP 8, add docstrings for functions
- **Markdown:** Keep lines under 100 chars where reasonable
- **Commit messages:** Use conventional commits format (`feat:`, `fix:`, `docs:`, `refactor:`)

## Testing

Before submitting a PR:
- [ ] Test hooks manually (SessionStart, UserPromptSubmit)
- [ ] Verify config resolution works
- [ ] Check that no shell injection risks were introduced
- [ ] Ensure backwards compatibility

## Questions?

- Open a [Discussion](https://github.com/remember-md/remember/discussions)
- Or create an [Issue](https://github.com/remember-md/remember/issues)

We're happy to help! 🙌
