from langchain_core.prompts import PromptTemplate

def get_scene_prompt(format_instructions: str):
    template = """
You are a cinematic scene analyst.

Your task:
Extract ONLY essential cinematic direction from the scene.
Avoid storytelling, metaphors, or unnecessary explanation.

STRICT RULES:
- Be concise and practical
- Max 2 sentences per field
- props can be well researched
- Focus on actionable filmmaking choices
- No emotional interpretation beyond what is visible
- No poetic language
- No repetition
- Output must follow the format exactly

Scene:
{scene_text}

{format_instructions}
"""

    return PromptTemplate(
        template=template,
        input_variables=["scene_text"],
        partial_variables={"format_instructions": format_instructions},
    )
