import os
import base64
import requests
import logging
from celery import shared_task
from django.conf import settings
from .models import GeneratedImage

# Set up logging
logger = logging.getLogger(__name__)

@shared_task
def generate_image(prompt):
    engine_id = "stable-diffusion-v1-6"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = settings.STABILITY_API_KEY

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    image_urls = []

    # Ensure the output directory exists
    output_dir = './out'
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logger.info(f"Created directory: {output_dir}")
        except Exception as e:
            logger.error(f"Failed to create directory {output_dir}: {e}")
            raise

    for i, image in enumerate(data["artifacts"]):
        image_data = base64.b64decode(image["base64"])
        image_path = os.path.join(output_dir, f"{prompt.replace(' ', '_')}_{i}.png")
        try:
            with open(image_path, "wb") as f:
                f.write(image_data)
            logger.info(f"Saved image: {image_path}")
            image_urls.append(image_path)
        except Exception as e:
            logger.error(f"Failed to save image {image_path}: {e}")
            raise

    for image_url in image_urls:
        GeneratedImage.objects.create(prompt=prompt, image_url=image_url)

    return image_urls
