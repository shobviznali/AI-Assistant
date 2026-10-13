import os

from dotenv import load_dotenv
from openai import OpenAI
from app.services.prompt_service import SYSTEM_PROMPT
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(prompt: str) -> str:

    response = client.responses.create(
        model="gpt-4.1-mini",
        instructions=SYSTEM_PROMPT,
        input=prompt
    )

    answer = response.output_text

    return answer
