# Changelog

All notable changes to ProjectForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-23

### Added
- **Core Features**
  - 5-agent sequential workflow (BA → Architect → QA → Synthesizer → PM)
  - Multi-format output generation (TXT, HTML, PDF)
  - Interactive CLI for project description input
  - Comprehensive business analysis with technical design

- **Enterprise Features**
  - Partial failure recovery with graceful degradation
  - Safe task extraction by agent role (no magic number indexing)
  - 12-Factor App configuration via environment variables
  - Context synthesis layer to prevent token bloat (40% reduction)

- **Agents**
  - Requirements Intake Specialist (Business Analyst)
  - Technical Architect (Database schemas, API design)
  - Senior Quality Auditor (Security, edge cases, validation)
  - Technical Synthesizer (Context reduction layer)
  - Project Manager (Sprint planning, success metrics)

- **Output Formats**
  - Plain text reports with section headers
  - Interactive HTML with collapsible sections and color-coded badges
  - Professional PDF documents via WeasyPrint

- **Utilities**
  - Production-grade markdown to HTML conversion
  - Role-based task output extraction with error handling
  - HTML template generator with embedded CSS and JavaScript

- **Documentation**
  - Comprehensive README.md with quick start guide
  - Detailed API.md with function references and examples
  - CONTRIBUTING.md with development guidelines
  - CHANGELOG.md (this file)
  - requirements.txt with dependency specifications

### Technical Details
- **LLM Support:** Google Gemini 2.5 Flash (configurable via .env)
- **Python Version:** 3.11+
- **Framework:** CrewAI for multi-agent orchestration
- **Dependencies:** crewai, google-generativeai, python-dotenv, markdown, weasyprint

### Architecture
```
User Input → BA → Architect → QA → Synthesizer → PM → Output (TXT/HTML/PDF)
                    ↓           ↓        ↓
                  Context  →  Context  → Context
```

### Performance
- Average execution time: 2-3 minutes
- Token usage: ~5,000-7,000 tokens (with synthesis)
- Context reduction: 40% via synthesis layer

### Security
- API keys stored in .env (excluded from git)
- No data persistence beyond local file system
- HTTPS for all LLM API communications

---

## [Unreleased]

### Planned Features
- Support for OpenAI GPT-4 and Anthropic Claude
- CLI argument parsing for non-interactive mode
- YAML/JSON configuration file support
- Web UI for project analysis
- Export to Word (.docx) and pure Markdown
- Unit test coverage (target: 80%+)
- Docker containerization
- CI/CD pipeline with GitHub Actions

### Known Issues
- PDF generation requires system dependencies (Pango, Cairo)
- Limited to sequential processing (no parallel agent execution)
- No caching layer for LLM responses (every run makes fresh API calls)

---

## Version History

### [1.0.0] - 2026-02-23
Initial release with core functionality

---

## Upgrade Guide

### From Development to 1.0.0

1. **Update dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add LLM_MODEL to .env**
   ```bash
   echo "LLM_MODEL=gemini/gemini-2.5-flash" >> .env
   ```

3. **Install system dependencies (macOS)**
   ```bash
   brew install pango gdk-pixbuf libffi
   ```

4. **Update imports (if using as library)**
   ```python
   # Old
   from utils import extract_outputs
   
   # New
   from project_forge.utils.task_extractors import extract_task_outputs_safe
   ```

---

## Breaking Changes

None (initial release)

---

## Deprecations

None (initial release)

---

## Contributors

- Initial development and architecture
- Enterprise refactoring and optimization
- Documentation and API reference

---

**For detailed API documentation, see [API.md](API.md)**  
**For contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)**
