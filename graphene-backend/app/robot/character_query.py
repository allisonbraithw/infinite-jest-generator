import os
import logging
import io

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import openai


openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_character_description_summary(docs: list, character: str = "Hal Incandenza"):
    # pass results to OpenAI & ask it to summarize
    system_prompt = f"You are a helpful AI assistant that takes chunks of text about a character \
        and produces a summary of that character's physical appearance. You should extract and \
        summarize physical descriptors only, ignore non-physical details about the character, and ignore \
        descriptions of other characters not specified in the prompt.\
        ```{docs}```"
    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {
            "role": "user",
            "content": f"Please provide me a detailed physical description of the character {character}",
        },
    ]
    logging.info("Sending prompt to OpenAI")
    logging.info("Prompt: " + system_prompt)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.1,
    )
    logging.info("Received response from OpenAI")

    return response.choices[0].message.content


def generate_image(description: str):
    response = openai.Image.create(
        prompt=description, n=1, size="512x512"
    )
    image_url = response["data"][0]["url"]
    return image_url


def generate_stability_image(description: str):
    stability_api = client.StabilityInference(
        key=os.environ.get("STABILITY_API_KEY"),
        verbose=True,
        engine="stable-diffusion-512-v2-1"
    )

    images = stability_api.generate(
        prompt=description)

    for resp in images:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                logging.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                # Save our generated images with their seed number as the filename.
                img.save(str(artifact.seed) + ".png")
