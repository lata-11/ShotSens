from agent.scene_intent import SceneIntentAgent

if __name__ == "__main__":
    scene = """
    They sit in silence. The clock ticks loudly.
    He avoids eye contact.
    """

    agent = SceneIntentAgent()
    result = agent.analyze_scene(scene)

    print(result)
