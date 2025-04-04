# Company Research Agent Template

## Overview
This repository provides building blocks for creating deep research agents specifically designed to assist remote job seekers in researching companies. The agents focus on gathering comprehensive information about companies, with particular emphasis on their remote work policies, culture, and hiring practices.

## Purpose
Finding detailed information about a company's remote work policies can be challenging and time-consuming. This project aims to:

1. Streamline the research process for remote job seekers
2. Provide structured, information-rich reports on companies
3. Help job seekers make informed decisions about potential employers
4. Assess companies' openness to remote work and any geographic restrictions

## Repository Structure

### System Prompts
The repository contains several variations of system prompts:

- **All-in-one versions**: Complete prompts that include both instructions and templates
- **Split versions**: Separate files for instructions and templates
- **JSON array versions**: Structured data format for each prompt variation

### Templates
Templates are provided in two formats:

- **Markdown templates** (`/templates/as-md/`): Human-readable format
- **JSON templates** (`/templates/json/`): Structured data format for programmatic use

Each template has multiple variations:
- Basic company research
- General remote work assessment
- Specialized templates (e.g., for specific regions like Israel)

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

1. **Initial Deep Research Agent**: Uses the templates in this repository to gather comprehensive company information
2. **Human-in-the-Loop Layer**: For verification and additional context
3. **Email Generation Agent**: Creates personalized outreach based on research findings

This workflow is designed not for mass-volume spammy outreach, but to provide decisive, information-rich retrievals for job seekers targeting specific types of companies.

## Usage

Each system prompt includes space for users to describe their specific requirements in detail, allowing the research to be tailored to their particular needs. For example:
- Target industries
- Preferred company sizes
- Geographic preferences
- Specific remote work arrangements
- Other job-seeking criteria

## Getting Started

1. Choose the appropriate system prompt version based on your needs
2. Customize the prompt with your specific requirements
3. Deploy with your preferred LLM or research tool
4. Review and refine the generated company research reports

## Contributing

Contributions to improve templates, system prompts, or suggest new workflow ideas are welcome!
