```json
{
  "type": "object",
  "properties": {
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
          "description": "The names of the key people associated with the company (focus on founders for startups)."
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
          "description": "Details about the company's funding history if publicly available."
        }
      },
      "required": [ "Key People" ]
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
          "description": "The company's broad strategic vision, especially for the current calendar year."
        },
        "Competitive Landscape": {
          "type": "string",
          "description": "Who are the company's main competitors and how do they distinguish themselves?"
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
          "description": "Analysis of the company's approach to remote work, including any caveats."
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
          "description": "Email addresses associated with the company's hiring or human resource functions (if available)."
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
        "Careers URL",
        "Mission And Values",
        "Red Flag Screen"
      ]
    },
    "Summary": {
      "type": "object",
      "properties": {
        "Company position": {
          "type": "string",
          "description": "Overall background of the company and its position in its industry."
        },
        "HQ And Headcount": {
          "type": "string",
          "description": "Company's headquarters and approximate headcount."
        },
        "Remote friendly?": {
          "type": "string",
          "description": "Summary of the company's remote work policy."
        },
        "Careers URL": {
          "type": "string",
          "format": "url",
          "description": "Link to the company's career URL."
        }
      },
      "required": [
        "Company position",
        "HQ And Headcount",
        "Remote friendly?",
        "Careers URL"
      ]
    }
  },
  "required": [
    "Company Details",
    "People And Funding",
    "Market Positioning",
    "Careers",
    "Summary"
  ]
}
```