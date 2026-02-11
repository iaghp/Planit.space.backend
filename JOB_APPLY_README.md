# Job Apply - CLI-based Job Application Automation Suite

A comprehensive Python CLI tool that streamlines the entire job application process: generating personalized cover letters, tailoring resumes, and automating browser-based job application form filling.

## Features

- 🤖 **AI-Powered Cover Letter Generation** - Generate personalized cover letters using OpenAI or Anthropic Claude
- 📄 **Resume Tailoring** - Automatically tailor your resume to match job descriptions
- 🌐 **Browser Automation** - Auto-fill job application forms with supervised, semi-auto, or full-auto modes
- 📑 **Professional PDF Generation** - Create beautifully formatted PDFs with custom fonts and signatures
- ⚙️ **YAML-Based Configuration** - Easy-to-edit configuration files for all your preferences
- 🎨 **Rich Terminal Output** - Beautiful, colorful terminal interface

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Install from source

```bash
# Clone the repository
git clone https://github.com/iaghp/Planit.space.backend.git
cd Planit.space.backend

# Install the package in editable mode
pip install -e .

# Install Playwright browsers (required for auto-fill feature)
playwright install
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Set up API Keys

Create a `.env` file in the project root:

```bash
# OpenAI API Key (optional - use either OpenAI or Anthropic)
OPENAI_API_KEY=sk-...

# Anthropic API Key (optional - use either OpenAI or Anthropic)
ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Configure Your Profile

Copy the example profile and customize it:

```bash
cp config/profile.yaml.example config/profile.yaml
```

Edit `config/profile.yaml` with your personal information:

```yaml
name: "John Doe"
email: "john.doe@example.com"
phone: "+1 (555) 123-4567"
address:
  street: "123 Main St"
  city: "San Francisco"
  state: "CA"
  zip: "94102"
linkedin: "https://linkedin.com/in/johndoe"
github: "https://github.com/johndoe"
website: "https://johndoe.com"
```

### 3. Customize Cover Letter Style (Optional)

Edit `config/cover_letter_style.yaml` to customize PDF formatting:

```yaml
font_family: "Helvetica"
font_size: 11
margins:
  top: 72
  bottom: 72
  left: 72
  right: 72
```

## Usage

### Quick Start - Full Pipeline

Generate a cover letter, tailor your resume, and auto-fill an application:

```bash
job-apply apply
```

This interactive command will:
1. Prompt you to paste a job description
2. Generate a personalized cover letter
3. Tailor your resume
4. Open a browser and help you fill the application

### Generate Cover Letter

```bash
# From job description text
job-apply cover-letter \
  --job-desc "We are looking for a Senior Software Engineer..." \
  --company "Acme Corp" \
  --role "Senior Software Engineer" \
  --notes "Emphasize my React experience" \
  --output ./output/cover_letter.pdf

# From job description file
job-apply cover-letter \
  --job-desc-file ./job_posting.txt \
  --company "Acme Corp" \
  --role "Senior Software Engineer"
```

### Tailor Resume

```bash
job-apply tailor-resume \
  --job-desc-file ./job_posting.txt \
  --resume ./templates/base_resume.pdf \
  --output ./output/resume_tailored.pdf
```

### Auto-Fill Application

```bash
# Supervised mode (recommended) - fills one section at a time with confirmation
job-apply auto-fill \
  --url "https://company.com/careers/apply" \
  --mode supervised \
  --resume ./output/resume.pdf \
  --cover-letter ./output/cover_letter.pdf

# Semi-auto mode - fills everything but pauses before submission
job-apply auto-fill \
  --url "https://company.com/careers/apply" \
  --mode semi-auto

# Full-auto mode - fills and submits (with final confirmation)
job-apply auto-fill \
  --url "https://company.com/careers/apply" \
  --mode full-auto
```

### Configure Profile Interactively

```bash
job-apply config
```

### Select AI Provider

```bash
# Use OpenAI (default)
job-apply cover-letter --ai-provider openai ...

# Use Anthropic Claude
job-apply cover-letter --ai-provider anthropic ...
```

## Project Structure

```
Planit.space.backend/
├── CLAUDE.md                    # Claude Code project context
├── README.md                    # This file
├── pyproject.toml               # Python project config
├── requirements.txt             # Dependencies
├── setup.py                     # Package setup
├── .env                         # API keys (not committed)
├── config/
│   ├── profile.yaml.example     # Example user profile
│   ├── profile.yaml             # Your profile (not committed)
│   ├── cover_letter_style.yaml  # Cover letter styling
│   └── prompts.yaml             # AI prompts
├── fonts/                       # Custom .ttf fonts
├── templates/                   # Base resume, signature image
├── output/                      # Generated files
├── src/
│   ├── __init__.py
│   ├── cli.py                   # Main CLI
│   ├── ai_client.py             # AI client wrapper
│   ├── cover_letter.py          # Cover letter generation
│   ├── resume_tailor.py         # Resume tailoring
│   ├── pdf_formatter.py         # PDF generation
│   ├── auto_apply.py            # Browser automation
│   └── config_manager.py        # Config management
└── tests/                       # Test suite
```

## Advanced Features

### Custom Fonts

Place `.ttf` font files in the `fonts/` directory and reference them in `config/cover_letter_style.yaml`.

### Signature Image

Place a signature image (PNG recommended) in `templates/signature.png` and reference it in your style config.

### Custom AI Prompts

Edit `config/prompts.yaml` to customize how the AI generates content:

```yaml
cover_letter_system_prompt: |
  You are a professional career advisor...

cover_letter_user_template: |
  Generate a cover letter for {role} at {company}...
```

## Supported Application Platforms

The auto-fill feature supports common ATS platforms including:
- Greenhouse
- Lever
- Workday
- BambooHR
- SmartRecruiters
- And generic application forms

## Troubleshooting

### Browser automation not working

Make sure Playwright browsers are installed:

```bash
playwright install
```

### PDF generation issues

Ensure you have write permissions to the `output/` directory.

### API errors

Check your `.env` file and ensure your API keys are valid and have sufficient credits.

## Development

### Run tests

```bash
pytest
```

### Code formatting

```bash
black src/
```

### Type checking

```bash
mypy src/
```

## Security Notes

- **Never commit** your `.env` file or `config/profile.yaml` to version control
- API keys should always be stored in environment variables
- Review all auto-filled information before submitting applications

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
