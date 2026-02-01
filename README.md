# ShotSens - Multimodal Scene Intent & Visual Planning Engine

> **"From Script to Screen: visualise the unwritten."**

ShotSens is an AI-powered engine designed to bridge the gap between written scripts and visual production. It extracts the implicit creative intent—emotion, mood, and visual tone—from a screenplay and converts it into structured visual planning signals and generated imagery.

## 🎬 Problem Statement
Scripts describe actions and dialogue, but **scene intent** including emotion, mood, and visual tone is often implicit and not directly stated. This ambiguity can lead to misinterpretation during the pre-production phase.

**ShotSens** solves this by building an AI system that:
1.  **Extracts creative intent** from raw script text.
2.  **Converts it into structured data** (camera angles, lighting, set design).
3.  **Generates visual representations** to aid storyboard generators, directors’ assistants, and previz systems.

---

## 📂 Deployed link 
- https://shotsens-cine-ai-hackfest.streamlit.app/

---

## ✨ Features

### 1. multimodal Analysis Modes
*   **🎬 Director's Cut**: Deep-dive analysis providing detailed breakdowns of:
    *   **Camera Style**: Angles, movement, and lens choices.
    *   **Visual Mood**: Lighting, color palette, and atmosphere.
    *   **Composition**: Framing and focus emphasis.
    *   **Blocking**: Actor movement and positioning.
*   **📝 Production Notes**: A streamlined output focusing on logistical elements like props, costumes, and set design requirements.

### 2. Intelligent Visualization
*   **AI Image Generation**: Automatically generates a visual representation of the scene based on the extracted intent, giving an immediate "look and feel" reference.
*   **Confidence Validation**: Uses a multi-pass validation system to ensure the AI's confidence in its analysis is reliable and stable.

### 3. Cinematic UI
*   Built with **Streamlit**, featuring a modern, responsive interface.
*   **Dark/Light Mode**: Optimized for readability with a premium aesthetic.
*   **Interactive Elements**: Toggle between analysis modes, view confidence scores, and expand detailed JSON outputs.

---

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) (Python-based UI)
*   **AI Logic**: [LangChain](https://www.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/)
*   **LLM Provider**: [Google Gemini](https://ai.google.dev/) (`langchain-google-genai`)
*   **Data Validation**: [Pydantic](https://docs.pydantic.dev/) for structured output parsing.
*   **Image Generation**: Integrated AI image generation (internal service).

---

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.10+
*   Google Gemini API Key (likely stored in `.env`)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd shotsens
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your API keys:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## 💻 Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

1.  **Enter Scene Text**: Paste a scene from your screenplay into the input box.
    *   *Example: "INT. HOSPITAL ROOM - NIGHT..."*
2.  **Select Mode**: Choose between **Director's Cut** (Detailed) or **Production Notes** (Logistical).
3.  **Analyze**: Click **"Analyze Scene"**.
4.  **View Results**:
    *   See the **Generated Image** representing the scene.
    *   Review the **Emotion & Confidence** scores.
    *   Explore the structured **Visual Breakdown** cards.
    *   Expand **"View Complete Analysis"** to see the raw JSON data.

---

## 📂 Project Structure

```
shotsens/
├── app.py                  # Main Streamlit application entry point
├── requirements.txt        # Project dependencies
├── utils/                  # Helper functions
│   └── convert_image_to_base64.py
└── src/
    ├── main.py
    ├── agent/              # Core AI Agent logic
    │   ├── scene_intent.py # Main agent orchestration
    │   └── prompt_builder.py
    ├── schema/             # Pydantic models for structured output
    │   └── scene_schema.py
    ├── image_generator/    # Image generation logic
    ├── confidence/         # Confidence validation logic
    └── services/           # LLM service configuration
```
---

## 📂 Demo

---


