import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agent.scene_intent import SceneAgent
from dotenv import load_dotenv

load_dotenv() # Loads your .env file

def main():
    agent = SceneAgent()
    script_snippet = """
    INT. HOSPITAL ROOM - NIGHT
    SHE laughs as HE jokes. Her hands tremble under the blanket.
    """
    
    result = agent.run(script_snippet)
    print(f"ShotSens Intent: {result.model_dump_json(indent=2)}")


if __name__ == "__main__":
    main()