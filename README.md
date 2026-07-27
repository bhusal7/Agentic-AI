# 🎓 College Assistant

A chat-based college assistant built with **Streamlit**, **LangGraph**, and **Groq's Llama 3.3 70B**. It automatically classifies each student question as **academic**, **fee-related**, or **general**, retrieves the right context via RAG from your college PDFs, and answers in a way personalized to the student's programme (BCA / BBA / B.Com (H)).

---

## ✨ Features

- **Automatic query routing** — an LLM classifier node decides whether a question is about academics, fees, or general chit-chat, and routes it to the right retriever.
- **RAG over your own PDFs** — academics handbook and fee structure documents are chunked, embedded, and indexed with FAISS for accurate, grounded answers.
- **Programme-aware answers** — responses are tailored to the student's selected programme (e.g. highlighting BCA-specific fee figures instead of BBA's).
- **Chat UI** — full conversational interface with message history, powered by Streamlit's native chat components.
- **Upload your own PDFs** — no need to hardcode file paths; swap in different handbooks/fee sheets from the sidebar at any time.
- **Graceful fallback** — if a PDF isn't available, that category falls back to the LLM's general knowledge instead of erroring out.

---

## 🗂️ Project structure

```
.
├── app.py                   # Streamlit app (this is the whole application)
├── academics_handbook.pdf   # optional — default academic knowledge source
├── fee_structure.pdf        # optional — default fee knowledge source
├── .env                     # holds your GROQ_API_KEY
└── README.md
```

You don't need the two PDFs to be present on disk — you can upload them from the sidebar instead.

---

## ⚙️ Requirements

- Python 3.10+
- A [Groq API key](https://console.groq.com/keys)

### Install dependencies

```bash
pip install streamlit langgraph langchain-groq langchain-community \
            langchain-text-splitters langchain-huggingface \
            faiss-cpu pypdf sentence-transformers python-dotenv
```

Or, save this as `requirements.txt` and run `pip install -r requirements.txt`:

```
streamlit
langgraph
langchain-groq
langchain-community
langchain-text-splitters
langchain-huggingface
faiss-cpu
pypdf
sentence-transformers
python-dotenv
```

---

## 🔑 Configuration

Create a `.env` file in the same folder as `app.py`:

```
GROQ_API_KEY=your_groq_api_key_here
```

The app will show a warning banner in the UI if this key isn't set.

---

## ▶️ Running the app

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

1. Pick your programme in the sidebar (BCA, BBA, or B.Com (H)).
2. Optionally upload your own `academics_handbook.pdf` and/or `fee_structure.pdf` — otherwise the app looks for files with those exact names next to `app.py`.
3. Start chatting in the main window. Ask about attendance policy, exam rules, tuition fees, scholarships, or just say hi.
4. Use **🗑️ Clear chat** in the sidebar to reset the conversation.

---

## 🧠 How it works

The app builds a small [LangGraph](https://langchain-ai.github.io/langgraph/) state graph:

```
START → classifier ──┬─→ academic_rag ─┐
                      ├─→ fee_rag      ─┼─→ response → END
                      └─→ general      ─┘
```

1. **classifier** — an LLM call labels the latest message as `academic`, `fee`, or `general`.
2. **academic_rag / fee_rag** — retrieve the top-matching chunks from the relevant FAISS index built from your PDF(s).
3. **general** — skips retrieval entirely for greetings or unrelated questions.
4. **response** — generates the final answer, injecting retrieved context (if any) and the student's programme so figures/policies relevant to them are highlighted.

Embeddings use `sentence-transformers/all-MiniLM-L6-v2` (via `langchain-huggingface`), and generation uses Groq's `llama-3.3-70b-versatile`.

---

## 🛠️ Notes & limitations

- Each question is currently answered independently — the graph doesn't carry multi-turn memory into the LLM's context beyond what's shown in the chat window (matching the original CLI script's behavior). Extending this to true multi-turn memory would mean passing accumulated `messages` into each `app.invoke(...)` call or adding a LangGraph checkpointer.
- PDF indexing is cached per file (by content/size for uploads, by path + modified time for local files), so re-running the app won't rebuild the FAISS index unless the file actually changes.
- If a PDF is missing and not uploaded, that category's questions still get answered — just from the LLM's general knowledge rather than your documents.