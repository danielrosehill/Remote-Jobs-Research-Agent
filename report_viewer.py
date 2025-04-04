#!/usr/bin/env python3
import os
import re
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for
from markdown import markdown
import bleach
from bleach.sanitizer import ALLOWED_TAGS, ALLOWED_ATTRIBUTES

# Create new sets from the frozen sets
allowed_tags = set(ALLOWED_TAGS)
allowed_attributes = dict(ALLOWED_ATTRIBUTES)

# Add additional HTML tags that we want to allow
allowed_tags.update(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'br', 'pre', 'code', 'blockquote', 'table', 'thead', 'tbody', 'tr', 'th', 'td'])
allowed_attributes.update({
    'table': ['class'],
    'th': ['scope', 'style'],
    'td': ['style'],
    'code': ['class'],
    'a': ['href', 'title', 'target', 'rel']
})

app = Flask(__name__)

# Constants
OUTPUT_DIR = Path(__file__).parent / "as-agent" / "outputs"
JSON_OUTPUT_DIR = Path(__file__).parent / "as-agent" / "outputs" / "json"

def get_reports(sort_by='date', reverse=True):
    """Get all reports from the outputs directory."""
    reports = []
    
    if not OUTPUT_DIR.exists():
        return reports
    
    for file in OUTPUT_DIR.glob('*.md'):
        # Extract company name and timestamp from filename
        # Expected format: CompanyName_YYYYMMDD_HHMMSS.md
        match = re.match(r'(.+)_(\d{8}_\d{6})\.md', file.name)
        if match:
            company_name = match.group(1).replace('_', ' ')
            timestamp_str = match.group(2)
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                
                # Check if there's a corresponding location restrictions JSON file
                location_json_path = JSON_OUTPUT_DIR / f"{file.stem}_location.json"
                location_restrictions = None
                if location_json_path.exists():
                    try:
                        with open(location_json_path, 'r') as f:
                            location_restrictions = json.load(f)
                    except Exception as e:
                        print(f"Error loading location restrictions: {e}")
                
                reports.append({
                    'filename': file.name,
                    'company_name': company_name,
                    'timestamp': timestamp,
                    'path': str(file),
                    'location_restrictions': location_restrictions
                })
            except ValueError:
                # If timestamp parsing fails, use file creation time
                reports.append({
                    'filename': file.name,
                    'company_name': file.stem.replace('_', ' '),
                    'timestamp': datetime.fromtimestamp(file.stat().st_ctime),
                    'path': str(file)
                })
    
    # Sort reports by date or company name
    if sort_by == 'date':
        reports.sort(key=lambda x: x['timestamp'], reverse=reverse)
    else:  # sort by company name
        reports.sort(key=lambda x: x['company_name'].lower(), reverse=reverse)
    
    return reports

def parse_report_content(content):
    """Parse the report content to extract sections."""
    sections = {}
    
    # Extract company name
    company_name_match = re.search(r'# \*\*Company Research For: (.+?)\*\*', content)
    if company_name_match:
        sections['company_name'] = company_name_match.group(1)
    
    # Extract location compatibility warning
    warning_match = re.search(r'⚠️ \*\*LOCATION COMPATIBILITY WARNING\*\*: (.*?)\n\n', content)
    if warning_match:
        sections['location_warning'] = warning_match.group(1)
    
    # Extract email section
    email_section_match = re.search(r'\| \*\*Careers Emails\*\* \| (.*?)\n\|', content, re.DOTALL)
    if email_section_match:
        email_text = email_section_match.group(1).strip()
        sections['emails'] = email_text
    
    # Extract cover letter if it exists
    cover_letter_match = re.search(r'## Cover Letter for (.*?)\n\n.*?### Cover Letter:\n\n(.*?)Best regards,', content, re.DOTALL)
    if cover_letter_match:
        sections['cover_letter_company'] = cover_letter_match.group(1)
        sections['cover_letter'] = cover_letter_match.group(2).strip()
    
    # Extract remote score
    remote_score_match = re.search(r'\*\*Remote Commitment Lead Score:\*\*\s+(\d+)/10', content)
    if remote_score_match:
        sections['remote_score'] = remote_score_match.group(1)
    
    # Extract location restrictions
    location_restrictions_match = re.search(r'\| \*\*Location Restrictions\?\*\* \| (.*?)\n\|', content, re.DOTALL)
    if location_restrictions_match:
        sections['location_restrictions'] = location_restrictions_match.group(1).strip()
    
    return sections

def extract_emails(content):
    """Extract email addresses from the content."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, content)

def get_location_restrictions_json(filename):
    """Get location restrictions JSON for a report."""
    base_name = filename.rsplit('.', 1)[0]  # Remove extension
    json_path = JSON_OUTPUT_DIR / f"{base_name}_location.json"
    
    if json_path.exists():
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading location restrictions: {e}")
    
    return None

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'date')
    reverse = request.args.get('order', 'desc') == 'desc'
    reports = get_reports(sort_by, reverse)
    return render_template('index.html', reports=reports, sort_by=sort_by, order='desc' if reverse else 'asc')

@app.route('/report/<filename>')
def view_report(filename):
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        return redirect(url_for('index'))
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse the content to extract sections
    sections = parse_report_content(content)
    
    # Get location restrictions JSON
    location_restrictions = get_location_restrictions_json(filename)
    
    # Convert markdown to HTML
    html_content = markdown(content, extensions=['tables', 'fenced_code'])
    
    # Sanitize HTML to prevent XSS
    html_content = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attributes)
    
    # Extract emails for the copyable section
    emails = extract_emails(content)
    
    # Get all reports for the sidebar
    all_reports = get_reports()
    
    return render_template(
        'report.html', 
        filename=filename,
        company_name=sections.get('company_name', 'Unknown Company'),
        html_content=html_content,
        emails=emails,
        sections=sections,
        location_restrictions=location_restrictions,
        reports=all_reports
    )

@app.route('/api/reports')
def api_reports():
    sort_by = request.args.get('sort', 'date')
    reverse = request.args.get('order', 'desc') == 'desc'
    reports = get_reports(sort_by, reverse)
    return jsonify(reports)

if __name__ == '__main__':
    # Create outputs directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    JSON_OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
