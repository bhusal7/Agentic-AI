# 🤖 Agentic-AI

> A collection of **Agentic AI**, **LangGraph**, **LangChain**, & **Retrieval-Augmented Generation (RAG)** projects built while learning modern AI engineering workflows.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge\&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20AI-orange?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Retrieval%20Augmented-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-black?style=for-the-badge)

---

# 📖 About

This repository contains multiple **Agentic AI** projects demonstrating different workflow patterns using **LangGraph**, **LangChain**, & **Large Language Models (LLMs)**.

The goal of this repository is to understand how autonomous AI systems reason, make decisions, use tools, retrieve knowledge, collaborate with humans, and execute complex workflows.

Projects range from simple sequential pipelines to advanced Retrieval-Augmented Generation (RAG) applications.

---

# 🚀 Technologies Used

* Python
* LangGraph
* LangChain
* Generative AI
* Agentic AI
* Retrieval-Augmented Generation (RAG)
* Vector Embeddings
* PDF Document Processing
* State Management
* Human-in-the-Loop (HITL)
* Tool Calling
* LLM Workflows

---

# 📂 Repository Structure

```
Agentic-AI/
│
├── Projects/
│
├── sequential_base.py
│      Sequential Workflow
│
├── parallel_reducers.py
│      Parallel Execution + Reducers
│
├── conditional_RAG.py
│      College RAG Assistant
│
├── humanintheloop.py
│      Human-in-the-Loop LinkedIn Writer
│
├── iterative_tools.py
│      Iterative Tool Calling Agent
│
├── states.py
│      Shared State Definitions
│
├── academics_handbook.pdf
│
├── fee_structure.pdf
│
├── requirements.txt
│
└── README.md
```

---

# 📚 Projects

## 1️⃣ Sequential Workflow

**File**

```
sequential_base.py
```

### Concepts

* Sequential execution
* State passing
* LangGraph basics
* Pipeline execution

### Workflow

```
Start
   │
   ▼
Node 1
   │
   ▼
Node 2
   │
   ▼
Node 3
   │
   ▼
 End
```

---

## 2️⃣ Parallel Workflow with Reducers

**File**

```
parallel_reducers.py
```

### Concepts

* Parallel nodes
* Concurrent execution
* Reducers
* State merging

### Workflow

```
             Start
               │
        ┌──────┴──────┐
        ▼             ▼
     Node A        Node B
        │             │
        └──────┬──────┘
               ▼
           Reducer
               │
               ▼
              End
```

---

## 3️⃣ Conditional RAG Assistant

**File**

```
conditional_RAG.py
```

### Features

* PDF Question Answering
* Vector Search
* Retrieval-Augmented Generation (RAG)
* Conditional Routing
* Context-based responses

### Documents Used

* academics_handbook.pdf
* fee_structure.pdf

### Pipeline

```
User Question
      │
      ▼
Retrieve Documents
      │
      ▼
Relevant Chunks
      │
      ▼
LLM
      │
      ▼
Answer
```

---

## 4️⃣ Human-in-the-Loop (HITL)

**File**

```
humanintheloop.py
```

### Features

* AI-generated LinkedIn posts
* Human approval
* Feedback loop
* Revision workflow

### Workflow

```
Generate Draft
      │
      ▼
Human Review
      │
 ┌────┴─────┐
 │          │
Approve   Reject
 │          │
 ▼          ▼
Publish   Improve
```

---

## 5️⃣ Iterative Tool Calling Agent

**File**

```
iterative_tools.py
```

### Features

* Tool calling
* Multiple reasoning steps
* Iterative execution
* Agent loop
* Autonomous decision making

### Workflow

```
Question
    │
    ▼
Reason
    │
    ▼
Use Tool
    │
    ▼
Observe
    │
    ▼
Need Another Tool?
    │
 ┌──┴───┐
 │ Yes  │
 ▼      │
Reason  │
 │      │
 └──────┘
    │
    ▼
Final Answer
```

---

# 🧠 LangGraph Concepts Covered

* StateGraph
* Nodes
* Edges
* START
* END
* Conditional Edges
* Reducers
* Parallel Execution
* Sequential Execution
* Human-in-the-Loop
* Tool Calling
* State Management
* Routing
* Multi-Step Reasoning

---

# 📄 RAG Concepts Covered

* PDF Loading
* Document Chunking
* Embeddings
* Vector Search
* Retrieval
* Prompt Engineering
* Context Injection
* LLM Generation

---

# 🎯 Learning Outcomes

This repository demonstrates:

* Building Agentic AI applications
* Designing LangGraph workflows
* Creating Retrieval-Augmented Generation systems
* Human-in-the-Loop architectures
* Tool-based AI agents
* State management
* Parallel execution
* Conditional routing
* Workflow orchestration

---

# 🛠️ Installation

Clone the repository

```bash
git clone https://github.com/bhusal7/Agentic-AI.git
```

Move into the project

```bash
cd Agentic-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run a Project

Sequential Workflow

```bash
python sequential_base.py
```

Parallel Workflow

```bash
python parallel_reducers.py
```

Conditional RAG

```bash
python conditional_RAG.py
```

Human in the Loop

```bash
python humanintheloop.py
```

Iterative Tool Calling

```bash
python iterative_tools.py
```

---

# 📈 Repository Goals

* Learn Agentic AI
* Master LangGraph
* Explore RAG pipelines
* Understand workflow orchestration
* Build production-ready AI systems
* Prepare for advanced multi-agent architectures

---

# 🔮 Future Projects

* Multi-Agent Collaboration
* AI Code Assistant
* GitHub Repository Analyzer
* Autonomous Research Agent
* Customer Support Agent
* Financial AI Assistant
* SQL AI Agent
* Resume Analyzer
* Email Automation Agent
* Deep Research Agent

---

# 🤝 Contributions

Contributions, suggestions, and improvements are welcome.

Feel free to fork this repository and submit a pull request.

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Vashudev Bhusal**

AI Engineer | Data Science | Machine Learning | Deep Learning | Generative AI | Agentic AI

GitHub: https://github.com/bhusal7

---

⭐ If you found this repository helpful, consider giving it a **Star**.
