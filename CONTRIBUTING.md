# Contributing to ProjectForge

Thank you for considering contributing to ProjectForge! This document outlines the guidelines and best practices for contributing.

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- macOS (for PDF generation testing) or Linux

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/projectforge.git
   cd projectforge
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install system dependencies (macOS)**
   ```bash
   brew install pango gdk-pixbuf libffi
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

## Code Standards

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use docstrings for all public modules, functions, classes, and methods

### Docstring Format
```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.
    
    Longer description if needed, explaining behavior,
    edge cases, or important notes.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input provided
    """
    pass
```

### Naming Conventions
- **Functions/Variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private methods:** `_leading_underscore`

## Branch Strategy

### Branch Naming
- Feature: `feature/description-of-feature`
- Bugfix: `bugfix/description-of-fix`
- Hotfix: `hotfix/critical-issue`
- Documentation: `docs/description-of-changes`

### Example
```bash
git checkout -b feature/add-openai-support
```

## Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

### Examples
```bash
feat(agents): add OpenAI model support

- Added OpenAI LLM configuration
- Updated agent creation to support multiple providers
- Added API key validation

Closes #42

---

fix(exporters): handle missing weasyprint dependency gracefully

- Catch ImportError when weasyprint not installed
- Display helpful installation message
- Continue execution without PDF generation

Fixes #38
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=project_forge

# Run specific test file
pytest tests/test_task_extractors.py
```

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names

**Example:**
```python
def test_extract_task_outputs_by_role_success():
    """Test successful extraction of all task outputs."""
    # Arrange
    tasks = create_mock_tasks()
    
    # Act
    outputs = extract_task_outputs_by_role(tasks)
    
    # Assert
    assert 'intake' in outputs
    assert 'architect' in outputs
    assert outputs['intake'] is not None
```

## Pull Request Process

### Before Submitting
1. Code follows style guidelines
2. All tests pass
3. New tests added for new features
4. Documentation updated
5. Commit messages follow convention
6. Branch is up to date with main

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated

## Related Issues
Closes #(issue number)
```

### Review Process
1. Maintainer will review within 2-3 business days
2. Address feedback with additional commits
3. Once approved, maintainer will merge
4. Delete feature branch after merge

## Bug Reports

### Before Submitting
- Check existing issues for duplicates
- Test with latest version
- Collect error messages and logs

### Bug Report Template
```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: macOS 15.2
- Python: 3.11.5
- ProjectForge Version: 1.0.0

**Error Messages**
```
Paste error traceback here
```

**Additional Context**
Screenshots, logs, or other relevant info
```

## Feature Requests

### Feature Request Template
```markdown
**Problem Statement**
Describe the problem this feature solves

**Proposed Solution**
Describe your ideal solution

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## Priority Areas for Contribution

### High Priority
- [ ] Unit test coverage for all modules
- [ ] Integration tests for full workflow
- [ ] Support for additional LLM providers (OpenAI, Claude)
- [ ] CLI argument parsing for non-interactive mode
- [ ] Configuration file support (YAML/JSON)

### Medium Priority
- [ ] Web UI for project analysis
- [ ] Export to Word/Markdown formats
- [ ] Custom agent/task templates
- [ ] Caching layer for LLM responses
- [ ] Retry logic with exponential backoff

### Low Priority
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Performance benchmarking suite
- [ ] Internationalization (i18n)

## Documentation

### Areas Needing Documentation
- API reference improvements
- Tutorial for custom agents
- Best practices guide
- Architecture deep-dive
- Troubleshooting guide

### Documentation Standards
- Write for beginners
- Include code examples
- Add diagrams where helpful
- Keep updated with code changes

## Security

### Reporting Security Issues
**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security@projectforge.dev
2. Include detailed description
3. Provide steps to reproduce
4. We'll respond within 48 hours

### Security Best Practices
- Never commit API keys or secrets
- Use environment variables for configuration
- Validate all user input
- Keep dependencies updated
- Follow principle of least privilege

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be added to:
- README.md Contributors section
- CHANGELOG.md for their contributions
- GitHub contributors page

## Questions?

- Open a Discussion on GitHub
- Join our Discord server
- Email: contributors@projectforge.dev

---

**Thank you for contributing to ProjectForge!**
