from langchain_core.prompts import PromptTemplate

def get_primary_scene_prompt(format_instructions: str):
    template = """
You are a film director preparing a scene for creative pre-production discussions 
with the cinematographer, production designer, and actors.

Your goal is to clearly explain the cinematic intent behind visual choices so the 
creative team understands the emotional tone, atmosphere, and staging decisions.

USE CASE:
This output will be used during pre-production meetings to align the creative team 
on how the scene should feel and appear on screen.

OUTPUT STYLE:
- Each field: 1–2 concise sentences
- Use professional cinematic terminology
- Explain WHY the visual choices support the scene’s emotional subtext
- Focus on storytelling clarity, mood, and performance dynamics

DO NOT:
- Describe exact object placement
- Invent backstory
- Introduce themes not present
- Use poetic metaphors
- Change emotional categories

REQUIRED FOCUS:
- Emotional tone and character psychology
- Visual mood and lighting intention
- Camera choices and audience perspective
- Set design and environmental storytelling
- Props relevance
- Actor blocking and spatial relationships
- Frame composition and focus
- Costume cues and character state
- Narrative reasoning (brief explanation)

SCENE:
{scene_text}

{format_instructions}
"""

    return PromptTemplate(
        template=template,
        input_variables=["scene_text"],
        partial_variables={"format_instructions": format_instructions},
    )


def get_minimal_scene_prompt(format_instructions: str):
    template = """
You are generating semantic intents as short production notes for a film scene.
Strictly return JSON

RULES:
- Keep every field extremely short (5–10 words).
- Focus on practical, production-friendly descriptions.
- Do NOT omit any fields.
- "Props" must ALWAYS be a string.
- Avoid style, poetry, or cinematographer language.
- Use neutral, factual, logistical wording.

REQUIRED FOCUS:
- Emotional tone and character psychology
- Visual mood and lighting intention
- Camera choices and audience perspective
- Set design and environmental storytelling
- Props relevance
- Actor blocking and spatial relationships
- Frame composition and focus
- Costume cues and character state
- Narrative reasoning (brief explanation)

Scene:
{scene_text}

{format_instructions}
"""

    return PromptTemplate(
        template=template,
        input_variables=["scene_text"],
        partial_variables={"format_instructions": format_instructions},
    )



def build_image_prompt(intent: dict) -> str:
    """
    Convert scene intent to an image generation prompt.
    """

    props = ", ".join(intent.get("props", [])) if isinstance(intent.get("props"), list) else intent.get("props")

    return f"""
Generate a cinematic keyframe image based on this scene intent.

Emotion: {intent.get('emotion')}
Visual Mood: {intent.get('visual_mood')}
Camera Style: {intent.get('camera_style')}
Set Design: {intent.get('set_design')}
Props: {props}
Costumes: {intent.get('costumes')}
Blocking: {intent.get('blocking')}
Composition: {intent.get('composition')}

Requirements:
- Produce a single high-quality cinematic frame
- Accurate film lighting and mood
- Realistic camera angle based on the camera style
- Include set, props, and costumes where appropriate
- DO NOT add characters or objects not mentioned
- DO NOT modify the emotional tone

Return ONLY the generated image.
"""


__all__ = [
    "get_primary_scene_prompt",
    "get_minimal_scene_prompt",
    "build_image_prompt"
]
