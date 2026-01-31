from google import genai
import os
import base64
from src.agent.prompt_builder import build_image_prompt

class ImageGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def generate(self, intent_dict):
        prompt = build_image_prompt(intent_dict)

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt
        )

        images_b64 = []

        for part in response.candidates[0].content.parts:
            # Ignore text-only parts
            if hasattr(part, "inline_data") and part.inline_data and part.inline_data.mime_type == "image/png":
                raw_bytes = part.inline_data.data
                b64 = base64.b64encode(raw_bytes).decode("utf-8")
                images_b64.append(b64)

        return images_b64
