import openai
import os
import base64

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


openai.organization = os.environ.get("OPENAI_ORG")
openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_image(description: str):
    response = openai.Image.create(
        model="dall-e-3", prompt=description, n=1, size="1024x1024"
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
                base64_encoded = base64.b64encode(
                    artifact.binary).decode('utf-8')
                return f"data:image/png;base64,{base64_encoded}"


# Scratch  Notes
# img = Image.open(io.BytesIO(artifact.binary))
# # Save our generated images with their seed number as the filename.
# img.save(str(artifact.seed) + ".png")
