# Remote Jobs Research Agent

## Overview
This repository provides a specialized agent designed to assist remote job seekers in researching companies. The agent focuses on gathering comprehensive information about companies, with particular emphasis on their remote work policies, culture, and hiring practices.

## Purpose
Finding detailed information about a company's remote work policies can be challenging and time-consuming. This project aims to:

1. Streamline the research process for remote job seekers
2. Provide structured, information-rich reports on companies (in both Markdown and PDF formats)
3. Help job seekers make informed decisions about potential employers
4. Assess companies' openness to remote work and any geographic restrictions

## Repository Structure

### Prompt Files
The repository contains three comprehensive prompt files, each containing both the system prompt and JSON schema:

- **[Basic Company Research](/prompts/basic.md)**: General company research without specific focus
- **[Remote Work Focus](/prompts/remote-general.md)**: Detailed assessment of remote work policies and culture
- **[Remote Work for Israel](/prompts/remote-ex-isr.md)**: Specialized research for remote job seekers in Israel

Each prompt file includes:
1. A complete system prompt with instructions
2. A markdown template for the research report
3. A JSON schema that can be used for structured data processing

## Recommended Tooling

### Email Retrieval
- [Hunter.io](https://hunter.io): For retrieving company email addresses and contact information

### Email Integration
- Gmail or other email service MCPs for sending follow-up communications

### Real-time Research
For enhanced research capabilities, consider using:
- [Perplexity Sonar](https://www.perplexity.ai)
- [Perplexity Deep Research](https://www.perplexity.ai)
- Regular LLMs augmented with tools like:
  - [Tavily](https://tavily.com)
  - Other augmented search pipelines

## Multi-Agent Workflow Ideas

This repository can serve as the foundation for more complex workflows:

1. **Initial Deep Research Agent**: Uses the prompts in this repository to gather comprehensive company information
2. **Human-in-the-Loop Layer**: For verification and additional context
3. **Email Generation Agent**: Creates personalized outreach based on research findings

This workflow is designed not for mass-volume spammy outreach, but to provide decisive, information-rich retrievals for job seekers targeting specific types of companies.

## Getting Started

1. Clone this repository and navigate to the project directory

2. Create a `.env` file based on the provided `.env.example` and add your API keys:
   ```
   HUNTER_API_KEY=your_hunter_api_key
   PERPLEXITY_API_KEY=your_perplexity_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Choose the appropriate prompt file based on your needs:
   - `prompts/basic.md` for general company research
   - `prompts/remote-general.md` for remote work assessment
   - `prompts/remote-ex-isr.md` for Israel-specific remote work research

5. **Running the Research Agent**:
   
   You can run the research agent using the provided wrapper script:
   ```bash
   ./run_research.sh
   ```
   
   This will start an interactive session where you can enter a company name and additional information.
   
   The generated reports will be saved in the `as-agent/outputs/[Company_Name]/[Date]` directory as both Markdown and PDF files with timestamps.

6. **Viewing Reports** (Optional):
   
   To browse and interact with your generated reports in a web interface:
   ```bash
   ./run_report_viewer.sh
   ```
   
   This will start a local web server at http://localhost:5000 where you can:
   - View all generated reports
   - Copy email addresses with a single click
   - Copy cover letters with a single click
   - Sort reports by date or company name

7. **Using Components Independently**:
   
   - **Research Agent Only**: If you only want to generate reports without using the viewer, just run the research agent and access the Markdown files directly in the `as-agent/outputs` directory.
   
   - **Report Viewer Only**: If you already have generated reports and just want to view them, you can run the report viewer without generating new reports.
   
   - **Custom Integration**: The modular design allows you to integrate these components into your own workflows as needed.

## Key Features

### Organized Research Sections
Research data is now organized into meaningful sections:
- Company Overview
- Remote Work Policies
- Leadership and Funding
- Career Opportunities
- Company Culture and Values
- Market Positioning
- Company Reputation

### Optional Cover Letter Generation
- During the research process, you'll be asked if you want to generate a cover letter
- Cover letters are entirely optional and only generated when explicitly requested
- If you choose to generate a cover letter, you'll be prompted to provide your reason for interest in the company

### PDF Report Generation
- Reports are automatically generated in both Markdown and PDF formats
- PDF files provide a professional format for saving and sharing research
- PDF generation uses the `markdown-pdf` package, which is installed automatically
- If PDF generation fails, the script will continue and provide instructions for manual installation

### Location Compatibility Tracking
- The agent extracts and tracks location restrictions from company data
- Structured JSON storage of location restrictions for programmatic access
- Compatibility checking between company restrictions and candidate location
- Visual warnings for location incompatibility in the report viewer

### Improved File Organization
- Reports are now organized in a hierarchical structure:
  - `outputs/[Company_Name]/[Date]/[Company_Name]_[Timestamp].md`
  - `outputs/[Company_Name]/[Date]/[Company_Name]_[Timestamp].pdf`
  - `outputs/[Company_Name]/[Date]/json/[Company_Name]_[Timestamp]_location.json`
- This organization makes it easier to find reports for specific companies and dates

## Report Viewer

1. **Installation**: The report viewer requires Flask and a few other Python packages. These dependencies are included in the main `requirements.txt` file.

2. **Starting the Viewer**:
   ```bash
   ./run_report_viewer.sh
   ```
   This script will install the necessary dependencies and start the Flask server.

3. **Features**:
   - Browse all generated reports in a user-friendly web interface
   - View reports organized by date or alphabetically
   - Copy email addresses with a single click
   - Copy cover letters with a single click (if generated)
   - View remote work scores with visual indicators
   - Responsive design for desktop and mobile viewing
   - Dedicated location information tab with color-coded restriction indicators

4. **Accessing the Viewer**:
   Once started, the report viewer will be available at http://localhost:5000

## Contributing

Contributions to improve prompts, system functionality, or suggest new workflow ideas are welcome!
