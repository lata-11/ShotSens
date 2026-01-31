from google import genai
import os
from src.agent.prompt_builder import build_image_prompt

class ImageGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        print(dir(self.client.models))

    def generate(self, intent_dict):
        prompt = build_image_prompt(intent_dict)

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt
        )

        for i, part in enumerate(response.candidates[0].content.parts):
            if part.inline_data:
                # Convert the inline data to a PIL Image object
                image = part.as_image()
                # Save the image to a file
                image.save(f'generated_image_{i}.png')
                print(f"Image saved as generated_image_{i}.png")
            elif part.text:
                print(f"Text part: {part.text}")
        
