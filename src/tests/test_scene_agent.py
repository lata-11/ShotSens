import sys
import os
import json
import pytest
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.agent.scene_intent import SceneAgent

load_dotenv()

@pytest.fixture(scope="module")
def agent():
    return SceneAgent()


test_cases = [
    {
        "name": "emotional_scene",
        "input": """
        INT. HOSPITAL ROOM - NIGHT
        SHE laughs as HE jokes. Her hands tremble under the blanket.
        """,
    },
    {
        "name": "action_scene",
        "input": """
        EXT. STREET - DAY
        A car explodes as the hero dives behind a barricade.
        Gunshots echo in the background.
        """,
    },
    {
        "name": "romantic_scene",
        "input": """
        EXT. BEACH - SUNSET
        They walk hand in hand as the waves crash gently.
        He whispers, 'I never want this moment to end.'
        """,
    },
    {
        "name": "tense_scene",
        "input": """
        INT. INTERROGATION ROOM - NIGHT
        Sweat drips down his forehead as the detective leans closer.
        Silence fills the air.
        """,
    },
    {
        "name": "eerie_scene",
        "input": """
        Dark, silent, and eerie street.
        PODCAST VOICE:
        Yem chesthudhavida aa ganta sepu anega?
        - SUSTAIN: Dark street.
        A loud cry is heard from the balcony. Spine chilling. Like
        a ghost sobbing, the cry is reverberating into the night.
        PODCAST VOICE:
        Roju sarigga ganta... Ratri yenimidhi nundi tommidhi varaku... yedusthundhi!
        Bhayamkaramga. Ollu gagurlupodechela... Oka pretham laanti yedupu. PRATHI ROJU!!!
        """,
    }
]

@pytest.mark.parametrize("case", test_cases)
def test_scene_agent(agent, case):
    result = agent.run(case["input"])

    print(f"\n--- Test Case: {case['name']} ---")
    print("Prettified Response JSON:")
    print(json.dumps(result.model_dump(), indent=4))  # Use indent=4 for better readability

    # Basic sanity assertions
    assert result is not None
    assert isinstance(result.model_dump(), dict)
