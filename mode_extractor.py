#!/usr/bin/env python3
"""
Mode Table Extractor
Extracts SQL queries and table references from Mode reports
"""

import os
import re
import sys
import json
from urllib.parse import urlparse

def extract_report_info(url):
    """Extract workspace and report ID from Mode URL"""
    # Example: https://app.mode.com/cashapp/reports/35f8533657e9/details/queries/c0c0ab2f7967
    pattern = r'mode\.com/([^/]+)/reports/([^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2)
    return None, None

def extract_tables_from_sql(sql):
    """Extract table references from SQL query"""
    tables = set()
    
    # Remove comments
    sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    
    # Pattern for FROM and JOIN clauses
    # Matches: FROM schema.table, JOIN schema.table, etc.
    patterns = [
        r'\bFROM\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)?)',
        r'\bJOIN\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)?)',
        r'\bFROM\s+([a-zA-Z0-9_]+)',
        r'\bJOIN\s+([a-zA-Z0-9_]+)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, sql, re.IGNORECASE)
        for match in matches:
            table = match.group(1)
            # Skip common SQL keywords
            if table.upper() not in ['SELECT', 'WHERE', 'GROUP', 'ORDER', 'HAVING', 'UNION']:
                tables.add(table)
    
    return sorted(tables)

def main():
    if len(sys.argv) < 2:
        print("Usage: python mode_extractor.py <mode_report_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    workspace, report_id = extract_report_info(url)
    
    if not workspace or not report_id:
        print(f"Error: Could not parse Mode URL: {url}")
        sys.exit(1)
    
    print(f"## Mode Report Analysis\n")
    print(f"**Report URL:** {url}")
    print(f"**Workspace:** {workspace}")
    print(f"**Report ID:** {report_id}\n")
    
    # Check for Mode credentials
    mode_token = os.environ.get('MODE_TOKEN')
    mode_secret = os.environ.get('MODE_SECRET')
    
    if not mode_token or not mode_secret:
        print("⚠️  **Mode credentials not found**")
        print("\nTo use this tool, you need to:")
        print("1. Set MODE_TOKEN and MODE_SECRET environment variables")
        print("2. Or manually provide the SQL queries\n")
        print("Please copy the SQL queries from the Mode report and paste them here.")
        sys.exit(1)
    
    # TODO: Use Mode API or MCP server to fetch queries
    print("### Fetching report data from Mode API...")
    print("\n⚠️  **Mode API integration pending**")
    print("\nFor now, please:")
    print("1. Open the report in Mode")
    print("2. Copy each SQL query")
    print("3. Paste them here for analysis")

if __name__ == "__main__":
    main()
