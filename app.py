import streamlit as st
import os
import base64
import base64
from io import BytesIO
from PIL import Image
from src.agent.scene_intent import SceneAgent
from utils.convert_image_to_base64 import get_base64_image

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

st.set_page_config(page_title="ShotSens", layout="wide", initial_sidebar_state="collapsed")
camera_base64 = get_base64_image("src/assets/Photo-Camera-PNG-Pic.png")


# Modern, sleek UI inspired by the reference design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main background - clean gradient */
    .stApp {
        background: linear-gradient(180deg, #fafbff 0%, #f0f4ff 100%);
    }
    
    /* Remove default padding */
    .main > div {
        padding-top: 0;
        padding-bottom: 3rem;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(139, 92, 246, 0.1);
        padding: 1rem 2.5rem;
        margin: -2rem -2rem 0 -2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 1px 3px rgba(139, 92, 246, 0.05);
    }
    
    .nav-logo {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    # .nav-logo-icon {
    #     font-size: 1.6rem;
    #     filter: drop-shadow(0 2px 4px rgba(139, 92, 246, 0.2));
    # }
    
    .nav-links {
        display: flex;
        gap: 2.5rem;
        align-items: center;
    }
    
    .nav-link {
        color: #475569;
        font-size: 0.95rem;
        font-weight: 500;
        text-decoration: none;
        transition: color 0.2s;
        position: relative;
    }
    
    .nav-link:hover {
        color: #8b5cf6;
    }
    
    .nav-link::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #8b5cf6, #6366f1);
        transition: width 0.2s;
    }
    
    .nav-link:hover::after {
        width: 100%;
    }
    
    /* Hero Section with Badge */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem 3rem 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%);
        border: 1.5px solid rgba(139, 92, 246, 0.2);
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #7c3aed;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1);
    }
    
    .hero-icon {
        width: 90px;
        height: 90px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 2rem auto;
        font-size: 2.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 4rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
        letter-spacing: -0.04em;
        line-height: 1.1;
        background: linear-gradient(135deg, #1e1b4b 0%, #4c1d95 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-title-accent {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        color: #475569;
        font-size: 1.15rem;
        font-weight: 400;
        margin: 0 0 1rem 0;
        line-height: 1.7;
        max-width: 750px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .hero-subtitle strong {
        color: #1e293b;
        font-weight: 600;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    
    .hero-feature {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .hero-feature::before {
        content: '●';
        color: #8b5cf6;
        font-size: 0.8rem;
    }
    
    /* Centered input container */
    .input-container {
        max-width: 600px;
        margin: 2rem auto;
        padding: 0 1.5rem;
    }
    /* Center and resize text area */
    .stTextArea {
        max-width: 920px;
        margin: 0 auto;
    }

    /* Style the text area box */
    .stTextArea textarea {
        border: 3.5px solid #667eea !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        background: white !important;
    }

    /* Focus effect */
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.12) !important;
    }

    
    /* Text area styling - Modern with gradient border */
    .stTextArea {
        margin-bottom: 1.5rem;
    }
    
    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        background-image: linear-gradient(white, white), 
                          linear-gradient(135deg, #93c5fd 0%, #a78bfa 50%, #c084fc 100%) !important;
        background-origin: border-box !important;
        background-clip: padding-box, border-box !important;
        border-radius: 16px !important;
        padding: 24px !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        color: #1e293b !important;
        transition: all 0.3s ease !important;
        line-height: 1.8 !important;
        min-height: 240px !important;
        resize: vertical !important;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.08) !important;
    }
    
    .stTextArea > div > div > textarea:hover {
        box-shadow: 0 6px 24px rgba(139, 92, 246, 0.15) !important;
        transform: translateY(-2px);
    }
    
    .stTextArea > div > div > textarea:focus {
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.2) !important;
        outline: none !important;
        transform: translateY(-2px);
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #94a3b8 !important;
        font-weight: 400 !important;
    }
    
    .stTextArea > div > div > textarea::selection {
        background: #ddd6fe !important;
        color: #1e1b4b !important;
    }
    
    /* Hide label */
    .stTextArea label {
        display: none !important;
    }
    
    /* Button container */
    .button-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 1.5rem;
    }
    
    /* Primary button - Analyze Scene */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.35) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button[kind="primary"]::before {
        content: '✨';
        margin-right: 0.5rem;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.45) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(-1px) !important;
    }
    
    /* Secondary button - Load Example */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #6366f1 !important;
        border: 2px solid #e0e7ff !important;
        border-radius: 12px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.1) !important;
        cursor: pointer !important;
    }
    
    .stButton > button[kind="secondary"]::before {
        content: '📄';
        margin-right: 0.5rem;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f5f3ff !important;
        border-color: #8b5cf6 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Results container */
    .results-container {
        max-width: 1200px;
        margin: 4rem auto 0 auto;
        padding: 0 1.5rem;
    }
    
    /* Section headers */
    .section-header {
        color: #1e293b;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        text-align: center;
    }
    
    /* Emotion/Confidence cards */
    .emotion-card {
        background: white;
        border: 2px solid #f0f4ff;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.08);
    }
    
    .emotion-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.15);
        border-color: #e0e7ff;
    }
    
    .emotion-card-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .emotion-badge {
        display: inline-block;
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        padding: 0.75rem 1.75rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    
    .confidence-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.75rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    /* Production detail cards - Enhanced gradient */
    .result-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3);
        border: none;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 200px;
        display: flex;
        flex-direction: column;
    }
    
    /* Animated gradient overlay */
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,255,255,0.08) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .result-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 32px rgba(139, 92, 246, 0.4);
    }
    
    .result-card-header {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85rem;
        font-weight: 800;
        margin: 0 0 1.25rem 0;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        position: relative;
        z-index: 1;
    }
    
    .result-card-content {
        color: rgba(255, 255, 255, 0.95);
        font-size: 0.95rem;
        line-height: 1.7;
        font-weight: 400;
        position: relative;
        z-index: 1;
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white !important;
        border: 2px solid #f0f4ff !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        transition: all 0.2s ease !important;
        padding: 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #fafbff !important;
        border-color: #e0e7ff !important;
    }
    
    .streamlit-expanderContent {
        background: #fafbff !important;
        border: 2px solid #f0f4ff !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 1.5rem !important;
    }
    
    /* Alert boxes */
    .stAlert {
        background: #eef2ff !important;
        border: 2px solid #c7d2fe !important;
        border-radius: 12px !important;
        color: #4338ca !important;
    }
    
    .stWarning {
        background: #fef3c7 !important;
        border: 2px solid #fcd34d !important;
        border-radius: 12px !important;
        color: #92400e !important;
    }
    
    .stError {
        background: #fee2e2 !important;
        border: 2px solid #fca5a5 !important;
        border-radius: 12px !important;
        color: #991b1b !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #8b5cf6, #6366f1);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #7c3aed, #4f46e5);
    }
    
    /* Columns */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Animation for results */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-card, .emotion-card {
        animation: slideIn 0.4s ease-out forwards;
    }
    .hero-icon-img {
        width: 150px;   /* change this */
        height: auto;  /* keeps aspect ratio */
        object-fit: contain;
    }
    
    .loader {
        border: 6px solid #f3f3f3;
        border-top: 6px solid #ff4b4b;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
        margin: auto;
        }
        @keyframes spin {
        100% { transform: rotate(360deg); }
        }
        .center {
        text-align: center;
        }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Top Navigation Bar
st.markdown("""
    <div class="top-nav">
        <div class="nav-logo">
            <span class="nav-logo-icon">🎬</span>
            ShotSens
        </div>
        <div class="nav-links">
            <a class="nav-link" href="#home">Home</a>
            <a class="nav-link" href="#features">Features</a>
            <a class="nav-link" href="#about">About</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Hero Section with Icon and Badge
st.markdown(f"""
    <div class="hero-section">
        <div class="hero-icon">
            <img src="data:image/png;base64,{camera_base64}" class="hero-icon-img">
        </div>
        <div class="hero-badge">
            ✨ AI-Powered Scene Analysis
        </div>
        <h1 class="hero-title">
            <span class="hero-title-accent">Multimodal Scene Intent & Visual Planning Engine</span>
        </h1>
        <p class="hero-subtitle">
            Transform screenplay scenes into detailed visual production insights with <strong>intelligent AI analysis</strong>. 
            Perfect for directors, cinematographers, and production designers.
        </p>
    </div>
""", unsafe_allow_html=True)


agent = SceneAgent()

# Centered Input Container
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Scene input text area
scene_text = st.text_area(
    "scene_input",
    height=240,
    placeholder="INT. HOSPITAL ROOM - NIGHT\n\nSHE laughs as HE jokes. Her hands tremble under the blanket.\n\nHE reaches for her hand, squeezing gently. The monitors beep softly in the background.",
    label_visibility="collapsed"
)

# Centered buttons below input
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    button_col1, button_col2 = st.columns(2)
    
    with button_col1:
        load_example = st.button("Show Scene Set", type="secondary", key="image", use_container_width=True)
    
    with button_col2:
        analyze_button = st.button("Analyze Scene", type="primary", key="analyze", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# Convert base64 → PIL image
def b64_to_pil(b64_string):
    img_bytes = base64.b64decode(b64_string)
    return Image.open(BytesIO(img_bytes))

if load_example:
    if scene_text.strip():
        with st.spinner("🎨 Generating visual scene setup..."):
            result = agent.run(scene_text)
            generated_imgs_b64 = agent.generate_image(result)

            if generated_imgs_b64:
                st.session_state["generated_image"] = generated_imgs_b64[0]
            else:
                st.warning("No image generated.")
    else:
        st.warning("Please enter a scene first.")

    st.rerun()


if "generated_image" in st.session_state:
    img_b64 = st.session_state["generated_image"]

    # HTML render (bypasses all PIL/Streamlit issues)
    st.markdown(
        f"""
        <div style='text-align:center;'>
            <img src="data:image/png;base64,{img_b64}" 
                 style="width:50%;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.2);" />
        </div>
        """,
        unsafe_allow_html=True
    )



def render_result(result):
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    # ---------- Emotional Analysis Section ----------
    st.markdown('<div class="section-header" style="margin-top: 3rem;">Emotional Analysis</div>', unsafe_allow_html=True)

    confidence_display = (
        f"{result.validated_confidence * 100:.0f}%"
        if result.validated_confidence is not None
        else "N/A"
    )

    if isinstance(result.narrative_reasoning, str):
        reasoning_text = result.narrative_reasoning
    elif isinstance(result.narrative_reasoning, list):
        reasoning_text = " ".join(result.narrative_reasoning)
    else:
        reasoning_text = "No reasoning available"


    col_spacer1, col_content, col_spacer2 = st.columns([0.5, 2, 0.5])

    with col_content:
        col_emotion, col_confidence = st.columns(2)

        with col_emotion:
            st.markdown(f"""
            <div class="emotion-card">
                <div class="emotion-card-label">Detected Emotion</div>
                <span class="emotion-badge">{result.emotion}</span>
            </div>
            """, unsafe_allow_html=True)

        with col_confidence:
            st.markdown(f"""
            <div class="emotion-card">
                <div class="emotion-card-label">Confidence Score</div>
                <span class="confidence-badge">{confidence_display}</span>
            </div>
            """, unsafe_allow_html=True)
            
    # Production Details Section 
    st.markdown('<div class="section-header" style="margin-top: 3.5rem; margin-bottom: 2rem;">Production Details</div>', unsafe_allow_html=True)

    # Safe props rendering
    if isinstance(result.props, list) and result.props:
        props_display = ", ".join(result.props)
    elif isinstance(result.props, str):
        props_display = result.props
    else:
        props_display = "None"


    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">CAMERA STYLE</div>
            <div class="result-card-content">{result.camera_style}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">VISUAL MOOD</div>
            <div class="result-card-content">{result.visual_mood}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">COMPOSITION</div>
            <div class="result-card-content">{result.composition}</div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">SET DESIGN</div>
            <div class="result-card-content">{result.set_design}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">PROPS</div>
            <div class="result-card-content">{props_display}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-card-header">BLOCKING</div>
            <div class="result-card-content">{result.blocking}</div>
        </div>
        """, unsafe_allow_html=True)


    # col_full = st.columns(1)

    # with col_full:
    #     st.markdown(f"""
    #     <div class="result-card">
    #         <div class="result-card-header">NARRATIVE REASONING</div>
    #         <div class="result-card-content">
    #             {reasoning_text[:200]}
    #             {'...' if len(reasoning_text) > 200 else ''}
    #         </div>
    #     </div>
    #     """, unsafe_allow_html=True)


    st.markdown("<br><br>", unsafe_allow_html=True)

    with st.expander("📋 View Complete Analysis"):
        st.markdown(f"**Full Narrative Reasoning:** {result.narrative_reasoning}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"**Props:** {props_display}")
        st.markdown(f"**Costumes:** {result.costumes}")
        st.markdown("<br>", unsafe_allow_html=True)
        st.json(result.model_dump())

    st.markdown('</div>', unsafe_allow_html=True)

   
# Analysis execution
if analyze_button:
    if scene_text and scene_text.strip():
        loader = st.empty()
        loader.markdown("""
        <div class="center">
            <div class="loader"></div>
            <p>🎬 Analyzing your scene...</p>
        </div>
        """, unsafe_allow_html=True)

        try:
            result = agent.run(scene_text)
            loader.empty()
            render_result(result)
        except Exception as e:
            loader.empty()
            st.error(f"Analysis Error: {str(e)}")
