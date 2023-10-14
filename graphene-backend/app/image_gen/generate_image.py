import openai
import os


openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_image(description: str):
    response = openai.Image.create(
        prompt=description, n=1, size="512x512"
    )
    image_url = response["data"][0]["url"]
    return image_url