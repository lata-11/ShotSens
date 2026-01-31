from agent.scene_intent import SceneAgent
from dotenv import load_dotenv

load_dotenv() # Loads your .env file

def main():
    agent = SceneAgent()
    script_snippet = """
    INT. HOSPITAL ROOM - NIGHT
    SHE laughs as HE jokes. Her hands tremble under the blanket.
    """
    
    result = agent.run(script_snippet)
    print(f"ShotSens Intent: {result.json(indent=2)}")

if __name__ == "__main__":
    main()