#!/bin/bash
# Quick wrapper for Mode Report Analyzer
# Usage: ./analyze-mode-report.sh <mode_url>

set -e

# Check if URL provided
if [ -z "$1" ]; then
    echo "Usage: $0 <mode_report_url>"
    echo ""
    echo "Example:"
    echo "  $0 https://app.mode.com/cashapp/reports/92b253c1af84"
    echo ""
    echo "Make sure MODE_TOKEN and MODE_SECRET are set:"
    echo "  export MODE_TOKEN=your_token"
    echo "  export MODE_SECRET=your_secret"
    exit 1
fi

# Check for credentials
if [ -z "$MODE_TOKEN" ] || [ -z "$MODE_SECRET" ]; then
    echo "❌ Error: MODE_TOKEN and MODE_SECRET must be set"
    echo ""
    echo "Set them with:"
    echo "  export MODE_TOKEN=your_token"
    echo "  export MODE_SECRET=your_secret"
    echo ""
    echo "Then run:"
    echo "  $0 $1"
    exit 1
fi

# Run the analyzer
echo "🔍 Analyzing Mode report..."
echo ""
uv run ~/recipes/mode_analyzer_standalone.py "$1"
