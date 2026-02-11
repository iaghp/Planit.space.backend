# Claude Code Context - Job Apply CLI

## Project Overview

**Job Apply** is a Python CLI-based Job Application Automation Suite that streamlines the entire job application process. It uses AI (OpenAI/Anthropic) to generate personalized cover letters, tailor resumes, and automate browser-based form filling.

## Quick Start

```bash
# Install dependencies
pip install -e .
playwright install

# Set up environment
cp .env.sample .env
# Edit .env with your API keys

# Configure profile
cp config/profile.yaml.example config/profile.yaml
# Edit with your personal info

# Run the CLI
job-apply --help
```

## Architecture

### Core Components

1. **CLI (`src/cli.py`)** - Typer-based command-line interface with commands:
   - `job-apply cover-letter` - Generate cover letters
   - `job-apply tailor-resume` - Tailor resumes to job descriptions
   - `job-apply auto-fill` - Browser automation for application forms
   - `job-apply apply` - Full pipeline (generate + tailor + auto-fill)
   - `job-apply config` - Interactive configuration setup

2. **AI Client (`src/ai_client.py`)** - Unified wrapper for OpenAI and Anthropic APIs
   - Supports both providers with automatic fallback
   - Handles retries and token limits
   - Environment variable-based configuration

3. **Cover Letter Generator (`src/cover_letter.py`)** - AI-powered cover letter creation
   - Loads user profile and job description
   - Applies custom instructions and formatting preferences
   - Generates structured, professional content

4. **PDF Formatter (`src/pdf_formatter.py`)** - Professional PDF generation using ReportLab
   - Custom fonts and signature support
   - 1-page constraint with auto-adjustment
   - Configurable margins, spacing, and styles

5. **Resume Tailor (`src/resume_tailor.py`)** - AI-powered resume customization
   - Parses base resume (PDF, DOCX, text)
   - Identifies relevant experiences to emphasize
   - Rewords and reorders content for job match

6. **Auto-Apply (`src/auto_apply.py`)** - Playwright-based browser automation
   - Three modes: supervised, semi-auto, full-auto
   - Detects and fills common form fields
   - Supports major ATS platforms (Greenhouse, Lever, Workday, etc.)

7. **Config Manager (`src/config_manager.py`)** - YAML-based configuration
   - Profile management
   - Style preferences
   - AI prompt templates

### Configuration Files

- `config/profile.yaml` - User's personal information (name, contact, LinkedIn, etc.)
- `config/cover_letter_style.yaml` - PDF formatting preferences
- `config/prompts.yaml` - AI prompt templates and system messages
- `.env` - API keys (never committed)

### Directory Structure

```
src/                  # Python source code
config/               # YAML configuration files
fonts/                # Custom .ttf fonts for PDFs
templates/            # Base resume, signature image
output/               # Generated PDFs (gitignored)
tests/                # Test suite
```

## Development Workflow

### Adding New Features

1. Update the appropriate module in `src/`
2. Add configuration options to relevant YAML files
3. Update CLI commands in `src/cli.py`
4. Write tests in `tests/`
5. Update documentation

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cover_letter.py

# Run with coverage
pytest --cov=src tests/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/
```

## Common Commands

```bash
# Generate a cover letter
job-apply cover-letter \
  --job-desc "Job description text..." \
  --company "Company Name" \
  --role "Role Title" \
  --output ./output/cover_letter.pdf

# Tailor resume
job-apply tailor-resume \
  --job-desc-file job_posting.txt \
  --resume templates/base_resume.pdf \
  --output output/resume_tailored.pdf

# Auto-fill application (supervised mode)
job-apply auto-fill \
  --url "https://jobs.company.com/apply" \
  --mode supervised \
  --resume output/resume.pdf \
  --cover-letter output/cover_letter.pdf

# Full pipeline
job-apply apply
```

## API Integration

### OpenAI
- Uses `gpt-4` or `gpt-3.5-turbo` models
- Requires `OPENAI_API_KEY` in `.env`
- Client in `src/ai_client.py`

### Anthropic Claude
- Uses `claude-3-opus` or `claude-3-sonnet` models
- Requires `ANTHROPIC_API_KEY` in `.env`
- Client in `src/ai_client.py`

## Key Technical Patterns

### Type Hints
All functions use Python type hints for clarity and IDE support.

### Error Handling
- Graceful degradation with user-friendly error messages
- Retry logic for API calls
- Input validation at CLI level

### Modularity
Each component works independently - can generate cover letters without resume tailoring, etc.

### Configuration-Driven
Most behavior controlled through YAML files, not hardcoded values.

## Environment Variables

```bash
# Required (at least one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Optional
AI_PROVIDER=openai  # or 'anthropic'
DEFAULT_MODEL=gpt-4
```

## Dependencies

Core libraries:
- `typer` - CLI framework
- `openai` - OpenAI API
- `anthropic` - Anthropic API
- `reportlab` - PDF generation
- `playwright` - Browser automation
- `PyYAML` - Configuration
- `rich` - Terminal formatting

## Conventions

### Code Style
- PEP 8 compliance
- 100 character line length (Black formatter)
- Type hints for all functions
- Docstrings for public APIs

### File Naming
- Generated PDFs: `CoverLetter_CompanyName_YYYYMMDD.pdf`
- Tailored resumes: `Resume_CompanyName_YYYYMMDD.pdf`

### Git Workflow
- Never commit `.env` or `config/profile.yaml`
- Keep `output/` directory empty (gitignored)
- Example configs use `.example` suffix

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'src'**
   - Run: `pip install -e .`

2. **Playwright browser not found**
   - Run: `playwright install`

3. **API authentication failed**
   - Check `.env` file has valid API keys
   - Ensure keys have correct format (sk-... for OpenAI, sk-ant-... for Anthropic)

4. **PDF generation fails**
   - Check write permissions on `output/` directory
   - Verify font files exist if using custom fonts

## Notes for AI Assistants

- This is a Python 3.10+ project using modern type hints
- All paths should be absolute when possible
- Configuration is YAML-based, never hardcode settings
- API keys MUST be in environment variables, never in code
- Follow existing patterns for consistency
- Browser automation requires user interaction in supervised mode
- PDFs must fit on 1 page - this is a hard requirement
