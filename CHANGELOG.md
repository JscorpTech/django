# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- English documentation (README.EN.md) for international developers
- SECURITY.md with comprehensive security best practices in both Uzbek and English
- CONTRIBUTING.md with detailed contribution guidelines
- GitHub issue templates (bug report and feature request)
- GitHub pull request template
- Language switcher in main README
- Better error handling and user feedback in post_gen_project.py hook
- Security warnings in .env.example for sensitive values

### Changed
- Improved default credentials in cookiecutter.json to use more descriptive example values
- Standardized Makefile commands:
  - `makemigration` → `makemigrations` (matches Django command)
  - `makemigrate` → `migrations` (clearer naming)
- Docker Compose files now use environment variables for database passwords:
  - docker-compose.yml: Uses environment variables with safe defaults for development
  - docker-compose.prod.yml: Requires DB_PASSWORD to be explicitly set (fails if not provided)
  - docker-compose.test.yml: Uses environment variables with safe defaults for testing

### Fixed
- **Critical:** Typo `SILK_ENEBLED` corrected to `SILK_ENABLED` in 4 files:
  - config/settings/common.py
  - config/conf/apps.py
  - config/urls.py
  - config/env.py
- Hardcoded database passwords in production Docker Compose configuration
- Missing error handling in cookiecutter hooks

### Security
- Database passwords in Docker Compose files no longer hardcoded
- Production docker-compose now requires explicit password setting
- Added comprehensive security documentation
- Improved default credential examples to be more obviously insecure
- Added warnings throughout configuration files about changing default secrets

## Previous Versions

This changelog was started with version 0.1.1. For earlier changes, please see the git commit history.

---

## Changelog Guidelines

### Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes or security improvements
