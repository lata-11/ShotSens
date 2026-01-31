from services.llm_service import call_llm
from agent.prompt_builder import build_prompt


class SceneIntentAgent:
    def __init__(self):
        pass

    def analyze_scene(self, scene_text: str) -> dict:
        prompt = build_prompt(scene_text)
        response = call_llm(prompt)
        return response
