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
        self.minimal_prompt = get_minimal_scene_prompt()
        self.minimal_chain = (
            self.minimal_prompt
            | self.llm
            | self.minimal_parser
        )


    def run(self, scene_text, mode="🎬 Director's Cut", conf_threshold=0.10, max_runs=5):
        is_directors_cut = mode == "🎬 Director's Cut"

        # 1️⃣ Primary run
        primary = self.primary_chain.invoke({"scene_text": scene_text})
        primary_dict = primary.dict()
        print("Primary run output:", primary_dict)

        conf_values = [primary_dict["confidence"]]

        # 2️⃣ Confidence validation (Director's Cut only)
        if is_directors_cut:
            for _ in range(max_runs - 1):
                minimal = self.minimal_chain.invoke({"scene_text": scene_text})
                minimal_dict = minimal.dict()
                conf_values.append(minimal_dict["confidence"])

                if should_stop(conf_values, conf_threshold):
                    break

        # 3️⃣ Final confidence
        final_conf = validate_confidence(conf_values) or conf_values[0]
        primary_dict["validated_confidence"] = final_conf

        return SceneOutput(**primary_dict)




        # Prepare minimal prompt
        minimal_prompt_text = self.minimal_prompt.format(scene_text=scene_text)

        # Iterative minimal runs
        if is_directors_cut:
            for _ in range(max_runs - 1):
                run_msg = self.llm.invoke(minimal_prompt_text)
                run_dict = self._to_dict(run_msg)
                print("Minimal run output:", run_dict)
                conf_values.append(run_dict["confidence"])

                # Early stopping condition
                if should_stop(conf_values, conf_threshold):
                    break

        # Compute final validated confidence
        final_conf = validate_confidence(conf_values) or conf_values[0]

        # Attach to primary output
        run1_dict["validated_confidence"] = final_conf

        if is_directors_cut:
            return SceneOutput(**run1_dict)
        else:
            # Minimal mode → adapt to SceneOutput schema
            return SceneOutput(
                emotion=run1_dict["emotion"],
                visual_mood=run1_dict["visual_mood"],
                camera_style=run1_dict["camera_style"],
                composition=run1_dict.get("composition", ""),
                set_design="N/A",
                props=[],
                blocking="N/A",
                costumes="N/A",
                narrative_reasoning="Production Notes Mode",
                confidence=run1_dict["confidence"],
                validated_confidence=final_conf
            )


    def generate_image(self, scene_output):
            return self.image_gen.generate(scene_output.model_dump())
