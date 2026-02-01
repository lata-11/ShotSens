from src.services.llm_service import get_llm
from src.image_generator.image_generator import ImageGenerator

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import AIMessage
import json

from src.schema.scene_schema import SceneOutput, MinimalSceneOutput

from src.agent.prompt_builder import (
    get_primary_scene_prompt,
    get_minimal_scene_prompt
)
from src.confidence.confidence_validator import should_stop, validate_confidence


class SceneAgent:
    def __init__(self):
        self.llm = get_llm()
        self.image_gen = ImageGenerator()

        # Primary (Director's Cut)
        self.primary_parser = PydanticOutputParser(
            pydantic_object=SceneOutput
        )
        self.primary_prompt = get_primary_scene_prompt(
            self.primary_parser.get_format_instructions()
        )
        self.primary_chain = (
            self.primary_prompt
            | self.llm
            | self.primary_parser
        )

        # Minimal (Production Notes)
        self.minimal_parser = PydanticOutputParser(
            pydantic_object=MinimalSceneOutput
        )

        self.minimal_prompt = get_minimal_scene_prompt(
            self.minimal_parser.get_format_instructions()
        )
        self.minimal_chain = (
            self.minimal_prompt
            | self.llm
            | self.minimal_parser
        )


    def run(self, scene_text, mode="director", max_iterations=3, threshold=0.05):
        """
        Runs the LLM multiple times:
        - First run: main output
        - Additional runs: only for confidence validation
        - Stop early if confidence stabilizes
        - Includes fallback values for missing fields
        """

        # 1️⃣ Choose which model output is the MAIN one
        if mode == "director":
            # main = primary prompt
            main_run = self.primary_chain.invoke({"scene_text": scene_text})
        else:
            # main = minimal prompt
            main_run = self.minimal_chain.invoke({"scene_text": scene_text})

        main_dict = main_run.dict()

        # 🔧 Add default values for missing fields
        main_dict = self._fill_missing_fields(main_dict)

        # Start collecting confidence values
        conf_values = [main_dict.get("confidence", 0.7)]

        # 2️⃣ Additional runs for confidence validation only
        for i in range(1, max_iterations):

            # Always use minimal prompt for validation
            validation_run = self.minimal_chain.invoke({"scene_text": scene_text})
            validation_dict = validation_run.dict()
            validation_dict = self._fill_missing_fields(validation_dict)

            conf_values.append(validation_dict.get("confidence", 0.7))

            # Early stopping: if last 2 confidences are close enough
            if should_stop(conf_values, threshold):
                break

        # 3️⃣ Final validated confidence
        final_conf = validate_confidence(conf_values)

        # Attach validated confidence to the main output
        main_dict["validated_confidence"] = final_conf

        return SceneOutput(**main_dict)

    def _fill_missing_fields(self, output_dict: dict) -> dict:
        """Fill missing required fields with sensible defaults."""
        defaults = {
            "composition": "Balanced framing with clear focal points",
            "narrative_reasoning": "Analysis based on available scene context",
            "confidence": 0.7,
            "emotion": "Undetermined",
            "visual_mood": "Naturalistic lighting",
            "camera_style": "Standard coverage",
            "set_design": "Generic setting",
            "props": [],
            "costumes": "Practical clothing",
            "blocking": "Standard actor positioning"
        }
        
        missing = []
        for key, default_value in defaults.items():
            if key not in output_dict or output_dict[key] is None:
                output_dict[key] = default_value
                missing.append(key)
        
        # Create a message if any fields were filled
        if missing:
            missing_str = ", ".join(missing)
            output_dict["missing_fields_message"] = (
                f"⚠️ The model response was incomplete. The following fields were auto-filled with contextual defaults: {missing_str}. "
                f"For better results, try a more detailed scene description. Try only one scene at a time."
            )
        
        return output_dict



    def generate_image(self, scene_output):
            return self.image_gen.generate(scene_output.model_dump())
