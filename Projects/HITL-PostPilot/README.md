# LinkedIn Post Generator (Human-in-the-Loop) — Streamlit Edition

A single-file Streamlit app powered by LangGraph that drafts LinkedIn posts,
pauses for human review, and rewrites the post based on your feedback (up to
3 attempts).

## How it works

1. You enter a topic.
2. A **writer** step (Groq's `llama-3.3-70b-versatile`) drafts a LinkedIn post.
3. The graph pauses at a **human review** step and shows you the draft.
4. You either:
   - Click **Approve** to accept the draft, or
   - Type feedback and click **Submit Feedback** to request a rewrite.
5. Steps 2–4 repeat until you approve the post or 3 attempts are reached.
6. The final post is shown along with the number of attempts and approval status.

## Files

```
app.py        # Streamlit app + LangGraph logic (single file)
README.md
```

## Setup

1. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install streamlit langgraph langchain-groq python-dotenv
   ```

3. **Set your Groq API key**

   Create a `.env` file in the same folder as `app.py`:

   ```
   GROQ_API_KEY=your_api_key_here
   ```

## Running the app

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`) in your browser.

## Notes

- The frontend uses only basic Streamlit widgets (`text_input`, `text_area`,
  `button`, `write`, `spinner`, `columns`) — no advanced/experimental features.
- Conversation state lives in `st.session_state`, and the LangGraph workflow
  uses an in-memory checkpointer (`MemorySaver`), so state resets when the
  app restarts or the page is refreshed.
- To start over with a new topic, refresh the page.