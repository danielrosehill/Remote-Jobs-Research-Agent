```json
{
  "type": "object",
  "properties": {
    "Remote Commitment Lead Score": {
      "type": "integer",
      "description": "A score out of 10 assessing the company's commitment to remote work."
    },
    "Company Details": {
      "type": "object",
      "properties": {
        "Company Name": {
          "type": "string",
          "description": "The name of the company."
        },
        "Company Size": {
          "type": "string",
          "description": "The company's approximate size according to headcount: <10 = micro, <100 = small, 100-999 = medium, 1000+ = large"
        },
        "Parent Company": {
          "type": "string",
          "description": "If the company is a subsidiary, list the parent organization or other relevant ties."
        },
        "Founded": {
          "type": "integer",
          "description": "The year when the company was founded."
        },
        "Description": {
          "type": "string",
          "description": "A short description of the company and what it does."
        },
        "Headquarters Location": {
          "type": "string",
          "description": "The company's official headquarters (city, country). For fully-remote companies, this may be just a nominal location."
        },
        "Other Locations": {
          "type": "string",
          "description": "Physical offices if any. For fully-remote companies, list the approximate geographical distribution of the workforce, if available."
        }
      },
      "required": [
        "Company Name",
        "Company Size",
        "Founded",
        "Description",
        "Headquarters Location"
      ]
    },
    "People And Funding": {
      "type": "object",
      "properties": {
        "Key People": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "The names of the key people associated with the company. Focus on those who champion remote work, if identifiable."
        },
        "VCs And Backers": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of venture capital firms and backers if publicly available. Note any backers that publicly support remote work initiatives."
        },
        "Funding History": {
          "type": "string",
          "description": "Details about the company's funding history. Has funding been explicitly allocated toward remote infrastructure or initiatives?"
        }
      },
      "required": [
        "Key People"
      ]
    },
    "Market Positioning": {
      "type": "object",
      "properties": {
        "Differentiation": {
          "type": "string",
          "description": "What distinguishes the company's products and its philosophy from others in a similar space? Is remote work part of their value proposition (e.g., providing remote collaboration tools)?"
        },
        "Vision": {
          "type": "string",
          "description": "Attempt to retrieve information in which the company or its leadership describes its broad strategic vision, especially for the current calendar year. Does their vision incorporate remote work as a core component?"
        },
        "Competitive Landscape": {
          "type": "string",
          "description": "Who are the company's main competitors and how do they distinguish themselves from them? How do their remote work policies compare to those competitors?"
        }
      },
      "required": [
        "Differentiation",
        "Competitive Landscape"
      ]
    },
    "Careers": {
      "type": "object",
      "properties": {
        "Remote Friendly?": {
          "type": "string",
          "description": "Analysis of the company's approach to remote work. Include explicit policies, observed practices, caveats, and supporting evidence (links, screenshots)."
        },
        "Remote Work Culture Assessment": {
          "type": "string",
          "enum": ["mature", "developing", "non-existent"],
          "description": "Assess the maturity and quality of their remote work culture. Consider asynchronous communication, documentation practices, remote team-building activities, inclusivity in virtual meetings, and leadership support for remote employees."
        },
        "Location Restrictions?": {
          "type": "string",
          "description": "List all location restrictions for remote employees. E.g., 'Must be located in US,' 'Must be within +/- 3 hours of CET,' 'Open to EMEA,' 'Excludes California,' etc. If no restrictions are explicitly stated, note that, but continue to look for implicit restrictions elsewhere (e.g. time overlap needed for meetings)"
        },
        "Salary Transparency": {
          "type": "string",
          "enum": ["Yes", "No", "Partial", "Varies by role"],
           "description": "Is the company transparent about salary ranges in their job postings?"
        },
        "Global Compensation Strategy?": {
          "type": "string",
          "description": "Determine whether the company has a defined global compensation strategy or if salary is determined on a case to case basis leading to inequalities."
        },
        "Time Zone Expectations?": {
          "type": "string",
          "description": "Document explicit or implicit time zone requirements. Does the job require significant overlap with a specific time zone, limiting flexibility despite being \"remote\"?"
        },
        "Careers URL": {
          "type": "string",
          "format": "url",
          "description": "The company's careers URL."
        },
        "Mission And Values": {
          "type": "string",
          "description": "The company's articulated vision for internal culture or inferred values. Are remote work values (trust, autonomy, clear communication) emphasized?"
        },
        "Careers Emails": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "email"
          },
          "description": "Email addresses associated with the company's recruiting or human resource functions (if available)."
        },
        "LinkedIn & Other Hiring Channels": {
          "type": "array",
          "items": {
            "type": "string",
            "format": "url"
          },
          "description": "Links to additional hiring channels, such as LinkedIn."
        },
        "Red Flag Screen": {
          "type": "string",
          "description": "Search for any significant adverse publicity or controversy, particularly complaints about remote work policies, communication issues, or unequal treatment of remote vs. in-office employees. Report 'no significant information found' if none."
        }
      },
      "required": [
        "Remote Friendly?",
        "Remote Work Culture Assessment",
        "Location Restrictions?",
        "Salary Transparency",
        "Global Compensation Strategy?",
        "Time Zone Expectations?",
        "Careers URL",
        "Mission And Values",
        "Red Flag Screen"
      ]
    },
    "Summary": {
      "type": "object",
      "properties": {
        "Company Position": {
          "type": "string",
          "description": "Overall background of the company and its position in its industry."
        },
        "HQ And Headcount": {
          "type": "string",
          "description": "Company's headquarters and approximate headcount. Is the headcount primarily remote, or primarily based in the HQ location?"
        },
        "Remote Friendly?": {
          "type": "string",
          "description": "Is the company remote friendly? Summary including any location restrictions and the overall maturity of their remote work culture. Summarize their global compensation strategy."
        },
        "Careers URL": {
          "type": "string",
          "format": "url",
          "description": "Link to the company's career URL."
        },
        "Lead Score Rationale": {
          "type": "string",
          "description": "Rationale for the Remote Commitment Lead Score. Justify the score based on evidence gathered in the 'Careers' section."
        }
      },
      "required": [
        "Company Position",
        "HQ And Headcount",
        "Remote Friendly?",
        "Careers URL",
        "Lead Score Rationale"
      ]
    }
  },
  "required": [
    "Remote Commitment Lead Score",
    "Company Details",
    "People And Funding",
    "Market Positioning",
    "Careers",
    "Summary"
  ]
}
```