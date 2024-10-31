from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=API_KEY)

# Define the structure for the resume
functions = [
    {
        "name": "generate_resume",
        "description": "Generate a structured resume from candidate description",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full name of the candidate"
                },
                "currentRole": {
                    "type": "string",
                    "description": "Current job title"
                },
                "experience": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company": {
                                "type": "string",
                                "description": "Name of the company"
                            },
                            "position": {
                                "type": "string",
                                "description": "Job title"
                            },
                            "duration": {
                                "type": "string",
                                "description": "Duration of employment"
                            },
                            "achievements": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "Key achievements and responsibilities"
                            }
                        },
                        "required": ["company", "position", "duration"]
                    }
                },
                "skills": {
                    "type": "object",
                    "properties": {
                        "technical": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "soft": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["technical"]
                },
                "yearsOfExperience": {
                    "type": "integer",
                    "description": "Total years of professional experience"
                }
            },
            "required": ["name", "currentRole", "experience", "skills", "yearsOfExperience"]
        }
    }
]

def generate_resume(description, use_turbo=False):
    """
    Generate a structured resume using either GPT-4-0 or GPT-4-turbo-preview
    
    Args:
        description (str): Description of the candidate
        use_turbo (bool): If True, uses GPT-4-turbo-preview, otherwise uses GPT-4-0
    """
    try:
        model = "gpt-4o"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert resume writer. Generate a detailed professional 
                    resume based on the provided description. Focus on creating realistic and 
                    relevant content that matches the candidate's experience level."""
                },
                {
                    "role": "user",
                    "content": description
                }
            ],
            functions=functions,
            function_call={"name": "generate_resume"},
            temperature=0.7  # Balanced between creativity and consistency
        )

        return json.loads(response.choices[0].message.function_call.arguments)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Example usage
description = """
The candidate is 27 years old, has 5 years of experience in IT and has experience in Java and Python. 
They have worked in 2 companies and is currently working as a Senior Software Engineer.
"""

# Using GPT-4-0 (May 2024 version)
resume = generate_resume(description)
print("\nGPT-4-0 Generated Resume:")
print(json.dumps(resume, indent=2))

# Example output:
"""
{
  "name": "Michael Chen",
  "currentRole": "Senior Software Engineer",
  "yearsOfExperience": 5,
  "experience": [
    {
      "company": "TechCorp Solutions",
      "position": "Senior Software Engineer",
      "duration": "2023 - Present",
      "achievements": [
        "Led development of microservices architecture using Java Spring Boot",
        "Implemented automated testing pipelines reducing bug detection time by 40%",
        "Mentored junior developers and conducted architecture design reviews"
      ]
    },
    {
      "company": "DataSys Technologies",
      "position": "Software Engineer",
      "duration": "2019 - 2023",
      "achievements": [
        "Developed Python-based data processing pipelines",
        "Improved system performance by 35% through code optimization",
        "Collaborated with cross-functional teams on major product releases"
      ]
    }
  ],
  "skills": {
    "technical": [
      "Java",
      "Python",
      "Spring Boot",
      "Microservices",
      "Docker",
      "AWS",
      "Git",
      "SQL"
    ],
    "soft": [
      "Team Leadership",
      "Mentoring",
      "Problem Solving",
      "Technical Documentation"
    ]
  }
}
"""