from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_KEY")


client = OpenAI(api_key=API_KEY)

# Define the structure for the resume
functions = [
    {
        "name": "generate_resume",
        "description": "Generate a structured resume from candidate description",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "summary of the candidates professional experience . Shows highlights of capability"
                },
                "personalDetails": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "full name of the candidate"
                        },
                        "title": {
                            "type": "string",
                            "description": "designation within organisation e.g director of engineering"
                        },
                        "email": {
                            "type": "string",
                            "description": "email id of candidate"
                        },
                        "personalUrls": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "personal website or blogsite or link to personal github page"
                            }
                        },
                        "city": {
                            "type": "string",
                            "description": "city in which the person stays currently"
                        },
                        "phone": {
                            "type": "string",
                            "description": "phone number of the candidate ,eg .91-9545037689"
                        }
                    }
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
                        "required": [
                            "company",
                            "position",
                            "duration"
                        ]
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
                    "required": [
                        "technical"
                    ]
                },
                "yearsOfExperience": {
                    "type": "integer",
                    "description": "Total years of professional experience"
                },
                "education": {
                    "type": "array",
                    "description" : "education details of degree and secondary high school",
                    "items": {
                        "type": "object",
                        "properties": {
                            "institutionName": {
                                "type": "string",
                                "description": "Name of the education institute where candidate studied"
                            },
                            "duration": {
                                "type": "string",
                                "description": "start year- end year of the academic year for the candudate "
                            },
                            "degreeName": {
                                "type": "string",
                                "description": "degree name , e.g Bachelor of engineering "
                            }
                        }
                    }
                }
            },
            "required": [
                "personalDetails",
                "experience",
                "skills",
                "yearsOfExperience",
                "education"
            ]
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
