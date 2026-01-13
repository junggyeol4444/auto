# Contributing to Smart Video Editor Pro

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Collect information about your environment
3. Create a minimal reproducible example

**Bug Report Template:**
```
**Environment:**
- OS: [Windows 10/11, macOS, Linux]
- Python version: [e.g., 3.9.7]
- Application version: [e.g., 1.0.0]

**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Logs/Screenshots:**
[Attach relevant logs or screenshots]
```

### Suggesting Features

We welcome feature suggestions! Please:
1. Check if the feature is already planned
2. Explain the use case
3. Describe expected behavior
4. Consider implementation complexity

### Contributing Code

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/auto.git
cd auto

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

#### Coding Standards

**Python Style:**
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

**Example:**
```python
def calculate_scene_duration(start_time: float, end_time: float) -> float:
    """
    Calculate the duration of a scene.
    
    Args:
        start_time: Scene start time in seconds
        end_time: Scene end time in seconds
    
    Returns:
        Scene duration in seconds
    """
    return end_time - start_time
```

**Code Formatting:**
```bash
# Format code with black
black src/

# Check style with flake8
flake8 src/

# Type checking with mypy
mypy src/
```

#### Commit Messages

Use clear, descriptive commit messages:

```
Add feature for batch video processing

- Implement queue management
- Add progress tracking for multiple videos
- Update GUI with batch processing tab
```

**Format:**
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (wrapped at 72 chars)
- Reference issues: "Fixes #123"

#### Pull Request Process

1. **Create a Branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes:**
   - Write clean, documented code
   - Add tests if applicable
   - Update documentation

3. **Test Your Changes:**
   ```bash
   # Run existing tests
   python test_basic.py
   
   # Test manually
   python main.py
   ```

4. **Commit and Push:**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request:**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Fill in description template
   - Link related issues

**PR Template:**
```
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

### Areas for Contribution

#### High Priority
- [ ] Add unit tests for core modules
- [ ] Improve error handling and user messages
- [ ] Optimize video processing performance
- [ ] Add support for more video formats
- [ ] Improve GUI responsiveness

#### Medium Priority
- [ ] Add batch processing feature
- [ ] Implement profile import/export
- [ ] Add video preview functionality
- [ ] Create installer for Windows
- [ ] Add keyboard shortcuts

#### Low Priority
- [ ] Add dark theme
- [ ] Implement undo/redo
- [ ] Add video thumbnail generation
- [ ] Create CLI version
- [ ] Add localization support

### Development Guidelines

#### Architecture
- Keep modules loosely coupled
- Use dependency injection where appropriate
- Follow single responsibility principle
- Write testable code

#### Testing
- Write unit tests for new features
- Test edge cases
- Test error conditions
- Maintain test coverage

#### Documentation
- Update README for user-facing changes
- Update ARCHITECTURE for technical changes
- Add docstrings to new functions
- Update USAGE guide for new features

### Code Review Process

All contributions go through code review:
1. Automated checks (future: CI/CD)
2. Manual review by maintainers
3. Testing by reviewers
4. Approval and merge

**Review Criteria:**
- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Security considerations

### Community Guidelines

**Be Respectful:**
- Welcome newcomers
- Be patient and constructive
- Focus on code, not people
- Assume good intentions

**Be Professional:**
- Use clear, professional language
- Stay on topic
- Respect different opinions
- Follow code of conduct

### Getting Help

**Questions?**
- Open a GitHub discussion
- Ask in pull request comments
- Check existing documentation
- Contact maintainers

**Resources:**
- README.md - Project overview
- ARCHITECTURE.md - Technical details
- USAGE.md - User guide
- QUICKSTART.md - Getting started

### Recognition

Contributors will be:
- Listed in contributors file
- Mentioned in release notes
- Credited in documentation
- Added to GitHub contributors page

Thank you for contributing to Smart Video Editor Pro! 🎉

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
