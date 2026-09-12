import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in .env")


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def analyze_job_description(
    title: str,
    company: str,
    job_description: str
) -> str:

    prompt = f"""
You are an AI career assistant.

Analyze this job vacancy.

Job Title: {title}
Company: {company}

Job Description:
{job_description}

Return a concise analysis using exactly these sections:

1. Required Skills
2. Key Responsibilities
3. Difficulty Level
4. Recommended Preparation

Keep the answer practical and easy to understand.
"""

    print("Sending request to Gemini...")

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    print("Gemini response received.")

    return interaction.output_text


def generate_cover_letter(
    title: str,
    company: str,
    job_description: str
) -> str:

    prompt = f"""
You are an expert career assistant.

Write a professional but natural cover letter for the following job.

Job Title:
{title}

Company:
{company}

Job Description:
{job_description}

Requirements:
- Write in English.
- Keep it concise.
- Make it specific to the job description.
- Do not invent experience, education, or achievements.
- Use a professional but human tone.
- Return only the cover letter.
"""

    print("Sending cover letter request to Gemini...")

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    print("Gemini cover letter response received.")

    return interaction.output_text