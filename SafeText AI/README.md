# Content Safety Analyzer

A Streamlit app powered by LangGraph that analyzes a piece of text using
three **parallel** LLM-based checks (fan-out from a single `START` node,
merged back into one state via a reducer):

- **Toxicity / Hate Speech** — profanity, aggression, hate speech
- **Copyright / Originality Risk** — plagiarism, trademark risk
- **Cultural / Regional Sensitivity** — political landmines, cultural insensitivity

Each check returns a score from 0 (safe) to 100 (high risk), scored by
Groq's `llama-3.3-70b-versatile` model.

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

## Usage

1. Check **"Use sample script"** to try the built-in example, or paste/type your own text.
2. Click **Analyze**.
3. The app runs all three checks in parallel via LangGraph and displays:
   - A label and risk level (Low / Medium / High) for each check
   - A progress bar for each score
   - The raw scores dictionary

## Notes

- The UI uses only basic Streamlit widgets (`text_area`, `checkbox`, `button`,
  `write`, `progress`, `spinner`) — no advanced/experimental features.
- The graph has no shared/sequential dependency between branches — all three
  nodes run off of `START` and write to the same `safety_scores` state key,
  which is merged via a custom reducer (`merge_score_dicts`).

## Suggested repository name

```
content-safety-analyzer-langgraph
```

## Suggested git commit message

```
feat: add Streamlit UI for parallel content safety analyzer (toxicity, copyright, cultural sensitivity)
```