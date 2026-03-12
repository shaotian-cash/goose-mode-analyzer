#!/usr/bin/env -S uvx --from requests python3
# /// script
# dependencies = ["requests"]
# ///
"""
Mode Report Analyzer for Goose
Extracts SQL queries and table references from Mode reports

Usage:
    uvx mode_analyzer_standalone.py <mode_report_url>
    
Environment Variables:
    MODE_TOKEN - Your Mode API token
    MODE_SECRET - Your Mode API secret
"""

import os
import re
import sys
import json
import requests
from urllib.parse import urlparse
from typing import List, Set, Tuple, Dict

class ModeReportAnalyzer:
    def __init__(self, token: str, secret: str):
        self.token = token
        self.secret = secret
        self.base_url = "https://app.mode.com/api"
        self.session = requests.Session()
        self.session.auth = (token, secret)
        
    def extract_report_info(self, url: str) -> Tuple[str, str]:
        """Extract workspace and report ID from Mode URL"""
        # Example: https://app.mode.com/cashapp/reports/35f8533657e9
        pattern = r'mode\.com/([^/]+)/reports/([^/]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    def get_report(self, workspace: str, report_id: str) -> Dict:
        """Fetch report details from Mode API"""
        url = f"{self.base_url}/{workspace}/reports/{report_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_queries(self, workspace: str, report_id: str) -> List[Dict]:
        """Fetch all queries from a report"""
        url = f"{self.base_url}/{workspace}/reports/{report_id}/queries"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('_embedded', {}).get('queries', [])
    
    def extract_tables_from_sql(self, sql: str) -> Set[str]:
        """Extract table references from SQL query"""
        if not sql:
            return set()
            
        tables = set()
        
        # Remove comments
        sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        
        # Patterns for FROM and JOIN clauses
        # Matches: schema.table, database.schema.table
        patterns = [
            # Three-part names: database.schema.table
            r'\b(?:FROM|JOIN)\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)\b',
            # Two-part names: schema.table
            r'\b(?:FROM|JOIN)\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+)\b',
            # Single names: table (with optional alias)
            r'\b(?:FROM|JOIN)\s+([a-zA-Z0-9_]+)\b(?:\s+(?:AS\s+)?[a-zA-Z0-9_]+)?',
        ]
        
        sql_keywords = {
            'SELECT', 'WHERE', 'GROUP', 'ORDER', 'HAVING', 'UNION', 
            'LIMIT', 'OFFSET', 'WITH', 'AS', 'ON', 'AND', 'OR', 'NOT',
            'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'CROSS', 'NATURAL',
            'EXISTS', 'IN', 'BETWEEN', 'LIKE', 'IS', 'NULL', 'CASE', 'WHEN',
            'THEN', 'ELSE', 'END', 'DISTINCT', 'ALL', 'ANY', 'SOME'
        }
        
        for pattern in patterns:
            matches = re.finditer(pattern, sql, re.IGNORECASE)
            for match in matches:
                table = match.group(1)
                # Skip SQL keywords
                if table.upper() not in sql_keywords:
                    tables.add(table)
        
        return tables
    
    def analyze_report(self, url: str) -> Dict:
        """Analyze a Mode report and extract all information"""
        workspace, report_id = self.extract_report_info(url)
        
        if not workspace or not report_id:
            raise ValueError(f"Could not parse Mode URL: {url}")
        
        # Fetch report details
        report = self.get_report(workspace, report_id)
        queries = self.get_queries(workspace, report_id)
        
        # Analyze queries
        all_tables = set()
        query_details = []
        
        for query in queries:
            query_name = query.get('name', 'Unnamed Query')
            query_token = query.get('token', '')
            raw_query = query.get('raw_query', '')
            
            tables = self.extract_tables_from_sql(raw_query)
            all_tables.update(tables)
            
            query_details.append({
                'name': query_name,
                'token': query_token,
                'sql': raw_query,
                'tables': sorted(tables)
            })
        
        return {
            'url': url,
            'workspace': workspace,
            'report_id': report_id,
            'report_name': report.get('name', 'Unknown'),
            'queries': query_details,
            'all_tables': sorted(all_tables)
        }
    
    def format_output(self, analysis: Dict) -> str:
        """Format analysis results as markdown"""
        output = []
        output.append("## Mode Report Analysis\n")
        output.append(f"**Report Name:** {analysis['report_name']}")
        output.append(f"**Report URL:** {analysis['url']}")
        output.append(f"**Workspace:** {analysis['workspace']}")
        output.append(f"**Report ID:** {analysis['report_id']}\n")
        
        output.append("### SQL Queries Found:\n")
        
        for i, query in enumerate(analysis['queries'], 1):
            output.append(f"#### Query {i}: {query['name']}\n")
            output.append("```sql")
            output.append(query['sql'])
            output.append("```\n")
            
            if query['tables']:
                output.append("**Tables Referenced:**")
                for table in query['tables']:
                    output.append(f"- `{table}`")
                output.append("")
        
        output.append("### Summary\n")
        output.append(f"**Total Queries:** {len(analysis['queries'])}")
        output.append(f"**Unique Tables:** {len(analysis['all_tables'])}\n")
        
        if analysis['all_tables']:
            output.append("**All Tables Referenced:**")
            for table in analysis['all_tables']:
                output.append(f"- `{table}`")
        
        return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: uvx mode_analyzer_standalone.py <mode_report_url>")
        print("\nExample:")
        print("  uvx mode_analyzer_standalone.py https://app.mode.com/cashapp/reports/92b253c1af84")
        print("\nEnvironment variables required:")
        print("  MODE_TOKEN - Your Mode API token")
        print("  MODE_SECRET - Your Mode API secret")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Get credentials from environment
    token = os.environ.get('MODE_TOKEN')
    secret = os.environ.get('MODE_SECRET')
    
    if not token or not secret:
        print("Error: MODE_TOKEN and MODE_SECRET environment variables must be set")
        print("\nSet them with:")
        print("  export MODE_TOKEN=your_token")
        print("  export MODE_SECRET=your_secret")
        sys.exit(1)
    
    try:
        analyzer = ModeReportAnalyzer(token, secret)
        analysis = analyzer.analyze_report(url)
        output = analyzer.format_output(analysis)
        print(output)
        
        # Also save to file
        output_file = f"mode_report_{analysis['report_id']}.md"
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"\n✅ Analysis saved to: {output_file}")
        
    except requests.exceptions.HTTPError as e:
        print(f"Error: Failed to fetch Mode report: {e}")
        print("\nPlease check:")
        print("1. Your MODE_TOKEN and MODE_SECRET are correct")
        print("2. You have access to this report")
        print("3. The report URL is valid")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
