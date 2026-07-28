import streamlit as st
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

st.set_page_config(page_title="Content Safety Analyzer", page_icon="🛡️")

# ------------------------------------------------------------------
# LLM
# ------------------------------------------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)


def merge_score_dicts(existing: dict, newupdate: dict) -> dict:
    if existing is None:
        return newupdate
    return {**existing, **newupdate}


# ------------------------------------------------------------------
# State
# ------------------------------------------------------------------

class AnalyzerState(TypedDict):
    raw_text: str
    # concept of reducers
    safety_scores: Annotated[dict[str, int], merge_score_dicts]


# ------------------------------------------------------------------
# Nodes (run in parallel branches from START)
# ------------------------------------------------------------------

def toxicity_node(state: AnalyzerState) -> dict:
    prompt = (
        "Analyze the following text for profanity, aggression, hate speech, or toxicity. "
        "Provide a score from 0 to 100, where 0 means perfectly clean and 100 means highly toxic. "
        "Return ONLY the plain integer number, nothing else.\n\n"
        f"Text:\n{state['raw_text']}"
    )
    response = llm.invoke(prompt)
    try:
        score = int(response.content.strip())
    except ValueError:
        score = 0

    return {"safety_scores": {"toxicity_level": score}}


def copyright_node(state: AnalyzerState) -> dict:
    prompt = (
        "Analyze the following text. Judge if it sounds heavily plagiarized, unoriginal, "
        "or presents a corporate trademark risk. Provide a score from 0 to 100, "
        "where 0 means entirely original and 100 means high risk. "
        "Return ONLY the plain integer number, nothing else.\n\n"
        f"Text:\n{state['raw_text']}"
    )
    response = llm.invoke(prompt)
    try:
        score = int(response.content.strip())
    except ValueError:
        score = 0

    return {"safety_scores": {"copyright_risk": score}}


def culture_node(state: AnalyzerState) -> dict:
    prompt = (
        "Analyze the following text for regional sensitivities, political landmines, "
        "or cultural insensitivity that might offend a global audience. Provide a score from 0 to 100, "
        "where 0 means completely safe and 100 means highly offensive. "
        "Return ONLY the plain integer number, nothing else.\n\n"
        f"Text:\n{state['raw_text']}"
    )
    response = llm.invoke(prompt)
    try:
        score = int(response.content.strip())
    except ValueError:
        score = 0

    return {"safety_scores": {"cultural_insensitivity": score}}


# ------------------------------------------------------------------
# Graph
# ------------------------------------------------------------------

def build_graph():
    builder = StateGraph(AnalyzerState)

    builder.add_node("toxicity_node", toxicity_node)
    builder.add_node("copyright_check", copyright_node)
    builder.add_node("culture_node", culture_node)

    builder.add_edge(START, "toxicity_node")
    builder.add_edge(START, "copyright_check")
    builder.add_edge(START, "culture_node")

    builder.add_edge("toxicity_node", END)
    builder.add_edge("copyright_check", END)
    builder.add_edge("culture_node", END)

    return builder.compile()


SAMPLE_SCRIPT = """Yo guys! Welcome back to the stream. Today I am going to show you how to hack into
your friend's system using a script I copied directly from an online forum.
Honestly, traditional security protocols are absolute garbage and anyone still using
them is an absolute idiot. Let's dive into the code!"""

SCORE_LABELS = {
    "toxicity_level": "Toxicity / Hate Speech",
    "copyright_risk": "Copyright / Originality Risk",
    "cultural_insensitivity": "Cultural / Regional Sensitivity",
}


def risk_level(score: int) -> str:
    if score < 34:
        return "Low"
    if score < 67:
        return "Medium"
    return "High"


# ------------------------------------------------------------------
# Streamlit UI (basic widgets only)
# ------------------------------------------------------------------

st.title("Content Safety Analyzer")
st.write(
    "Runs three parallel checks on a piece of text using LangGraph: "
    "toxicity, copyright/originality risk, and cultural sensitivity."
)

if "app" not in st.session_state:
    st.session_state.app = build_graph()

if "scores" not in st.session_state:
    st.session_state.scores = None

use_sample = st.checkbox("Use sample script")

if use_sample:
    raw_text = st.text_area("Text to analyze", value=SAMPLE_SCRIPT, height=180)
else:
    raw_text = st.text_area("Text to analyze", value="", height=180, placeholder="Paste or type text here...")

if st.button("Analyze"):
    if raw_text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        initial_state = {
            "raw_text": raw_text.strip(),
            "safety_scores": {}
        }
        with st.spinner("Running toxicity, copyright, and cultural analysis in parallel..."):
            final_state = st.session_state.app.invoke(initial_state)
        st.session_state.scores = final_state["safety_scores"]

if st.session_state.scores:
    st.subheader("Results")

    for key, label in SCORE_LABELS.items():
        score = st.session_state.scores.get(key)
        if score is None:
            continue
        st.write(f"**{label}**: {score}/100 ({risk_level(score)})")
        st.progress(min(max(score, 0), 100) / 100)

    st.write("Raw scores:")
    st.write(st.session_state.scores)