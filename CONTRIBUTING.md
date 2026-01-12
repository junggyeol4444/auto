# Contributing to YouTube Auto Content Generator

We welcome contributions! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/junggyeol4444/auto/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)
   - Error messages and logs

### Suggesting Features

1. Check existing issues and discussions
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/junggyeol4444/auto.git
cd auto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run setup validation
python setup.py
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic
- Keep functions focused and concise

## Testing

- Test your changes before submitting
- Add tests for new features
- Ensure existing tests still pass

## Module Guidelines

### Adding New Crawlers

1. Extend `BaseCrawler` in `src/crawler/web_crawler.py`
2. Implement required methods
3. Add error handling and logging
4. Respect robots.txt and rate limits

### Adding New TTS Engines

1. Extend `TTSEngine` in `src/tts/tts_engine.py`
2. Implement `synthesize()` method
3. Add to `TTSManager._create_engine()`
4. Document usage in README

### Adding New Templates

1. Extend `ScriptTemplate` in `src/content/restructure.py`
2. Implement `format()` method
3. Add to `ContentRestructurer.templates`
4. Create template file in `templates/`

## Documentation

- Update README.md for major changes
- Update USER_GUIDE.md for user-facing features
- Update API.md for API changes
- Add comments for complex code

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be concise (50 chars or less)
- Reference issues and PRs when applicable

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

## Questions?

Feel free to ask questions by:
- Opening an issue with the "question" label
- Starting a discussion in GitHub Discussions

Thank you for contributing! 🎉
