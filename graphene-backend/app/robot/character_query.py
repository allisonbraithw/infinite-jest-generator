import os
import re
import sys
import pickle

import chromadb
import tiktoken
import openai
import nltk

import PyPDF2 as pdf
from sentence_transformers import SentenceTransformer


openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_character_description_summary(docs: list, character: str = "Hal Incandenza"):
    # pass results to OpenAI & ask it to summarize
    system_prompt = f"You are a helpful AI assistant that takes chunks of text about a character \
        and produces a summary of that character's physical appearance. You should extract and \
        summarize physical descriptors only, ignore non-physical details about the character. \
        ```{docs}```"
    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {
            "role": "user",
            "content": f"Please provide me a detailed physical description of the character {character}",
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.1,
    )

    return response.choices[0].message.content


def generate_image(description: str):
    response = openai.Image.create(
        prompt=description, n=1, size="512x512"
    )
    image_url = response["data"][0]["url"]
    return image_url
