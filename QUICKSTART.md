# Job Apply CLI - Quick Start Guide

This guide will help you get started with the Job Apply CLI tool.

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers (for auto-fill feature)

```bash
playwright install chromium
```

### 3. Set Up Configuration

```bash
# Copy the example profile
cp config/profile.yaml.example config/profile.yaml

# Edit with your information
nano config/profile.yaml  # or use your favorite editor
```

### 4. Set Up API Keys

```bash
# Copy the sample env file
cp .env.sample .env

# Add your API keys
echo "OPENAI_API_KEY=your-key-here" >> .env
# OR
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
```

## Usage Examples

### 1. Generate a Cover Letter

```bash
# Using job description from a file
python -m src.cli cover-letter \
  --job-desc-file demo/sample_job.txt \
  --company "Acme Corp" \
  --role "Senior Software Engineer" \
  --notes "Emphasize my leadership experience"

# Using direct text
python -m src.cli cover-letter \
  --job-desc "We are looking for a Python developer..." \
  --company "Tech Startup" \
  --role "Python Developer"
```

### 2. Tailor a Resume

```bash
# Create a sample resume first
cat > demo/base_resume.txt << 'EOF'
John Doe
Software Engineer

Experience:
- Led development of microservices platform at Tech Corp (2020-2024)
- Built React applications at Startup Inc (2018-2020)
- Developed Python APIs and automated testing frameworks

Skills: Python, JavaScript, React, Node.js, AWS, Docker, PostgreSQL
EOF

# Tailor it to a job
python -m src.cli tailor-resume \
  --resume demo/base_resume.txt \
  --job-desc-file demo/sample_job.txt \
  --output output/tailored_resume.txt
```

### 3. Auto-Fill Application (Supervised Mode)

```bash
python -m src.cli auto-fill \
  --url "https://example.com/careers/apply" \
  --mode supervised \
  --resume output/resume.pdf \
  --cover-letter output/cover_letter.pdf
```

### 4. Full Pipeline

```bash
# Run the complete workflow interactively
python -m src.cli apply
```

## Testing Without API Keys

You can run the tests without API keys since they use mocked responses:

```bash
pip install pytest pytest-cov
python -m pytest tests/ -v
```

## Directory Structure After Setup

```
Planit.space.backend/
├── config/
│   ├── profile.yaml              # Your personal info (DO NOT COMMIT)
│   ├── profile.yaml.example      # Example template
│   ├── cover_letter_style.yaml   # PDF styling
│   └── prompts.yaml              # AI prompts
├── output/                       # Generated files appear here
│   ├── CoverLetter_AcmeCorp_20240210.pdf
│   └── resume_tailored.txt
├── demo/                         # Demo files
│   ├── sample_job.txt
│   └── base_resume.txt
└── .env                          # API keys (DO NOT COMMIT)
```

## Common Issues

### "API key not found"
- Make sure you have created a `.env` file in the project root
- Check that your API key is in the correct format:
  - OpenAI: `sk-...`
  - Anthropic: `sk-ant-...`

### "Profile not found"
- Copy `config/profile.yaml.example` to `config/profile.yaml`
- Fill in your personal information

### "Playwright browser not found"
- Run: `playwright install chromium`

### Tests failing
- Make sure you have pytest installed: `pip install pytest pytest-cov`
- Tests use mocks and don't require API keys

## Next Steps

1. Customize your profile in `config/profile.yaml`
2. Adjust PDF styling in `config/cover_letter_style.yaml`
3. Modify AI prompts in `config/prompts.yaml` if needed
4. Try generating a cover letter with a real job posting
5. Experiment with different AI providers and models

## Getting Help

```bash
# General help
python -m src.cli --help

# Command-specific help
python -m src.cli cover-letter --help
python -m src.cli tailor-resume --help
python -m src.cli auto-fill --help
python -m src.cli apply --help
```

## Security Notes

- Never commit your `.env` file or `config/profile.yaml` to version control
- Review all generated content before submitting applications
- In supervised mode, the tool will pause for your review before submitting
