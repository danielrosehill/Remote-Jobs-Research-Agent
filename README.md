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

## Usage

Each system prompt includes space for users to describe their specific requirements in detail, allowing the research to be tailored to their particular needs. For example:
- Target industries
- Preferred company sizes
- Geographic preferences
- Specific remote work arrangements
- Other job-seeking criteria

## Getting Started

1. Choose the appropriate prompt file based on your needs:
   - `prompts/basic.md` for general company research
   - `prompts/remote-general.md` for remote work assessment
   - `prompts/remote-ex-isr.md` for Israel-specific remote work research

2. Copy the entire system prompt section into your LLM or research tool

3. For applications requiring structured data, use the JSON schema provided at the bottom of each prompt file

4. Customize the prompt with your specific requirements

5. Deploy with your preferred LLM or research tool

6. Review and refine the generated company research reports

## Contributing

Contributions to improve templates, system prompts, or suggest new workflow ideas are welcome!
