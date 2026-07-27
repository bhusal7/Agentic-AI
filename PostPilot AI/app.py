import streamlit as st
from main import app

st.set_page_config(
    page_title="LinkedIn Post Studio",
    page_icon="💼",
    layout="wide"
)

st.title("💼 LinkedIn Post Studio")
st.caption(
    "Generate professional LinkedIn posts using LangGraph, Mistral AI, "
    "Groq, and Tavily Search."
)

st.divider()

topic = st.text_area(
    "Enter your topic",
    placeholder="Example: Why AI won't replace software engineers...",
    height=120,
)

generate = st.button(
    "🚀 Generate LinkedIn Post",
    use_container_width=True
)

if generate:

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Generating your LinkedIn post..."):

        initial_state = {
            "topic": topic,
            "messages": [],
            "draft": "",
            "review_feedback": "",
            "is_approved": False,
            "attempt": 0,
        }

        final_state = app.invoke(initial_state)

    st.success("Generation Complete!")

    st.subheader("📄 Final LinkedIn Post")

    st.write(final_state["draft"])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Iterations",
            final_state["attempt"]
        )

    with col2:
        st.metric(
            "Approved",
            "✅ Yes" if final_state["is_approved"] else "❌ No"
        )

    st.subheader("📝 Reviewer Feedback")

    st.info(final_state["review_feedback"])

    st.download_button(
        "⬇ Download Post",
        final_state["draft"],
        file_name="linkedin_post.txt"
    )