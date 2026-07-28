import streamlit as st
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="LinkedIn Post Generator (HITL)")

# ------------------------------------------------------------------
# LangGraph setup
# ------------------------------------------------------------------

writer_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)


class State(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]
    draft: str
    review_feedback: str
    is_approved: bool
    attempt: int


WRITER_SYSTEM_PROMPT = (
    "You are an expert LinkedIn content writer. Write engaging, professional "
    "LinkedIn posts about the given topic. "
    "Rules: strong hook in the first line, one clear takeaway, easy to skim "
    "with short paragraphs, roughly 150-200 words, end with an engaging "
    "question or CTA, no hashtags. "
    "If you receive feedback on a previous draft, address every point carefully."
)


def writer_node(state: State) -> dict:
    """Writes (or rewrites) the LinkedIn post."""
    attempt = state.get("attempt", 0) + 1
    topic = state["topic"]
    previous_feedback = state.get("review_feedback", "")

    if attempt == 1:
        user_message = f"Write a LinkedIn post on this topic: {topic}"
    else:
        user_message = (
            f"Your previous draft on '{topic}' was rejected.\n\n"
            f"Reviewer feedback:\n{previous_feedback}\n\n"
            f"Write a NEW improved LinkedIn post that fixes every issue mentioned."
        )

    messages = [("system", WRITER_SYSTEM_PROMPT), ("human", user_message)]
    response = writer_llm.invoke(messages)

    return {
        "draft": response.content,
        "attempt": attempt
    }


def human_review_node(state: State) -> dict:
    """Pauses the graph and waits for the human to approve or give feedback."""
    human_response = interrupt({
        "draft": state["draft"],
        "attempt": state["attempt"],
        "instruction": "Type 'approved' to accept, or type your feedback to request a rewrite."
    })

    response = human_response.strip()

    if response.lower() in ["approved", "approve", "yes", "ok", "good"]:
        return {
            "is_approved": True,
            "review_feedback": "Approved by human."
        }
    else:
        return {
            "is_approved": False,
            "review_feedback": response
        }


def should_stop_looping(state: State):
    if state["is_approved"]:
        return END
    if state["attempt"] >= 3:
        return END
    return "writer"


def build_graph():
    graph = StateGraph(State)

    graph.add_node("writer", writer_node)
    graph.add_node("human_review", human_review_node)

    graph.add_edge(START, "writer")
    graph.add_edge("writer", "human_review")

    graph.add_conditional_edges(
        "human_review",
        should_stop_looping,
        {
            "writer": "writer",
            END: END,
        },
    )

    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


def get_initial_state(topic: str) -> State:
    return {
        "topic": topic,
        "messages": [],
        "draft": "",
        "review_feedback": "",
        "is_approved": False,
        "attempt": 0,
    }


# ------------------------------------------------------------------
# Streamlit frontend (basic widgets only)
# ------------------------------------------------------------------

st.title("LinkedIn Post Generator")
st.write("This tool drafts a LinkedIn post, shows it to you for review, and rewrites it based on your feedback (max 3 attempts).")

if "app" not in st.session_state:
    st.session_state.app = build_graph()

if "config" not in st.session_state:
    st.session_state.config = {"configurable": {"thread_id": "linkedin_session_1"}}

if "result" not in st.session_state:
    st.session_state.result = None

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False


topic = st.text_input("What topic do you want a LinkedIn post about?")

if st.button("Generate Post"):
    if topic.strip() == "":
        st.warning("Please enter a topic first.")
    else:
        st.session_state.started = True
        st.session_state.finished = False
        initial_state = get_initial_state(topic.strip())
        with st.spinner("Writing draft..."):
            st.session_state.result = st.session_state.app.invoke(
                initial_state, config=st.session_state.config
            )

result = st.session_state.result

if st.session_state.started and result is not None:

    if "__interrupt__" in result:
        interrupt_data = result["__interrupt__"][0].value

        st.subheader(f"Draft for your review (Attempt {interrupt_data['attempt']})")
        st.text_area("Draft", value=interrupt_data["draft"], height=250, disabled=True)
        st.write(interrupt_data["instruction"])

        feedback = st.text_input("Your response (type 'approved' or give feedback)", key="feedback_input")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Approve"):
                with st.spinner("Finalizing..."):
                    st.session_state.result = st.session_state.app.invoke(
                        Command(resume="approved"), config=st.session_state.config
                    )

        with col2:
            if st.button("Submit Feedback"):
                if feedback.strip() == "":
                    st.warning("Please type some feedback first.")
                else:
                    with st.spinner("Rewriting draft..."):
                        st.session_state.result = st.session_state.app.invoke(
                            Command(resume=feedback.strip()), config=st.session_state.config
                        )

    else:
        st.session_state.finished = True

    if st.session_state.finished:
        st.subheader("Final LinkedIn Post")
        st.text_area("Final Post", value=result["draft"], height=250, disabled=True)
        st.write(f"Total attempts: {result['attempt']}")
        st.write(f"Approved by human: {result['is_approved']}")