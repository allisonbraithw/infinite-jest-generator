import openai


def generate_image(description: str):
    response = openai.Image.create(
        prompt=description, n=1, size="512x512"
    )
    image_url = response["data"][0]["url"]
    return image_url
