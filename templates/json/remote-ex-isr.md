{
  "type": "object",
  "properties": {
    "Remote Friendliness & Israel Hiring Lead Score": {
      "type": "integer",
      "description": "A score out of 10 assessing remote friendliness and Israel hiring potential."
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
          "description": "The company's headquarters (city, country)."
        },
        "Other Locations": {
          "type": "string",
          "description": "Satellite offices and approximate workforce distribution globally."
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
          "description": "The names of the key people associated with the company. For startups, focus on the founders."
        },
        "VCs And Backers": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "List of venture capital firms and backers if publicly available."
        },
        "Funding History": {
          "type": "string",
          "description": "Details about the company's funding history are in the public domain."
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
          "description": "What distinguishes the company's products and its philosophy from others in a similar space?"
        },
        "Vision": {
          "type": "string",
          "description": "Attempt to retrieve information in which the company or its leadership describes its broad strategic vision, especially for the current calendar year."
        },
        "Competitive Landscape": {
          "type": "string",
          "description": "Who are the company's main competitors and how do they distinguish themselves from them?"
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
          "description": "Assess the maturity/quality of their potential remote work culture."
        },
        "Hiring in Israel?": {
          "type": "boolean",
          "description": "Explicitly state whether the company has a history of hiring in Israel or similar time zones/regions."
        },
        "Salary Transparency": {
          "type": "string",
          "enum": ["Yes", "No", "Partial"],
          "description": "Is the company transparent about salary ranges in their job postings?"
        },
        "Careers URL": {
          "type": "string",
          "format": "url",
          "description": "The company's careers URL."
        },
        "Mission And Values": {
          "type": "string",
          "description": "The company's articulated vision for internal culture or inferred values (e.g., hustle mindset, employee wellness, stable growth)."
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
          "description": "Any significant adverse publicity or controversy surrounding the company, particularly regarding treatment of staff. Report 'no significant information found' if none."
        }
      },
      "required": [
        "Remote Friendly?",
        "Remote Work Culture Assessment",
        "Hiring in Israel?",
        "Salary Transparency",
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
          "description": "Company's headquarters and approximate headcount."
        },
        "Remote Friendly?": {
          "type": "string",
          "description": "Is the company remote friendly? Summary including findings about hiring remotely in Israel."
        },
        "Careers URL": {
          "type": "string",
          "format": "url",
          "description": "Link to the company's career URL."
        },
        "Lead Score Rationale": {
          "type": "string",
          "description": "Rationale for the Remote Friendliness & Israel Hiring Lead Score. Justify the score based on evidence gathered."
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
    "Remote Friendliness & Israel Hiring Lead Score",
    "Company Details",
    "People And Funding",
    "Market Positioning",
    "Careers",
    "Summary"
  ]
}