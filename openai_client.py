import openai
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

openai.api_key = os.environ.get("OPENAI_API_KEY")


def categorize_text(text):
    categories = [
        "Consensus",
        "Devimint/Teseting",
        "Lightning",
        "On-Chain Bitcoin",
        "Rust",
        "Nix",
        "UI/Frontend",
        "CI/CD",
        "Other",
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant who responds in exactly 1 word with the correct categorization.",
            },
            {"role": "user", "content": f"Categorize the following text: {text}"},
            {
                "role": "assistant",
                "content": f"The text belongs to one of these categories: {categories}",
            },
        ],
    )

    return response["choices"][0]["message"]["content"]
