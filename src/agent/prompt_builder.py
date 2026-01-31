from langchain_core.prompts import PromptTemplate

def get_primary_scene_prompt(format_instructions: str):
    template = """
You are a film director analyzing a scene.  
Your job is to describe the cinematic intent using clear, practical, director-friendly language.  
Your interpretation should match the same emotional tone, mood, and camera intention  
that you would express in a short creative brief.

CRITICAL RULE:
Your answers must represent the *same conceptual categories* that would appear  
in a compact 2–3 word summary of the same scene.  
The short version and long version must align in meaning.

GUIDELINES:
- Keep each field concise (1–2 sentences max)
- Use cinematic terminology but avoid poetic/flowery language
- Focus on emotional tone, mood, camera intent, set design, props, blocking, and composition
- DO NOT describe exact object placement (left/right)
- DO NOT add story interpretation that is not grounded in the scene
- DO NOT change emotional categories between long and short formats
- Narrative reasoning: explain briefly *why* these choices fit the scene's subtext

SCENE:
{scene_text}

{format_instructions}
"""

    return PromptTemplate(
        template=template,
        input_variables=["scene_text"],
        partial_variables={"format_instructions": format_instructions},
    )

def get_minimal_scene_prompt():
    template = """
You are summarizing the SAME cinematic intent that a film director would describe  
in the longer version of this analysis.  
Your task is to output a *compressed version* of the same meaning  
using 2–3 word cinematic labels.

These short labels MUST represent the same emotional tone, visual mood,  
and camera intention that would appear in the full director-style description.  
Do NOT reinterpret or shift emotional categories.  
Only compress — do not alter meaning.

OUTPUT STRICT JSON (escaped braces):
{{
  "emotion": "...",
  "visual_mood": "...",
  "camera_style": "...",
  "confidence": float
}}

RULES:
- Max 3 words per field
- The meaning must match the longer version of the same categories
- No story interpretation
- No new creative angles
- No poetic language
- No object placement
- No long sentences
- No text outside the JSON

SCENE:
{scene_text}
"""

    return PromptTemplate(
        template=template,
        input_variables=["scene_text"]
    )
