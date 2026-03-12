# Mode Report Analyzer for Goose 🦆

Extract SQL queries and table references from Mode reports automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

A tool for [Goose](https://github.com/block/goose) that analyzes Mode Analytics reports and extracts:
- All SQL queries
- Table references and dependencies
- Data lineage information

Perfect for documentation, auditing, and understanding complex Mode reports.

## Quick Start

```bash
# Install
git clone https://github.com/shaotian-cash/goose-mode-analyzer.git ~/recipes

# Set credentials
export MODE_TOKEN=your_token MODE_SECRET=your_secret

# Analyze a report
~/recipes/analyze-mode-report.sh "https://app.mode.com/workspace/reports/REPORT_ID"
```

📖 **[Full Installation Guide](INSTALL.md)** | 🚀 **[Usage Examples](USAGE.md)**

---

## Mode Report Analyzer

Extract SQL queries and table references from Mode reports.

### Quick Start

```bash
# Set your Mode credentials (do this once per session)
export MODE_TOKEN=your_token_here
export MODE_SECRET=your_secret_here

# Analyze a Mode report
uv run ~/recipes/mode_analyzer_standalone.py "https://app.mode.com/cashapp/reports/REPORT_ID"
```

### Using with Goose Recipe

```bash
goose run --recipe ~/recipes/mode-table-extractor.yaml \
  --params mode_report_url=https://app.mode.com/cashapp/reports/REPORT_ID
```

### What It Does

1. **Connects to Mode API** using your credentials
2. **Fetches all queries** from the specified report
3. **Extracts table references** from each SQL query
4. **Generates a report** with:
   - All SQL queries with syntax highlighting
   - Tables referenced in each query
   - Summary of total queries and unique tables
   - Complete list of all tables used

### Output

The tool generates:
- **Console output** - Formatted markdown report
- **File output** - `mode_report_<REPORT_ID>.md` saved in current directory

### Example Output

```markdown
## Mode Report Analysis

**Report Name:** BIT Performance & Capacity Measurement
**Report URL:** https://app.mode.com/cashapp/reports/35f8533657e9
**Workspace:** cashapp
**Report ID:** 35f8533657e9

### SQL Queries Found:

#### Query 1: wow_changes
```sql
SELECT ...
FROM app_cash.health.labelbox_parse_w_customer_token
...
```

**Tables Referenced:**
- `app_cash.health.labelbox_parse_w_customer_token`
- `JIRA_ANALYTICS.JIRA_REPORTING.FACT_TICKET_DETAILS`

### Summary
**Total Queries:** 11
**Unique Tables:** 40
```

### Files

- `mode_analyzer_standalone.py` - Main analyzer script (standalone with dependencies)
- `mode_report_analyzer.py` - Alternative version (requires requests library)
- `mode-table-extractor.yaml` - Goose recipe definition
- `mode-analyzer.sh` - Shell wrapper (experimental)
- `requirements.txt` - Python dependencies

### Getting Mode Credentials

1. Log into Mode at https://app.mode.com
2. Go to your account settings
3. Navigate to API Tokens
4. Create a new token or use existing one
5. Copy the token and secret

### Troubleshooting

**Error: MODE_TOKEN and MODE_SECRET environment variables must be set**
- Make sure you've exported both variables in your current shell session

**Error: Failed to fetch Mode report**
- Check that your credentials are correct
- Verify you have access to the report
- Ensure the report URL is valid

**Error: Could not parse Mode URL**
- URL should be in format: `https://app.mode.com/WORKSPACE/reports/REPORT_ID`
- Remove any `/details/queries/...` suffixes if present (they're optional)

## Future Enhancements

- [ ] Add support for Mode charts and visualizations
- [ ] Extract data lineage information
- [ ] Support for private/shared reports
- [ ] Batch processing of multiple reports
- [ ] Integration with data catalog tools
