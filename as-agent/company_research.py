#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import re

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
JSON_OUTPUT_DIR = Path(__file__).parent / "outputs" / "json"

def setup():
    """Setup the environment and check for required API keys."""
    # Create outputs directory if it doesn't exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Create JSON outputs directory
    JSON_OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    
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
        candidate_file = Path("context-data/candidate/candidate.json")
        if not candidate_file.exists():
            print("Warning: Candidate data file not found")
            return None
            
        with open(candidate_file, 'r') as f:
            candidate_data = json.load(f)
            
        if candidate_data and isinstance(candidate_data, list) and len(candidate_data) > 0:
            return candidate_data[0]  # Return the first candidate object
        else:
            print("Warning: Invalid candidate data format")
            return None
    except Exception as e:
        print(f"Error loading candidate data: {e}")
        return None

def search_perplexity(query, company_name):
    """Search using Perplexity API."""
    if not PERPLEXITY_API_KEY:
        print("Perplexity API key not found, skipping this search method.")
        return None
    
    print(f"Searching for information about {company_name} using Perplexity...")
    print(f"Query: {query}")
    print("Sending request to Perplexity API...")
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "sonar-pro",  # Using the Sonar Pro model for research
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful research assistant. Provide detailed, accurate information with citations when available."
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }
    
    try:
        print("Waiting for Perplexity API response...")
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            print(f"Error: Perplexity API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        response.raise_for_status()
        result = response.json()
        
        print("Received response from Perplexity API")
        
        # Extract the text from the response
        if "choices" in result and len(result["choices"]) > 0:
            text = result["choices"][0]["message"]["content"]
            print(f"Successfully extracted content from Perplexity response (length: {len(text)} characters)")
            return {"text": text, "citations": result.get("citations", [])}
        else:
            print("Error: Could not extract content from Perplexity response")
            print(f"Response structure: {result.keys()}")
            return None
    except Exception as e:
        print(f"Error searching Perplexity: {e}")
        print("Check your API key and network connection")
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
        print("Sending request to OpenRouter API...")
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
        "limit": 20  # Increased limit to get more results for filtering
    }
    
    try:
        print("Sending request to Hunter.io API...")
        response = requests.get(
            "https://api.hunter.io/v2/domain-search",
            params=params
        )
        
        if response.status_code != 200:
            print(f"Error: Hunter.io API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and "emails" in result["data"]:
            email_count = len(result["data"]["emails"])
            print(f"Found {email_count} email addresses for {company_domain}")
            return result
        else:
            print(f"No emails found for {company_domain}")
            return None
    except Exception as e:
        print(f"Error searching Hunter.io: {e}")
        print("Check your API key and network connection")
        return None

def extract_domain_from_website(website):
    """Extract domain from website URL and normalize it."""
    if not website:
        print("Warning: Empty website URL provided")
        return None
    
    try:
        # Normalize the URL by adding https:// if not present
        if not isinstance(website, str):
            print(f"Warning: Non-string website URL provided: {type(website)}")
            website = str(website)
            
        if not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        # Extract domain
        domain = website.lower()
        for prefix in ["https://", "http://", "www."]:
            if domain.startswith(prefix):
                domain = domain[len(prefix):]
        
        # Remove path and query parameters
        domain = domain.split("/")[0]
        
        # Remove any trailing dots
        domain = domain.rstrip('.')
        
        # Validate domain has at least one dot (e.g., example.com)
        if '.' not in domain:
            print(f"Warning: Domain '{domain}' may not be valid - missing TLD")
        
        return domain
    except Exception as e:
        print(f"Error extracting domain from website: {e}")
        return None

def filter_career_emails(emails_data):
    """Filter emails to find career-related, founder, and generic/non-generic addresses."""
    if not emails_data or "data" not in emails_data:
        return [], [], [], []
    
    career_emails = []
    founder_emails = []
    generic_emails = []
    non_generic_emails = []
    
    for email in emails_data["data"]["emails"]:
        # Get values with safe defaults
        email_address = email.get("value", "")
        position = email.get("position", "")
        position = position.lower() if position else ""
        
        first_name = email.get("first_name", "")
        first_name = first_name.lower() if first_name else ""
        
        last_name = email.get("last_name", "")
        last_name = last_name.lower() if last_name else ""
        
        department = email.get("department", "")
        department = department.lower() if department else ""
        
        type_value = email.get("type", "")
        
        # Check for generic emails
        if type_value == "generic":
            generic_emails.append(email)
            # Only add up to 3 generic emails
            if len(generic_emails) >= 3:
                generic_emails = generic_emails[:3]
        
        # Check for non-generic emails
        elif type_value != "generic" and first_name and last_name:
            non_generic_emails.append(email)
            # Only add up to 3 non-generic emails
            if len(non_generic_emails) >= 3:
                non_generic_emails = non_generic_emails[:3]
        
        # Check for career-related emails
        career_keywords = ["career", "recruit", "hr", "hiring", "talent", "job", "human resource"]
        if (position and any(keyword in position for keyword in career_keywords)) or \
           (department and any(keyword in department for keyword in career_keywords)) or \
           (email_address and any(keyword in email_address.lower() for keyword in career_keywords)):
            career_emails.append(email)
        
        # Check for founder emails
        founder_keywords = ["founder", "ceo", "chief executive", "president", "owner"]
        if position and any(keyword in position for keyword in founder_keywords):
            founder_emails.append(email)
    
    return career_emails, founder_emails, generic_emails, non_generic_emails

def generate_research_queries(company_name, additional_info):
    """Generate research queries for the company."""
    queries = [
        {
            "title": "Company Overview",
            "query": f"Detailed company information for {company_name} {additional_info if additional_info else ''} including size, headquarters, founding date, and description"
        },
        {
            "title": "Remote Work Policies",
            "query": f"Remote work policies and culture at {company_name} {additional_info if additional_info else ''}, including location restrictions and time zone expectations"
        },
        {
            "title": "Leadership and Funding",
            "query": f"Leadership team and funding history of {company_name} {additional_info if additional_info else ''}, including VCs and backers"
        },
        {
            "title": "Career Opportunities",
            "query": f"Career opportunities and hiring process at {company_name} {additional_info if additional_info else ''}, including salary transparency and compensation strategy"
        },
        {
            "title": "Company Culture and Values",
            "query": f"Company values, mission, and culture at {company_name} {additional_info if additional_info else ''}"
        },
        {
            "title": "Market Positioning",
            "query": f"Market position and competitors of {company_name} {additional_info if additional_info else ''}, including industry trends and business model"
        },
        {
            "title": "Company Reputation",
            "query": f"Any controversies or notable achievements related to {company_name} {additional_info if additional_info else ''}, including employee reviews and public perception"
        }
    ]
    return queries

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

def extract_location_restrictions(research_data):
    """Extract location restrictions from research data.
    Returns a dictionary with location restriction details.
    """
    # In a real implementation, you would parse the research data to extract location restrictions
    # This is a simplified implementation for demonstration purposes
    
    # Default values
    restrictions = {
        "has_restrictions": False,
        "restricted_to": [],
        "excluded_regions": [],
        "time_zone_requirements": "",
        "restriction_level": "none",  # none, low, medium, high
        "restriction_description": "No location restrictions found."
    }
    
    # Parse research data to find location restrictions
    # This would involve analyzing the text for mentions of location requirements
    
    if not research_data:
        print("Warning: No research data provided for location restriction extraction")
        return restrictions
    
    # Example logic (in a real implementation, this would be more sophisticated)
    for data in research_data:
        if not isinstance(data, dict):
            continue
            
        text = ""
        try:
            if "text" in data and data["text"]:  # Perplexity API format
                text = data["text"].lower() if isinstance(data["text"], str) else str(data["text"]).lower()
            elif "choices" in data and data["choices"] and len(data["choices"]) > 0:  # OpenRouter API format
                content = data["choices"][0].get("message", {}).get("content")
                if content:
                    text = content.lower() if isinstance(content, str) else str(content).lower()
            else:
                continue
                
            # Check for common restriction phrases
            if "us only" in text or "united states only" in text:
                restrictions["has_restrictions"] = True
                if "United States" not in restrictions["restricted_to"]:
                    restrictions["restricted_to"].append("United States")
                restrictions["restriction_level"] = "high"
            
            if "eu only" in text or "europe only" in text:
                restrictions["has_restrictions"] = True
                if "European Union" not in restrictions["restricted_to"]:
                    restrictions["restricted_to"].append("European Union")
                restrictions["restriction_level"] = "high"
                
            if "north america" in text and "only" in text:
                restrictions["has_restrictions"] = True
                if "North America" not in restrictions["restricted_to"]:
                    restrictions["restricted_to"].append("North America")
                restrictions["restriction_level"] = "high"
                
            # Check for time zone requirements
            if "time zone" in text and ("overlap" in text or "hours" in text):
                # Extract time zone information (simplified)
                if "est" in text or "edt" in text:
                    restrictions["time_zone_requirements"] = "Eastern Time (ET)"
                    restrictions["has_restrictions"] = True
                    restrictions["restriction_level"] = max(restrictions["restriction_level"], "medium")
                elif "pst" in text or "pdt" in text:
                    restrictions["time_zone_requirements"] = "Pacific Time (PT)"
                    restrictions["has_restrictions"] = True
                    restrictions["restriction_level"] = max(restrictions["restriction_level"], "medium")
                elif "cet" in text or "central european" in text:
                    restrictions["time_zone_requirements"] = "Central European Time (CET)"
                    restrictions["has_restrictions"] = True
                    restrictions["restriction_level"] = max(restrictions["restriction_level"], "medium")
        except Exception as e:
            print(f"Error processing research data for location restrictions: {e}")
            continue
    
    # Update restriction description based on findings
    if restrictions["has_restrictions"]:
        description_parts = []
        
        if restrictions["restricted_to"]:
            description_parts.append(f"Restricted to: {', '.join(restrictions['restricted_to'])}")
            
        if restrictions["excluded_regions"]:
            description_parts.append(f"Excluded regions: {', '.join(restrictions['excluded_regions'])}")
            
        if restrictions["time_zone_requirements"]:
            description_parts.append(f"Time zone requirements: {restrictions['time_zone_requirements']}")
            
        restrictions["restriction_description"] = " | ".join(description_parts)
    
    return restrictions

def check_location_compatibility(location_restrictions, candidate_data):
    """Check if candidate's location is compatible with company restrictions.
    Returns a tuple of (is_compatible, warning_message).
    """
    if not location_restrictions["has_restrictions"] or not candidate_data:
        return True, ""
        
    # Extract candidate location information
    candidate_location = candidate_data.get("personal_information", {}).get("location", "")
    candidate_timezone = candidate_data.get("personal_information", {}).get("timezone", "")
    
    if not candidate_location and not candidate_timezone:
        return True, "Warning: Cannot determine location compatibility. Candidate location information is missing."
    
    # Check for region compatibility
    is_compatible = True
    warning_reasons = []
    
    if location_restrictions["restricted_to"]:
        # Simple region check (in a real implementation, this would be more sophisticated)
        is_region_match = False
        for region in location_restrictions["restricted_to"]:
            if region.lower() in candidate_location.lower():
                is_region_match = True
                break
                
        if not is_region_match:
            is_compatible = False
            warning_reasons.append(f"Company is restricted to {', '.join(location_restrictions['restricted_to'])}, but candidate is in {candidate_location}")
    
    if location_restrictions["excluded_regions"]:
        for region in location_restrictions["excluded_regions"]:
            if region.lower() in candidate_location.lower():
                is_compatible = False
                warning_reasons.append(f"Company excludes {region}, but candidate is in {candidate_location}")
    
    # Check time zone compatibility (simplified)
    if location_restrictions["time_zone_requirements"] and candidate_timezone:
        # This is a very simplified check - in reality, you'd need more sophisticated time zone comparison
        if location_restrictions["time_zone_requirements"].lower() not in candidate_timezone.lower():
            is_compatible = False
            warning_reasons.append(f"Company requires {location_restrictions['time_zone_requirements']} overlap, but candidate is in {candidate_timezone}")
    
    warning_message = ""
    if not is_compatible:
        warning_message = "⚠️ **LOCATION COMPATIBILITY WARNING**: " + " | ".join(warning_reasons)
    
    return is_compatible, warning_message

def generate_cover_letter(company_name, interest_reason, research_data):
    """Generate a cover letter for the candidate."""
    # Load candidate data
    candidate_data = load_candidate_data()
    if not candidate_data:
        print("Warning: Could not load candidate data for cover letter")
        # Fallback to generic cover letter
        return generate_generic_cover_letter(company_name, interest_reason, research_data)
    
    # Extract candidate information
    name = candidate_data.get("personal_information", {}).get("name", "")
    email = candidate_data.get("personal_information", {}).get("public_email", "")
    website = candidate_data.get("personal_information", {}).get("website", "")
    resume = candidate_data.get("personal_information", {}).get("resume", "")
    objective = candidate_data.get("career_goals_and_preferences", {}).get("objective", "")
    ideal_roles = candidate_data.get("career_goals_and_preferences", {}).get("ideal_roles", [])
    
    # Extract skills from candidate data
    communication_skills = candidate_data.get("skills_and_expertise", {}).get("communication_and_strategy", [])
    ai_skills = candidate_data.get("skills_and_expertise", {}).get("ai_and_technical", [])
    soft_skills = candidate_data.get("skills_and_expertise", {}).get("soft_skills", [])
    
    # Extract a brief company description from research data
    company_description = extract_company_description(company_name, research_data)
    
    # Generate cover letter using OpenRouter or Perplexity
    prompt = f"""
    Generate a concise cover letter for {name} applying to {company_name}.
    
    IMPORTANT: The cover letter MUST be between 100-120 words total. This is a strict requirement.
    
    About the company: {company_description}
    
    Why the candidate is interested: {interest_reason}
    
    Candidate's career objective: {objective}
    
    Ideal roles the candidate is seeking: {', '.join(ideal_roles[:3])}
    
    Key skills to highlight: 
    - Communication and strategy: {', '.join(communication_skills[:3])}
    - AI and technical: {', '.join(ai_skills[:3])}
    - Soft skills: {', '.join(soft_skills[:3])}
    
    The cover letter should be professional, personalized to the company, and highlight relevant experience and skills.
    It MUST be between 100-120 words total and include a proper email signature with the candidate's actual name, website, and resume link.
    Make it concise, impactful, and focused on the most relevant skills and experiences.
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
    Generate three concise, attention-grabbing email subject lines for {name}'s job application to {company_name}.
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
1. {subject_lines[0] if len(subject_lines) > 0 else f"Application for [Position] - {name}"}
2. {subject_lines[1] if len(subject_lines) > 1 else f"Experienced Professional Interested in {company_name}"}
3. {subject_lines[2] if len(subject_lines) > 2 else f"Connecting About Opportunities at {company_name}"}

### Cover Letter:

{cover_letter_text}

Best regards,

{name}
{website}
{resume}
"""
    
    return cover_letter_section

def generate_generic_cover_letter(company_name, interest_reason, research_data):
    """Generate a generic cover letter when candidate data is not available."""
    # Extract a brief company description from research data
    company_description = extract_company_description(company_name, research_data)
    
    # Generate cover letter using OpenRouter or Perplexity
    prompt = f"""
    Generate a concise cover letter for a candidate applying to {company_name}.
    
    IMPORTANT: The cover letter MUST be between 100-120 words total. This is a strict requirement.
    
    About the company: {company_description}
    
    Why the candidate is interested: {interest_reason}
    
    The cover letter should be professional, personalized to the company, and highlight relevant experience and skills.
    It MUST be between 100-120 words total and include a proper email signature with name, website, and resume link.
    Make it concise, impactful, and focused on the most relevant skills and experiences.
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
    
    # Format the cover letter section
    cover_letter_section = f"""
## Cover Letter for {company_name}

### Cover Letter:

{cover_letter_text}

Best regards,
[Your Name]
[Your Website]
[Your Resume]
"""
    
    return cover_letter_section

def extract_company_description(company_name, research_data):
    """Extract a brief company description from research data."""
    # This is a simplified implementation
    # In a real implementation, you would use NLP to extract relevant information
    
    company_description = f"{company_name} is a company that appears to be remote-friendly."
    
    # Try to extract a better description from research data
    if research_data and len(research_data) > 0:
        for data in research_data:
            if isinstance(data, dict):
                text = ""
                if "text" in data:
                    text = data["text"]
                elif "choices" in data and len(data["choices"]) > 0:
                    text = data["choices"][0]["message"]["content"]
                
                if text and len(text) > 0:
                    # Look for sentences that describe what the company does
                    sentences = text.split(". ")
                    for sentence in sentences:
                        if company_name in sentence and ("is " in sentence.lower() or "provides" in sentence.lower() or "offers" in sentence.lower()):
                            return sentence + "."
    
    return company_description

def generate_report(company_name, company_url, additional_info, research_data, email_data, interest_reason=None):
    """Generate the final research report."""
    # Process research data to extract key information
    # In a real implementation, you would use NLP to summarize and extract insights
    
    # Format the company info section
    company_info = f"# {company_name} Research Report\n\n"
    if additional_info:
        company_info += f"**Additional Info:** {additional_info}\n\n"
    
    if company_url:
        company_info += f"**Company URL:** {company_url}\n\n"
    
    # Extract location restrictions
    location_restrictions = extract_location_restrictions(research_data)
    
    # Add location compatibility information
    location_section = generate_location_section(location_restrictions)
    
    # Format the research data section
    research_section = "## Research Data\n\n"
    
    # Clean up the research data for better presentation
    queries = generate_research_queries(company_name, additional_info)
    for i, data in enumerate(research_data, 1):
        # Get the title from the queries list if available, otherwise use a default title
        if i <= len(queries) and hasattr(queries[i-1], 'get') and queries[i-1].get('title'):
            section_title = queries[i-1]['title']
        else:
            section_title = f"Research Item {i}"
            
        research_section += f"### {section_title}\n\n"
        
        if isinstance(data, dict):
            # Format text content
            if "text" in data:
                research_section += data["text"] + "\n\n"
            elif "choices" in data and len(data["choices"]) > 0:
                research_section += data["choices"][0]["message"]["content"] + "\n\n"
            
            # Add citations if available
            if "citations" in data and data["citations"]:
                research_section += "**Sources:**\n\n"
                for citation in data["citations"]:
                    research_section += f"- {citation}\n"
                research_section += "\n"
        else:
            research_section += str(data) + "\n\n"
    
    # Format the contact information section
    contact_section = ""
    if email_data:
        career_emails, founder_emails, generic_emails, non_generic_emails = email_data
        
        contact_section = "## Contact Information\n\n"
        
        if career_emails:
            contact_section += "### Career-related Emails\n\n"
            for email in career_emails:
                name_part = f"{email.get('first_name', '')} {email.get('last_name', '')}".strip()
                position_part = email.get('position', '')
                if name_part and position_part:
                    contact_section += f"- {email.get('value')} ({name_part}, {position_part})\n"
                elif name_part:
                    contact_section += f"- {email.get('value')} ({name_part})\n"
                else:
                    contact_section += f"- {email.get('value')}\n"
            contact_section += "\n"
        
        if founder_emails:
            contact_section += "### Founder Emails\n\n"
            for email in founder_emails:
                name_part = f"{email.get('first_name', '')} {email.get('last_name', '')}".strip()
                position_part = email.get('position', '')
                if name_part and position_part:
                    contact_section += f"- {email.get('value')} ({name_part}, {position_part})\n"
                elif name_part:
                    contact_section += f"- {email.get('value')} ({name_part})\n"
                else:
                    contact_section += f"- {email.get('value')}\n"
            contact_section += "\n"
        
        if generic_emails:
            contact_section += "### Generic Emails\n\n"
            for email in generic_emails:
                contact_section += f"- {email.get('value')}\n"
            contact_section += "\n"
        
        if non_generic_emails:
            contact_section += "### Team Member Emails\n\n"
            for email in non_generic_emails:
                name_part = f"{email.get('first_name', '')} {email.get('last_name', '')}".strip()
                position_part = email.get('position', '')
                if name_part and position_part:
                    contact_section += f"- {email.get('value')} ({name_part}, {position_part})\n"
                elif name_part:
                    contact_section += f"- {email.get('value')} ({name_part})\n"
                else:
                    contact_section += f"- {email.get('value')}\n"
            contact_section += "\n"
    
    # Generate a cover letter if interest reason is provided
    cover_letter_section = ""
    if interest_reason:
        cover_letter_section = generate_cover_letter(company_name, interest_reason, research_data)
    
    # Combine all sections into the final report
    report = company_info + location_section + contact_section + research_section
    
    # Add the cover letter if available
    if cover_letter_section:
        report += "\n" + cover_letter_section
    
    # Save location restrictions as JSON
    save_location_restrictions_json(company_name, location_restrictions, company_url)
    
    return report

def save_location_restrictions_json(company_name, location_restrictions, company_url=None):
    """Save location restrictions as JSON for later use."""
    # Sanitize company name for filename
    safe_name = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in company_name)
    safe_name = safe_name.replace(' ', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp}_location.json"
    
    output_path = JSON_OUTPUT_DIR / filename
    
    if company_url:
        location_restrictions["company_url"] = company_url
    
    with open(output_path, 'w') as f:
        json.dump(location_restrictions, f, indent=2)
    
    print(f"Location restrictions saved to {output_path}")

def generate_location_section(location_restrictions):
    """Generate the location section of the report."""
    location_section = "## Location Restrictions\n\n"
    if location_restrictions["has_restrictions"]:
        location_section += f"**Restrictions:** {location_restrictions['restriction_description']}\n\n"
    else:
        location_section += "**No location restrictions found.**\n\n"
    
    return location_section

def save_report(company_name, report, location_data=None):
    """Save the report to a file."""
    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Clean company name for filename
    clean_name = re.sub(r'[^\w\s-]', '', company_name).strip().replace(' ', '_')
    
    # Create company-specific subfolder within outputs directory
    company_folder = os.path.join("outputs", clean_name)
    os.makedirs(company_folder, exist_ok=True)
    
    # Create date-based subfolder within company folder
    date_folder = os.path.join(company_folder, datetime.now().strftime("%Y%m%d"))
    os.makedirs(date_folder, exist_ok=True)
    
    # Create JSON output directory if it doesn't exist
    json_output_dir = os.path.join(date_folder, "json")
    os.makedirs(json_output_dir, exist_ok=True)
    
    # Create filename
    filename = f"{clean_name}_{timestamp}.md"
    filepath = os.path.join(date_folder, filename)
    
    # Save the markdown report
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    
    # Generate PDF from markdown
    try:
        from markdown_pdf import MarkdownPdf
        
        pdf_filename = f"{clean_name}_{timestamp}.pdf"
        pdf_filepath = os.path.join(date_folder, pdf_filename)
        
        # Convert markdown to PDF
        print(f"Generating PDF report: {pdf_filepath}")
        md_pdf = MarkdownPdf()
        md_pdf.convert_markdown_to_pdf(filepath, pdf_filepath)
        print(f"PDF report generated successfully")
    except Exception as e:
        print(f"Error generating PDF: {e}")
        print("PDF generation skipped. Please install required dependencies with: pip install markdown-pdf")
    
    # Save location data as JSON if provided
    if location_data:
        json_filename = f"{clean_name}_{timestamp}_location.json"
        json_filepath = os.path.join(json_output_dir, json_filename)
        
        with open(json_filepath, "w", encoding="utf-8") as f:
            json.dump(location_data, f, indent=2)
    
    return filepath

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
    
    # Get company URL
    print("\nCompany URL (e.g., example.com or https://example.com):")
    print("This will be used to look up email addresses via Hunter.io")
    company_url = input("> ").strip()
    
    # Get additional info (optional)
    print("\nAdditional identifying information (optional, press Enter to skip):")
    print("This helps disambiguate companies with similar names.")
    print("Example: For 'Mercury', you might add 'banking startup'")
    additional_info = input("> ").strip()
    
    # Ask if user wants to generate a cover letter
    print("\nWould you like to generate a cover letter? (yes/no):")
    print("Cover letters are optional and can be personalized if you provide a reason for interest.")
    generate_cover_letter = input("> ").strip().lower()
    
    interest_reason = None
    if generate_cover_letter in ['yes', 'y']:
        # Get reason for interest (for cover letter)
        print("\nWhy are you interested in this company?")
        print("This will be used to personalize your cover letter.")
        interest_reason = input("> ").strip()
    
    return company_name, company_url, additional_info, interest_reason

def main():
    """Main function to run the company research agent."""
    # Print welcome message
    print_welcome()
    
    # Setup environment
    setup()
    
    # Get user input
    company_name, company_url, additional_info, interest_reason = get_user_input()
    
    print(f"\nStarting research on {company_name}...")
    if additional_info:
        print(f"Additional information provided: {additional_info}")
    if company_url:
        print(f"Company URL provided: {company_url}")
    
    # Generate research queries
    print("\nGenerating research queries...")
    queries = generate_research_queries(company_name, additional_info)
    print(f"Generated {len(queries)} research queries")
    
    # Collect research data
    research_data = []
    
    # Try Perplexity first, fall back to OpenRouter if needed
    if PERPLEXITY_API_KEY:
        print("\nUsing Perplexity API for research...")
        for i, query in enumerate(queries, 1):
            print(f"\nProcessing query {i} of {len(queries)}...")
            result = search_perplexity(query["query"], company_name)
            if result:
                research_data.append(result)
                print(f"Successfully added research data from query {i}")
            else:
                print(f"No data retrieved for query {i}")
            
            if i < len(queries):
                print("Waiting before next query to avoid rate limiting...")
                time.sleep(1)  # Avoid rate limiting
    elif OPENROUTER_API_KEY:
        print("\nUsing OpenRouter API for research...")
        for i, query in enumerate(queries, 1):
            print(f"\nProcessing query {i} of {len(queries)}...")
            result = search_openrouter(query["query"], company_name)
            if result:
                research_data.append(result)
                print(f"Successfully added research data from query {i}")
            else:
                print(f"No data retrieved for query {i}")
            
            if i < len(queries):
                print("Waiting before next query to avoid rate limiting...")
                time.sleep(1)  # Avoid rate limiting
    
    print(f"\nResearch complete. Collected data from {len(research_data)} queries")
    
    # Extract company website from research data if not provided by user
    company_website = company_url
    if not company_website:
        print("\nExtracting company website from research data...")
        company_website = extract_company_website(research_data)
        if company_website:
            print(f"Found company website: {company_website}")
        else:
            print("Could not extract company website from research data")
    
    # If we couldn't find the website, try a direct search
    if not company_website:
        print("\nAttempting direct search for company website...")
        website_query = f"What is the official website URL for {company_name} {additional_info if additional_info else ''}?"
        if PERPLEXITY_API_KEY:
            website_result = search_perplexity(website_query, company_name)
            # In a real implementation, you would parse the result to extract the website
        elif OPENROUTER_API_KEY:
            website_result = search_openrouter(website_query, company_name)
            # In a real implementation, you would parse the result to extract the website
    
    # Look up emails if we have a domain
    email_data = None
    if company_url:
        print(f"\nExtracting domain from URL: {company_url}")
        domain = extract_domain_from_website(company_url)
        if domain:
            print(f"Extracted domain: {domain}")
            hunter_results = search_hunter_io(domain)
            if hunter_results:
                print("Processing email results...")
                career_emails, founder_emails, generic_emails, non_generic_emails = filter_career_emails(hunter_results)
                print(f"Found {len(career_emails)} career emails, {len(founder_emails)} founder emails, "
                      f"{len(generic_emails)} generic emails, and {len(non_generic_emails)} non-generic emails")
                email_data = (career_emails, founder_emails, generic_emails, non_generic_emails)
            else:
                print("No email data found")
        else:
            print(f"Could not extract domain from URL: {company_url}")
    
    # Generate and save the report
    print("\nGenerating report...")
    report = generate_report(company_name, company_url, additional_info, research_data, email_data, interest_reason)
    print("Report generated successfully")
    
    print("\nSaving report to file...")
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
