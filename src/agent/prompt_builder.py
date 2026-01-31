def build_prompt(scene_text: str) -> str:
    return f"""
You are a film director and cinematographer AI.

Analyze the following scene and infer:
- emotion
- visual mood
- camera style
- confidence (0–1)

Return ONLY valid JSON.

Scene:
{scene_text}
"""
