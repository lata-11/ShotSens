from langchain.prompts import PromptTemplate

DIRECTOR_TEMPLATE = """
You are a Director and Cinematographer analyzing a script.
{format_instructions}

SCENE TEXT: {scene_text}

Analyze character subtext and hospital/night settings to infer visuals.
"""

def get_scene_prompt(parser_instructions):
    return PromptTemplate(
        template=DIRECTOR_TEMPLATE,
        input_variables=["scene_text"],
        partial_variables={"format_instructions": parser_instructions}
    )