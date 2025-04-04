#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Constants
OUTPUT_DIR = Path(__file__).parent / "outputs"
TEMPLATE_PATH = Path(__file__).parent.parent / "config-files" / "templates" / "as-md" / "remote-general.md"
CANDIDATE_DATA_PATH = Path(__file__).parent.parent / "context-data" / "candidate" / "example.json"

def setup():
    """Setup the environment and check for required API keys."""
    # Create outputs directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Check for required API keys
    missing_keys = []
    if not HUNTER_API_KEY:
        missing_keys.append("HUNTER_API_KEY")
    if not PERPLEXITY_API_KEY and not OPENROUTER_API_KEY:
        missing_keys.append("PERPLEXITY_API_KEY or OPENROUTER_API_KEY")
    
    if missing_keys:
        print(f"Error: Missing required API keys: {', '.join(missing_keys)}")
        print("Please add them to your .env file.")
        sys.exit(1)
    
    # Check if template file exists
    if not TEMPLATE_PATH.exists():
        print(f"Error: Template file not found at {TEMPLATE_PATH}")
        sys.exit(1)
        
    # Check if candidate data exists
    if not CANDIDATE_DATA_PATH.exists():
        print(f"Warning: Candidate data file not found at {CANDIDATE_DATA_PATH}")
        print("Cover letter generation will be disabled.")

def load_template():
    """Load the report template."""
    with open(TEMPLATE_PATH, 'r') as f:
        return f.read()

def load_candidate_data():
    """Load candidate data from JSON file."""
    try:
        with open(CANDIDATE_DATA_PATH, 'r') as f:
            data = json.load(f)
            return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    except Exception as e:
        print(f"Error loading candidate data: {e}")
        return None

def search_perplexity(query, company_name):
    """Search using Perplexity API."""
    if not PERPLEXITY_API_KEY:
        print("Perplexity API key not found, skipping this search method.")
        return None
    
    print(f"Searching for information about {company_name} using Perplexity...")
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": query,
        "options": {
            "include_citations": True
        }
    }
    
    try:
        response = requests.post(
            "https://api.perplexity.ai/search",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching Perplexity: {e}")
        return None

def search_openrouter(query, company_name):
    """Search using OpenRouter API."""
    if not OPENROUTER_API_KEY:
        print("OpenRouter API key not found, skipping this search method.")
        return None
    
    print(f"Searching for information about {company_name} using OpenRouter...")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "anthropic/claude-3-opus:beta",  # Using Claude 3 Opus for deep research
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching OpenRouter: {e}")
        return None

def search_hunter_io(company_domain):
    """Search for email addresses using Hunter.io API."""
    if not HUNTER_API_KEY:
        print("Hunter.io API key not found, skipping email lookup.")
        return None
    
    print(f"Looking up email addresses for {company_domain} using Hunter.io...")
    
    params = {
        "domain": company_domain,
        "api_key": HUNTER_API_KEY,
        "limit": 10
    }
    
    try:
        response = requests.get(
            "https://api.hunter.io/v2/domain-search",
            params=params
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error searching Hunter.io: {e}")
        return None

def extract_domain_from_website(website):
    """Extract domain from website URL."""
    if not website:
        return None
    
    # Remove protocol and www if present
    domain = website.lower()
    for prefix in ["https://", "http://", "www."]:
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    
    # Remove path and query parameters
    domain = domain.split("/")[0]
    
    return domain

def filter_career_emails(emails_data):
    """Filter emails to find career-related and founder addresses."""
    if not emails_data or "data" not in emails_data:
        return [], []
    
    career_emails = []
    founder_emails = []
    
    for email in emails_data["data"]["emails"]:
        email_address = email.get("value", "")
        position = email.get("position", "").lower()
        first_name = email.get("first_name", "").lower()
        last_name = email.get("last_name", "").lower()
        department = email.get("department", "").lower()
        
        # Check for career-related emails
        career_keywords = ["career", "recruit", "hr", "hiring", "talent", "job", "human resource"]
        if any(keyword in position.lower() for keyword in career_keywords) or \
           any(keyword in department.lower() for keyword in career_keywords) or \
           any(keyword in email_address.lower() for keyword in career_keywords):
            career_emails.append(email)
        
        # Check for founder emails
        founder_keywords = ["founder", "ceo", "chief executive", "president", "owner"]
        if any(keyword in position.lower() for keyword in founder_keywords):
            founder_emails.append(email)
    
    return career_emails, founder_emails

def generate_research_queries(company_name, additional_info):
    """Generate research queries for the company."""
    base_queries = [
        f"Detailed company information for {company_name} {additional_info if additional_info else ''} including size, headquarters, founding date, and description",
        f"Remote work policies and culture at {company_name} {additional_info if additional_info else ''}, including location restrictions and time zone expectations",
        f"Leadership team and funding history of {company_name} {additional_info if additional_info else ''}, including VCs and backers",
        f"Career opportunities and hiring process at {company_name} {additional_info if additional_info else ''}, including salary transparency and compensation strategy",
        f"Company values, mission, and culture at {company_name} {additional_info if additional_info else ''}, especially regarding remote work",
        f"Competitors of {company_name} {additional_info if additional_info else ''} and how they compare in terms of remote work policies",
        f"Any controversies or red flags related to {company_name} {additional_info if additional_info else ''}, especially regarding treatment of employees"
    ]
    return base_queries

def extract_company_website(research_data):
    """Extract company website from research data."""
    # This is a simplified implementation - in a real scenario, you would parse the research data
    # to find the company's website
    
    # For demonstration purposes, let's assume we can find it in the research data
    # In a real implementation, you would use NLP or regex to extract this information
    
    # If website can't be found, return None
    return None

def is_remote_friendly(research_data):
    """Determine if the company is remote-friendly based on research data."""
    # This is a simplified implementation - in a real scenario, you would analyze the research data
    # to determine if the company is remote-friendly
    
    # For demonstration purposes, let's assume we can determine this from the research data
    # In a real implementation, you would use NLP or regex to extract this information
    
    # For now, we'll just return True for testing purposes
    # In a real implementation, you would return True or False based on the analysis
    return True

def generate_cover_letter(company_name, company_description, interest_reason, candidate_data):
    """Generate a cover letter for the candidate."""
    if not candidate_data:
        return None
    
    # Extract candidate information
    name = candidate_data.get("personal_information", {}).get("name", "")
    email = candidate_data.get("personal_information", {}).get("public_email", "")
    website = candidate_data.get("personal_information", {}).get("website", "")
    resume = candidate_data.get("personal_information", {}).get("resume", "")
    objective = candidate_data.get("career_goals_and_preferences", {}).get("objective", "")
    ideal_roles = candidate_data.get("career_goals_and_preferences", {}).get("ideal_roles", [])
    skills = candidate_data.get("skills_and_expertise", {})
    
    # Generate cover letter using OpenRouter or Perplexity
    prompt = f"""
    Generate a concise cover letter (maximum 120 words) for {name} applying to {company_name}.
    
    About the company: {company_description}
    
    Why the candidate is interested: {interest_reason}
    
    Candidate's career objective: {objective}
    
    Ideal roles the candidate is seeking: {', '.join(ideal_roles[:3])}
    
    Key skills to highlight: 
    - Communication and strategy: {', '.join(skills.get('communication_and_strategy', [])[:3])}
    - AI and technical: {', '.join(skills.get('ai_and_technical', [])[:3])}
    - Soft skills: {', '.join(skills.get('soft_skills', [])[:3])}
    
    The cover letter should be professional, personalized to the company, and highlight relevant experience and skills.
    It should be no more than 120 words and include a proper email signature with name, website, and resume link.
    """
    
    # Generate using available API
    cover_letter_text = ""
    if OPENROUTER_API_KEY:
        result = search_openrouter(prompt, company_name)
        if result and "choices" in result and len(result["choices"]) > 0:
            cover_letter_text = result["choices"][0]["message"]["content"]
    elif PERPLEXITY_API_KEY:
        result = search_perplexity(prompt, company_name)
        if result and "text" in result:
            cover_letter_text = result["text"]
    
    # Generate subject lines
    subject_lines_prompt = f"""
    Generate three concise, attention-grabbing email subject lines for a job application to {company_name}.
    The subject lines should be professional but stand out in a recruiter's inbox.
    Each should be no more than 8 words.
    Format as a numbered list with just the subject lines, nothing else.
    """
    
    subject_lines = []
    if OPENROUTER_API_KEY:
        result = search_openrouter(subject_lines_prompt, company_name)
        if result and "choices" in result and len(result["choices"]) > 0:
            subject_lines_text = result["choices"][0]["message"]["content"]
            subject_lines = [line.strip().replace("1. ", "").replace("2. ", "").replace("3. ", "") 
                            for line in subject_lines_text.split("\n") if line.strip()][:3]
    elif PERPLEXITY_API_KEY:
        result = search_perplexity(subject_lines_prompt, company_name)
        if result and "text" in result:
            subject_lines_text = result["text"]
            subject_lines = [line.strip().replace("1. ", "").replace("2. ", "").replace("3. ", "") 
                            for line in subject_lines_text.split("\n") if line.strip()][:3]
    
    # Format the cover letter section
    cover_letter_section = f"""
## Cover Letter for {company_name}

### Suggested Subject Lines:
1. {subject_lines[0] if len(subject_lines) > 0 else "Application for [Position] - {name}"}
2. {subject_lines[1] if len(subject_lines) > 1 else "Experienced Professional Interested in {company_name}"}
3. {subject_lines[2] if len(subject_lines) > 2 else "Connecting About Opportunities at {company_name}"}

### Cover Letter:

{cover_letter_text}

Best regards,

{name}
{website}
{resume}
"""
    
    return cover_letter_section

def generate_report(company_name, additional_info, research_data, email_data, interest_reason=None):
    """Generate the final research report."""
    template = load_template()
    
    # Replace placeholders with actual data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = template.replace("{Company-Name}", company_name)
    report = report.replace("{timestamp}", timestamp)
    
    # In a real implementation, you would parse the research_data to fill in all the template fields
    # This would involve extracting specific information for each section
    
    # For the careers emails section, we can use the email_data
    careers_emails_section = ""
    if email_data:
        career_emails, founder_emails = email_data
        
        if career_emails:
            careers_emails_section += "**Career-related emails:**\n\n"
            for email in career_emails:
                careers_emails_section += f"- {email.get('value')} ({email.get('first_name')} {email.get('last_name')}, {email.get('position')})\n"
        
        if founder_emails:
            careers_emails_section += "\n**Founder emails:**\n\n"
            for email in founder_emails:
                careers_emails_section += f"- {email.get('value')} ({email.get('first_name')} {email.get('last_name')}, {email.get('position')})\n"
    
    # Replace the careers emails placeholder
    # In a real implementation, you would locate this in the template and replace it appropriately
    
    # Check if company is remote-friendly and add cover letter if it is
    if is_remote_friendly(research_data):
        print("Company appears to be remote-friendly. Generating cover letter...")
        candidate_data = load_candidate_data()
        if candidate_data:
            # Extract a brief company description from research data
            # This is a simplified implementation
            company_description = f"{company_name} is a company that appears to be remote-friendly."
            
            cover_letter = generate_cover_letter(
                company_name, 
                company_description, 
                interest_reason, 
                candidate_data
            )
            
            if cover_letter:
                # Add cover letter to the end of the report
                report += "\n\n" + cover_letter
    
    return report

def save_report(company_name, report):
    """Save the report to a file."""
    # Sanitize company name for filename
    safe_name = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in company_name)
    safe_name = safe_name.replace(' ', '_')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp}.md"
    
    output_path = OUTPUT_DIR / filename
    
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"Report saved to {output_path}")
    return output_path

def print_welcome():
    """Print welcome message and instructions."""
    print("\n" + "=" * 80)
    print("COMPANY RESEARCH AGENT".center(80))
    print("=" * 80)
    print("\nThis tool will research a company and generate a comprehensive report")
    print("focusing on remote work policies, culture, and other important details.")
    print("\nThe report will be saved in the 'outputs' folder.")
    print("\n" + "-" * 80)

def get_user_input():
    """Get company name and additional info from user interactively."""
    print("\nPlease provide the following information:")
    
    # Get company name with validation
    while True:
        company_name = input("\nCompany Name: ").strip()
        if company_name:
            break
        print("Company name cannot be empty. Please try again.")
    
    # Get additional info (optional)
    print("\nAdditional identifying information (optional, press Enter to skip):")
    print("This helps disambiguate companies with similar names.")
    print("Example: For 'Mercury', you might add 'banking startup'")
    additional_info = input("> ").strip()
    
    # Get reason for interest (for cover letter)
    print("\nWhy are you interested in this company? (optional, press Enter to skip)")
    print("This will be used to personalize your cover letter if the company is remote-friendly.")
    interest_reason = input("> ").strip()
    
    return company_name, additional_info, interest_reason

def main():
    """Main function to run the company research agent."""
    # Print welcome message
    print_welcome()
    
    # Setup environment
    setup()
    
    # Get user input
    company_name, additional_info, interest_reason = get_user_input()
    
    print(f"\nStarting research on {company_name}...")
    if additional_info:
        print(f"Additional information provided: {additional_info}")
    
    # Generate research queries
    queries = generate_research_queries(company_name, additional_info)
    
    # Collect research data
    research_data = []
    
    # Try Perplexity first, fall back to OpenRouter if needed
    if PERPLEXITY_API_KEY:
        for query in queries:
            result = search_perplexity(query, company_name)
            if result:
                research_data.append(result)
            time.sleep(1)  # Avoid rate limiting
    elif OPENROUTER_API_KEY:
        for query in queries:
            result = search_openrouter(query, company_name)
            if result:
                research_data.append(result)
            time.sleep(1)  # Avoid rate limiting
    
    # Extract company website from research data
    company_website = extract_company_website(research_data)
    
    # If we couldn't find the website, try a direct search
    if not company_website:
        website_query = f"What is the official website URL for {company_name} {additional_info if additional_info else ''}?"
        if PERPLEXITY_API_KEY:
            website_result = search_perplexity(website_query, company_name)
            # In a real implementation, you would parse the result to extract the website
        elif OPENROUTER_API_KEY:
            website_result = search_openrouter(website_query, company_name)
            # In a real implementation, you would parse the result to extract the website
    
    # Look up emails if we have a domain
    email_data = None
    if company_website:
        domain = extract_domain_from_website(company_website)
        if domain:
            hunter_results = search_hunter_io(domain)
            if hunter_results:
                career_emails, founder_emails = filter_career_emails(hunter_results)
                email_data = (career_emails, founder_emails)
    
    # Generate and save the report
    print("\nGenerating report...")
    report = generate_report(company_name, additional_info, research_data, email_data, interest_reason)
    report_path = save_report(company_name, report)
    
    print("\n" + "=" * 80)
    print(f"Research completed for {company_name}.")
    print(f"Report saved to {report_path}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nResearch interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
