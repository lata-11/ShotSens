from langchain.output_parsers import PydanticOutputParser
from schemas.scene_schema import SceneOutput
from agent.prompt_builder import get_scene_prompt
from services.llm_service import get_llm

class SceneAgent:
    def __init__(self):
        self.llm = get_llm()
        self.parser = PydanticOutputParser(pydantic_object=SceneOutput)
        self.prompt = get_scene_prompt(self.parser.get_format_instructions())
        # The LCEL Chain: Prompt -> LLM -> Parser
        self.chain = self.prompt | self.llm | self.parser

    def run(self, scene_text):
        return self.chain.invoke({"scene_text": scene_text})