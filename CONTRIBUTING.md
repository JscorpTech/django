# Contributing to JST-Django Template

Thank you for your interest in contributing to JST-Django! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Submitting Changes](#submitting-changes)
7. [Style Guidelines](#style-guidelines)
8. [Reporting Bugs](#reporting-bugs)

## Code of Conduct

Please be respectful and constructive in all interactions with other contributors.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your changes

```bash
git clone https://github.com/YOUR_USERNAME/django.git
cd django
git checkout -b feature/your-feature-name
```

## Development Setup

This is a cookiecutter template project. To test your changes:

1. Install cookiecutter:
```bash
pip install cookiecutter
```

2. Generate a project from your local template:
```bash
cookiecutter /path/to/your/local/django/template
```

3. Test the generated project

## Making Changes

### Template Changes

When modifying the template:

1. **Files in `{{cookiecutter.project_slug}}/`** - These are template files
2. **Use Jinja2 syntax** for conditional content: `{% if cookiecutter.option %}`
3. **Test with different configurations** - Try different cookiecutter.json options
4. **Update documentation** - Keep README.MD and README.EN.md in sync

### Hook Changes

When modifying hooks in `hooks/`:

1. Test both success and failure scenarios
2. Add proper error handling
3. Print helpful messages for users

## Testing

Before submitting changes:

1. **Test template generation:**
```bash
cookiecutter . --no-input
```

2. **Test with various options:**
```bash
cookiecutter . --no-input celery=yes silk=yes channels=yes
```

3. **Test the generated project:**
```bash
cd generated_project
make up
make test
```

4. **Check for common issues:**
   - Missing imports
   - Typos in variable names
   - Invalid Python syntax
   - Missing dependencies
   - Security vulnerabilities

## Submitting Changes

1. **Commit your changes:**
```bash
git add .
git commit -m "Description of changes"
```

2. **Push to your fork:**
```bash
git push origin feature/your-feature-name
```

3. **Create a Pull Request:**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots if applicable
   - Explain why the change is needed

## Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use type hints where applicable
- Maximum line length: 120 characters (configurable via cookiecutter)
- Use meaningful variable names
- Add docstrings to functions and classes

### Documentation

- Update both Uzbek (README.MD) and English (README.EN.md) documentation
- Use clear, concise language
- Include examples where helpful
- Keep formatting consistent

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep first line under 72 characters
- Add detailed description if needed

Examples:
```
Fix typo in SILK_ENABLED environment variable

Add English documentation for international users

Update security documentation with best practices
```

## Reporting Bugs

When reporting bugs, please include:

1. **Description** - Clear description of the issue
2. **Steps to Reproduce** - How to reproduce the bug
3. **Expected Behavior** - What should happen
4. **Actual Behavior** - What actually happens
5. **Environment:**
   - OS (Linux, macOS, Windows)
   - Python version
   - Docker version
   - Cookiecutter version
6. **Screenshots** - If applicable
7. **cookiecutter.json values** - What options you used

## Feature Requests

For feature requests:

1. Check if it already exists in issues
2. Clearly describe the feature
3. Explain the use case
4. Provide examples if possible

## Questions?

If you have questions:

1. Check existing documentation
2. Search closed issues
3. Open a new issue with the "question" label

## Common Areas for Contribution

- **Bug fixes** - Always welcome!
- **Documentation** - Improvements and translations
- **New features** - Discuss in an issue first
- **Testing** - Add more test coverage
- **Examples** - Add usage examples
- **Security** - Report vulnerabilities privately

## Recognition

Contributors will be recognized in:
- Git commit history
- Release notes
- Project documentation

Thank you for contributing! 🎉
