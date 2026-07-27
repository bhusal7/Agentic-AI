# LinkedIn Post Generator

A Streamlit app that uses a LangGraph agent workflow to draft, self-review,
and iteratively improve a LinkedIn post on any topic you give it.

## How it works

The app builds a small agentic graph with two LLMs playing distinct roles:

- **Writer** (`mistral-small-latest` via `ChatMistralAI`): drafte post.
  It can call a Tavily web search tool first if the topic needs current
  information or stats.
- **Reviewer** (`llama-3.3-70b-versatile` via `ChatGroq`): strictly evaluates
  the draft against a checklist (hook, one clear takeaway, skimmability,
  word count, CTA/question ending, tone, no hashtags) and returns
  `APPROVED` or `REJECTED` with feedback.

If the reviewer rejects the draft, the writer gets the feedback and tries
again. This loops until the post is approved or a maximum of 3 attempts is
reached.

### Graph flow

```
START -> writer -> (tools? -> reviewer) or (extract_draft -> reviewer)
reviewer -> (approved or max attempts reached -> END) or (writer)
```

## Requirements

- Python 3.9+
- API keys for:
  - **Mistral AI** (writer LLM)
  - **Groq** (reviewer LLM)
  - **Tavily** (web search tool)

## Setup

1. Clone/download this project and move into its folder.

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install streamlit langgraph langchain-groq langchain-mistralai langchain-tavily python-dotenv
   ```

4. Create a `.env` file in the project root with your API keys:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Running the app

```bash
streamlit run app.py
```

This opens the app in your browser (usually at `http://localhost:8501`).

## Using the app

1. Enter a topic in the text box (e.g. "the future of remote work").
2. Click **Generate Post**.
3. Wait while the agent writes, (optionally searches the web), and
   reviews the draft — repeating up to 3 attempts if needed.
4. The final post is displayed, along with the number of attempts used,
   whether it was approved, and the reviewer's last feedback if it wasn't
   approved within the attempt limit.

## Notes

- Console-style logs (verdicts, feedback, generated post) are still printed
  to the terminal running Streamlit, in addition to being shown in the UI.
- The app logic (state, nodes, routing, and graph structure) is unchanged
  from the original CLI script — only the input/output layer was adapted
  to Streamlit.