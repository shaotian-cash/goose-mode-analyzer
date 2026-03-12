# Mode Report Analyzer - Usage Guide

## TL;DR - Quick Usage

```bash
# 1. Set credentials (one time per session)
export MODE_TOKEN=bdd47c1a6dde
export MODE_SECRET=9d1aa419400e31a72fda4cbf

# 2. Analyze any Mode report
~/recipes/analyze-mode-report.sh "https://app.mode.com/cashapp/reports/REPORT_ID"
```

## Three Ways to Use

### Method 1: Simple Shell Script (Recommended)

```bash
export MODE_TOKEN=your_token MODE_SECRET=your_secret
~/recipes/analyze-mode-report.sh "https://app.mode.com/cashapp/reports/35f8533657e9"
```

### Method 2: Direct Python Script

```bash
export MODE_TOKEN=your_token MODE_SECRET=your_secret
uv run ~/recipes/mode_analyzer_standalone.py "https://app.mode.com/cashapp/reports/35f8533657e9"
```

### Method 3: Goose Recipe

```bash
export MODE_TOKEN=your_token MODE_SECRET=your_secret
goose run --recipe ~/recipes/mode-table-extractor.yaml \
  --params mode_report_url=https://app.mode.com/cashapp/reports/35f8533657e9
```

## Using with Goose Chat

Once you have the tool set up, you can use it directly in goose conversations:

```
You: Analyze the Mode report at https://app.mode.com/cashapp/reports/35f8533657e9

Goose: [runs the analyzer and shows you all queries and tables]
```

The tool will automatically:
1. Extract all SQL queries from the report
2. Parse each query to find table references
3. Generate a comprehensive markdown report
4. Save the results to a file

## What You Get

### Console Output
- Formatted markdown with all queries
- Tables referenced in each query
- Summary statistics

### File Output
- `mode_report_<REPORT_ID>.md` - Full analysis saved locally

### Example Summary
```
### Summary
**Total Queries:** 11
**Unique Tables:** 40

**All Tables Referenced:**
- `app_cash.health.labelbox_parse_w_customer_token`
- `JIRA_ANALYTICS.JIRA_REPORTING.FACT_TICKET_DETAILS`
- `JIRA_ANALYTICS.JIRA_REPORTING.CUSTOM_FIELDS`
... (37 more tables)
```

## Tips

1. **Save your credentials** in your shell profile (~/.zshrc or ~/.bashrc):
   ```bash
   export MODE_TOKEN=your_token
   export MODE_SECRET=your_secret
   ```

2. **URL formats** - All these work:
   - `https://app.mode.com/cashapp/reports/35f8533657e9`
   - `https://app.mode.com/cashapp/reports/35f8533657e9/details`
   - `https://app.mode.com/cashapp/reports/35f8533657e9/details/queries/c0c0ab2f7967`

3. **Batch processing** - Analyze multiple reports:
   ```bash
   for report in report1 report2 report3; do
     ~/recipes/analyze-mode-report.sh "https://app.mode.com/cashapp/reports/$report"
   done
   ```

## Integration with Your Workflow

### For tsk-29213 (Case Tests)

```bash
# 1. Set credentials
export MODE_TOKEN=bdd47c1a6dde MODE_SECRET=9d1aa419400e31a72fda4cbf

# 2. Analyze the test report
~/recipes/analyze-mode-report.sh "https://app.mode.com/cashapp/reports/35f8533657e9"

# 3. Review the output file
cat mode_report_35f8533657e9.md

# 4. Use the extracted tables for your tests
```

### Future Use

Whenever you need to analyze a Mode report:

1. Just paste the URL to goose
2. Goose will run the analyzer
3. You get all queries and tables instantly

No need to:
- Manually open Mode
- Copy-paste queries
- Parse SQL by hand
- Track down table references

## Files Created

```
~/recipes/
├── README.md                      # Full documentation
├── USAGE.md                       # This file
├── mode-table-extractor.yaml      # Goose recipe
├── mode_analyzer_standalone.py    # Main tool (recommended)
├── mode_report_analyzer.py        # Alternative version
├── analyze-mode-report.sh         # Convenience wrapper
├── mode-analyzer.sh               # Experimental MCP version
└── requirements.txt               # Python dependencies
```

## Next Steps

1. ✅ Tool is ready to use
2. ✅ Tested with your report
3. ✅ Found 11 queries and 40 tables
4. 🎯 Use it whenever you need Mode analysis
5. 🚀 Share with your team if useful

## Questions?

- Check `~/recipes/README.md` for detailed documentation
- Run with `--help` for usage info
- Ask goose to help you use it!
