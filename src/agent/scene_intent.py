from langchain_core.output_parsers import PydanticOutputParser
import json
from langchain_core.messages import AIMessage
from schema.scene_schema import SceneOutput
from agent.prompt_builder import (
    get_primary_scene_prompt,
    get_minimal_scene_prompt
)
from services.llm_service import get_llm

from confidence.confidence_validator import should_stop, validate_confidence

class SceneAgent:
    def __init__(self):
        self.llm = get_llm()

        # Parser ONLY for primary (full) run
        self.parser = PydanticOutputParser(pydantic_object=SceneOutput)

        # Build prompts
        self.primary_prompt = get_primary_scene_prompt(
            self.parser.get_format_instructions()
        )
        self.minimal_prompt = get_minimal_scene_prompt()   # <-- NO format instructions

        # LCEL chain ONLY for primary run
        self.primary_chain = self.primary_prompt | self.llm | self.parser

    def _to_dict(self, ai_msg: AIMessage):
        """Extract JSON dict from AIMessage."""
        text = ai_msg.content

        # Sometimes LLM returns non-strict text → attempt to extract JSON block
        try:
            return json.loads(text)
        except:
            # Try fallback → locate JSON manually
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])



    def run(self, scene_text, conf_threshold=0.10, max_runs=5):
        """
        1. Run full prompt once.
        2. Repeatedly run minimal prompt until:
        - confidence difference < conf_threshold OR
        - max_runs reached.
        3. Return primary output + validated confidence.
        """

        # Primary full-quality run (parsed)
        run1 = self.primary_chain.invoke({"scene_text": scene_text})
        run1_dict = run1.dict()
        print("Primary run output:", run1_dict)

        # Track all confidence values
        conf_values = [run1_dict["confidence"]]

        # Prepare minimal prompt
        minimal_prompt_text = self.minimal_prompt.format(scene_text=scene_text)

        # Iterative minimal runs
        for _ in range(max_runs - 1):
            run_msg = self.llm.invoke(minimal_prompt_text)
            run_dict = self._to_dict(run_msg)
            print("Minimal run output:", run_dict)
            conf_values.append(run_dict["confidence"])

            # Early stopping condition
            if should_stop(conf_values, conf_threshold):
                break

        # Compute final validated confidence
        final_conf = validate_confidence(conf_values)

        # Attach to primary output
        run1_dict["validated_confidence"] = final_conf
        return SceneOutput(**run1_dict)


