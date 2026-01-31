import streamlit as st
from src.agent.scene_intent import SceneAgent

st.set_page_config(page_title="ShotSens", layout="wide")

st.title("🎬 ShotSens Scene Intent Analyzer")

agent = SceneAgent()

scene_text = st.text_area("Enter Scene Text", height=200)

if st.button("Load Example Scene"):
    scene_text = """
    INT. HOSPITAL ROOM - NIGHT
    SHE laughs as HE jokes. Her hands tremble under the blanket.
    """

def render_result(result):
    st.subheader("🎭 Emotion")
    st.info(result.emotion)

    st.subheader("🎨 Visual Mood")
    st.write(result.visual_mood)

    st.subheader("📷 Camera Style")
    st.write(result.camera_style)

    st.subheader("🏗 Set Design")
    st.write(result.set_design)

    st.subheader("🧩 Props")
    for prop in result.props:
        st.markdown(f"- {prop}")

    st.subheader("👗 Costumes")
    st.write(result.costumes)

    st.subheader("🎯 Blocking")
    st.write(result.blocking)

    st.subheader("🖼 Composition")
    st.write(result.composition)

    st.subheader("🧠 Narrative Reasoning")
    st.write(result.narrative_reasoning)

    st.subheader("📊 Confidence Score")
    st.progress(result.confidence)
    st.write(f"Confidence: **{result.confidence * 100:.1f}%**")

    with st.expander("🔍 View Raw JSON"):
        st.json(result.model_dump())


if st.button("Analyze Scene"):
    if scene_text.strip():
        with st.spinner("Analyzing scene..."):
            try:
                result = agent.run(scene_text)
                render_result(result)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter valid scene text.")
