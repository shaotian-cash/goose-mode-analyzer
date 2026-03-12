#!/bin/bash
# Mode Report Analyzer
# Extracts SQL queries and tables from Mode reports using MCP server

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <mode_report_url>"
    echo "Example: $0 https://app.mode.com/cashapp/reports/92b253c1af84"
    exit 1
fi

MODE_URL="$1"

# Check for credentials
if [ -z "$MODE_TOKEN" ] || [ -z "$MODE_SECRET" ]; then
    echo "Error: MODE_TOKEN and MODE_SECRET environment variables must be set"
    echo ""
    echo "Example:"
    echo "  export MODE_TOKEN=your_token"
    echo "  export MODE_SECRET=your_secret"
    echo "  $0 $MODE_URL"
    exit 1
fi

echo "Analyzing Mode Report: $MODE_URL"
echo ""

# Extract report ID from URL
REPORT_ID=$(echo "$MODE_URL" | grep -oP 'reports/\K[^/]+' | head -1)
WORKSPACE=$(echo "$MODE_URL" | grep -oP 'mode\.com/\K[^/]+' | head -1)

echo "Workspace: $WORKSPACE"
echo "Report ID: $REPORT_ID"
echo ""

# Use MCP Mode server to fetch report
echo "Fetching report data via MCP Mode server..."
echo ""

# Run the MCP server and interact with it
# Note: This requires the mcp_mode package to be installed
uvx mcp_mode@latest <<EOF
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_report",
    "arguments": {
      "workspace": "$WORKSPACE",
      "report_id": "$REPORT_ID"
    }
  }
}
EOF
