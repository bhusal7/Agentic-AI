import os
import tempfile
from typing import TypedDict, Annotated

import streamlit as st
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="College Assistant",
    page_icon="🎓",
    layout="centered",
)

PROGRAMME_OPTIONS = {
    "BCA": "BCA",
    "BBA": "BBA",
    "B.Com (H)": "B.Com (H)",
}

DEFAULT_ACADEMIC_PDF = "academics_handbook.pdf"
DEFAULT_FEE_PDF = "fee_structure.pdf"


# --------------------------------------------------------------------------
# Step 1 - Cached resources (embeddings model, retrievers, LLM)
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)


@st.cache_resource(show_spinner="Indexing PDF…")
def build_retriever(pdf_path: str, file_hash: str):
    """file_hash is only used as a cache key so re-uploaded files rebuild the index."""
    embeddings = get_embeddings()
    loader = PyPDFLoader(pdf_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(document)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})


def _resolve_pdf_path(uploaded_file, default_path: str):
    """Return (path, hash) for either an uploaded file or the default path on disk."""
    if uploaded_file is not None:
        suffix = os.path.splitext(uploaded_file.name)[1] or ".pdf"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(uploaded_file.getvalue())
        tmp.close()
        return tmp.name, f"upload:{uploaded_file.name}:{len(uploaded_file.getvalue())}"

    if os.path.exists(default_path):
        return default_path, f"default:{default_path}:{os.path.getmtime(default_path)}"

    return None, None


# --------------------------------------------------------------------------
# Step 2 - Graph state
# --------------------------------------------------------------------------
class State(TypedDict):
    programme: str
    messages: Annotated[list, add_messages]
    query_type: str
    retrived_context: str


# --------------------------------------------------------------------------
# Step 3 - Nodes
# --------------------------------------------------------------------------
def make_classifier_node(llm):
    def classifier_node(state: State) -> dict:
        last_message = state["messages"][-1].content

        prompt = (
            "Classify the following student query into exactly one category: "
            "'academic', 'fee', or 'general'.\n\n"
            "Use 'academic' for questions about attendance, exams, grading, credits, "
            "promotion, course structure, summer training, or degree requirements.\n"
            "Use 'fee' for questions about tuition, payment, refund, late charges, "
            "scholarships, or any money-related topic.\n"
            "Use 'general' for greetings, casual talk, or anything not related to "
            "the college rules or fee.\n\n"
            f"Query: {last_message}\n\n"
            "Return only one word: academic, fee, or general."
        )

        response = llm.invoke(prompt)
        category = response.content.strip().lower()

        if "academic" in category:
            category = "academic"
        elif "fee" in category:
            category = "fee"
        else:
            category = "general"

        return {"query_type": category}

    return classifier_node


def make_academic_rag_node(retriever):
    def academic_rag_node(state: State) -> dict:
        query = state["messages"][-1].content
        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"retrived_context": context}

    return academic_rag_node


def make_fee_rag_node(retriever):
    def fee_rag_node(state: State) -> dict:
        query = state["messages"][-1].content
        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"retrived_context": context}

    return fee_rag_node


def general_node(state: State) -> dict:
    return {"retrived_context": "NO_RETRIEVAL_NEEDED"}


def make_response_node(llm):
    def response_node(state: State) -> dict:
        query = state["messages"][-1].content
        programme = state.get("programme", "Unknown")
        context = state["retrived_context"]

        if context == "NO_RETRIEVAL_NEEDED":
            prompt = (
                f"You are a friendly college assistant talking to a {programme} student. "
                f"Answer this question using your own general knowledge:\n\n{query}"
            )
        else:
            prompt = (
                f"You are a college assistant helping a {programme} student. "
                f"Use the following context from the official college documents to answer "
                f"the question accurately. If the context mentions specific figures for "
                f"different programmes, highlight the one relevant to {programme} if possible.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {query}\n\n"
                f"Give a clear, friendly, and precise answer."
            )

        response = llm.invoke(prompt)
        return {"messages": [("ai", response.content.strip())]}

    return response_node


# --------------------------------------------------------------------------
# Step 4 - Router
# --------------------------------------------------------------------------
def route_query(state: State):
    if state["query_type"] == "academic":
        return "academic_rag"
    elif state["query_type"] == "fee":
        return "fee_rag"
    else:
        return "general"


# --------------------------------------------------------------------------
# Step 5 - Build the graph
# --------------------------------------------------------------------------
@st.cache_resource(show_spinner="Building the assistant graph…")
def build_graph(_academic_retriever, _fee_retriever, academic_key: str, fee_key: str):
    """The trailing *_key args exist purely so Streamlit's cache invalidates
    when a new PDF is uploaded (retriever objects themselves aren't hashable)."""
    llm = get_llm()

    graph = StateGraph(State)

    graph.add_node("classifier", make_classifier_node(llm))
    graph.add_node("academic_rag", make_academic_rag_node(_academic_retriever))
    graph.add_node("fee_rag", make_fee_rag_node(_fee_retriever))
    graph.add_node("general", general_node)
    graph.add_node("response", make_response_node(llm))

    graph.add_edge(START, "classifier")
    graph.add_conditional_edges("classifier", route_query)
    graph.add_edge("academic_rag", "response")
    graph.add_edge("fee_rag", "response")
    graph.add_edge("general", "response")
    graph.add_edge("response", END)

    return graph.compile()


# --------------------------------------------------------------------------
# Streamlit UI
# --------------------------------------------------------------------------
st.title("🎓 College Assistant")
st.caption("Ask about academics, fees, or anything else — I'll route your question automatically.")

if not os.environ.get("GROQ_API_KEY"):
    st.warning(
        "No `GROQ_API_KEY` found in the environment. Add it to a `.env` file "
        "or your environment variables before chatting.",
        icon="⚠️",
    )

with st.sidebar:
    st.header("Setup")

    programme = st.selectbox(
        "Which programme are you in?",
        options=list(PROGRAMME_OPTIONS.keys()),
        index=0,
    )

    st.divider()
    st.subheader("Knowledge base")
    st.caption(
        "Uses `academics_handbook.pdf` and `fee_structure.pdf` from the app's folder "
        "by default. You can upload your own copies below instead."
    )
    academic_upload = st.file_uploader("Academics handbook (PDF)", type=["pdf"], key="academic_upload")
    fee_upload = st.file_uploader("Fee structure (PDF)", type=["pdf"], key="fee_upload")

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.pop("chat_history", None)
        st.rerun()

# Resolve PDF paths (upload takes precedence over default file on disk)
academic_path, academic_key = _resolve_pdf_path(academic_upload, DEFAULT_ACADEMIC_PDF)
fee_path, fee_key = _resolve_pdf_path(fee_upload, DEFAULT_FEE_PDF)

missing = []
if academic_path is None:
    missing.append(f"`{DEFAULT_ACADEMIC_PDF}`")
if fee_path is None:
    missing.append(f"`{DEFAULT_FEE_PDF}`")

if missing:
    st.info(
        "Missing " + " and ".join(missing) + ". Upload the file(s) in the sidebar, "
        "or place them next to `app.py`, to enable academic/fee retrieval. "
        "General questions will still work.",
        icon="📄",
    )

# Build retrievers only for files that are available
academic_retriever = build_retriever(academic_path, academic_key) if academic_path else None
fee_retriever = build_retriever(fee_path, fee_key) if fee_path else None

# If a PDF is missing, fall back to a retriever-less node that still lets the graph run
if academic_retriever is None:
    def _academic_rag_node_fallback(state: State) -> dict:
        return {"retrived_context": "NO_RETRIEVAL_NEEDED"}
    academic_node_override = _academic_rag_node_fallback
else:
    academic_node_override = None

if fee_retriever is None:
    def _fee_rag_node_fallback(state: State) -> dict:
        return {"retrived_context": "NO_RETRIEVAL_NEEDED"}
    fee_node_override = _fee_rag_node_fallback
else:
    fee_node_override = None

# Build (or fetch cached) graph app
if academic_retriever is not None and fee_retriever is not None:
    app = build_graph(academic_retriever, fee_retriever, academic_key, fee_key)
else:
    # Build a graph with fallback nodes when one or both PDFs are unavailable
    llm = get_llm()
    graph = StateGraph(State)
    graph.add_node("classifier", make_classifier_node(llm))
    graph.add_node(
        "academic_rag",
        academic_node_override or make_academic_rag_node(academic_retriever),
    )
    graph.add_node("fee_rag", fee_node_override or make_fee_rag_node(fee_retriever))
    graph.add_node("general", general_node)
    graph.add_node("response", make_response_node(llm))
    graph.add_edge(START, "classifier")
    graph.add_conditional_edges("classifier", route_query)
    graph.add_edge("academic_rag", "response")
    graph.add_edge("fee_rag", "response")
    graph.add_edge("general", "response")
    graph.add_edge("response", END)
    app = graph.compile()

# --------------------------------------------------------------------------
# Chat state & display
# --------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of ("human"/"ai", text) tuples

for role, text in st.session_state.chat_history:
    with st.chat_message("user" if role == "human" else "assistant"):
        st.markdown(text)

user_query = st.chat_input(f"Ask something as a {PROGRAMME_OPTIONS[programme]} student…")

if user_query:
    st.session_state.chat_history.append(("human", user_query))
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = app.invoke(
                    {
                        "programme": PROGRAMME_OPTIONS[programme],
                        "messages": [("human", user_query)],
                    }
                )
                answer = result["messages"][-1].content
            except Exception as exc:  # surfaces API/key/network errors nicely in the UI
                answer = f"Sorry, something went wrong: {exc}"
        st.markdown(answer)

    st.session_state.chat_history.append(("ai", answer))