# 💼 LinkedIn Post Studio

An AI-powered LinkedIn content generation application built using **LangGraph**, **LangChain**, **Mistral AI**, **Groq**, **Tavily Search**, and **Streamlit**.

The application automatically writes, reviews, and improves LinkedIn posts through an iterative multi-agent workflow until the content is publication-ready.

---

# Features

- ✍️ AI LinkedIn Post Writer
- 🌐 Web Search using Tavily
- 🤖 Multi-Agent Workflow
- 🔄 Automatic Draft Refinement
- 📝 AI Reviewer
- ✅ Quality Approval System
- 🎯 Professional LinkedIn Writing
- 📥 Download Generated Post
- 💻 Streamlit Interface

---

# Tech Stack

- Python
- LangGraph
- LangChain
- Streamlit
- Mistral AI
- Groq
- Tavily Search API
- python-dotenv

---

# Workflow

```text
User Topic
      │
      ▼
 Writer Agent
      │
      ▼
Need Web Search?
   │        │
 Yes       No
 │          │
 ▼          ▼
Tool      Draft
 │          │
 └────► Reviewer Agent
              │
              ▼
 Approved?
   │        │
 Yes       No
 │          │
 ▼          ▼
 Finish   Rewrite
              │
              └─────────────► Writer
```

---

# Project Structure

```text
LinkedIn-Post-Studio/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env
└── assets/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/LinkedIn-Post-Studio.git
```

Move inside the project

```bash
cd LinkedIn-Post-Studio
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_key
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
```

---

# Run the Application

```bash
streamlit run app.py
```

---

# Example

**Input**

```
Machine Learning is Dead
```

**Output**

- Professional LinkedIn Post
- AI Review Feedback
- Approval Status
- Number of Iterations

---

# Future Improvements

- Multiple writing styles
- Tone selection
- Post length options
- LinkedIn carousel generation
- AI image generation
- Export to PDF
- Direct LinkedIn publishing
- Post history

---

# Technologies Used

- LangGraph
- LangChain
- Mistral AI
- Groq
- Tavily Search
- Streamlit

---

# Author

**Your Name**

Built with ❤️ using LangGraph and Generative AI.