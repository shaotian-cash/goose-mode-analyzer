# Installation Guide

## Quick Install

```bash
# 1. Clone the repository
git clone https://github.com/shaotian-cash/goose-mode-analyzer.git ~/recipes

# 2. Make scripts executable
chmod +x ~/recipes/*.sh ~/recipes/*.py

# 3. Set your Mode credentials
export MODE_TOKEN=your_mode_token
export MODE_SECRET=your_mode_secret

# 4. Test it
~/recipes/analyze-mode-report.sh "https://app.mode.com/cashapp/reports/35f8533657e9"
```

## Getting Mode Credentials

1. Log into Mode at https://app.mode.com
2. Click your profile → Account Settings
3. Navigate to **API Tokens**
4. Create a new token or use existing one
5. Copy the **Token** and **Secret**

## Permanent Setup (Optional)

Add credentials to your shell profile so they're always available:

```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'export MODE_TOKEN=your_token' >> ~/.zshrc
echo 'export MODE_SECRET=your_secret' >> ~/.zshrc
source ~/.zshrc
```

## Requirements

- **uv** - Python package runner (install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Mode API credentials** - Token and Secret
- **Python 3.8+** - Usually pre-installed on macOS

## Usage

### Method 1: Shell Script (Easiest)
```bash
~/recipes/analyze-mode-report.sh "MODE_URL"
```

### Method 2: Python Script
```bash
uv run ~/recipes/mode_analyzer_standalone.py "MODE_URL"
```

### Method 3: Goose Recipe
```bash
goose run --recipe ~/recipes/mode-table-extractor.yaml \
  --params mode_report_url=MODE_URL
```

## Troubleshooting

**Command not found: uv**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Permission denied**
```bash
chmod +x ~/recipes/*.sh ~/recipes/*.py
```

**MODE_TOKEN not set**
```bash
export MODE_TOKEN=your_token
export MODE_SECRET=your_secret
```

## Support

- 📖 Full documentation: [README.md](README.md)
- 🚀 Quick guide: [USAGE.md](USAGE.md)
- 🐛 Issues: https://github.com/shaotian-cash/goose-mode-analyzer/issues
