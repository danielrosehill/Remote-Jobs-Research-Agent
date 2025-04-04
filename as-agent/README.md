# Company Research Agent

This interactive Python script helps you research companies with a focus on their remote work policies, culture, and other important details. It generates comprehensive reports using tools like Perplexity, OpenRouter, and Hunter.io.

## Features

- Interactive CLI that guides you through the research process
- Generates detailed company research reports in Markdown format
- Focuses on remote work policies, culture, and practices
- Searches for career-related and founder email addresses
- Automatically generates personalized cover letters for remote-friendly companies
- Creates suggested email subject lines for job applications
- Saves reports in the `outputs` folder with timestamps
- Flexible search using either Perplexity API or OpenRouter API

## Setup

1. Install the required dependencies:
   ```
   pip install python-dotenv requests
   ```

2. Copy the `.env.example` file to `.env` in the root directory:
   ```
   cp ../.env.example ../.env
   ```

3. Edit the `.env` file and add your API keys:
   - HUNTER_API_KEY: Get from [Hunter.io](https://hunter.io/)
   - PERPLEXITY_API_KEY: Get from [Perplexity API](https://www.perplexity.ai/api)
   - OPENROUTER_API_KEY: Get from [OpenRouter](https://openrouter.ai/)

   Note: You need at least Hunter.io API key and either Perplexity or OpenRouter API key.

## Usage

Simply run the script without any arguments:

```bash
python company_research.py
```

The script will guide you through the process with interactive prompts:
1. Enter the company name you want to research
2. Optionally provide additional identifying information for disambiguation
3. Share why you're interested in the company (used for cover letter generation)
4. The script will then conduct research and generate a report

## Output

The script generates a detailed report in Markdown format and saves it in the `outputs` directory. The filename includes the company name and a timestamp.

The report follows a structured template that includes:
- Company details (size, headquarters, founding date)
- People and funding information
- Market positioning
- Remote work policies and culture
- Career opportunities and contact information
- Summary with a remote commitment lead score

For remote-friendly companies, the report also includes:
- A personalized cover letter (max 120 words)
- Three suggested email subject lines for your application
- Professional email signature with your name, website, and resume link

## Candidate Data

The script uses candidate information from `context-data/candidate/example.json` to personalize the cover letter. This file contains:
- Personal information (name, email, website, resume link)
- Career goals and preferences
- Professional experience
- Skills and expertise

You can modify this file to include your own information for more personalized cover letters.

## Customization

You can modify the template file at `../config-files/templates/as-md/remote-general.md` to change the structure and content of the generated reports.
