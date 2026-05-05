**# FinSight: Adversarial Earnings Analysis**

An AI system that reads SEC 10-K reports and produces **evidence-based financial insights** using a **multi-agent debate (Optimist vs Skeptic)** over RAG-retrieved context.


## 🚀 Overview

FinSight ingests annual reports (10-K PDFs), retrieves the most relevant sections, and runs an **agentic debate**:

* 🟢 **Optimist Agent** → strengths & growth
* 🔴 **Skeptic Agent** → risks & weaknesses
* ⚖️ **Judge Agent** → balanced summary + score

Exposed as a **FastAPI service** where users upload a PDF and receive a structured analysis.

---

## 🧠 Key Features

* 📄 **PDF Parsing & Chunking** (LangChain)
* 🔎 **Retrieval-Augmented Generation (RAG)**
* 🗃️ **Vector Store (FAISS)**
* 🤖 **Agentic Debate (LangGraph)**
* ⚖️ **Final Consensus + Financial Score (0–10)**
* 🌐 **FastAPI endpoint with file upload**

---

## 🏗️ Architecture

```
PDF → Chunking → Vector DB (FAISS)
     → Retrieval (Top-K Context)
     → LangGraph Agents:
          Optimist → Skeptic → Judge
     → Final Report
     → FastAPI JSON Response
```

---

## 🛠️ Tech Stack

* **Python**
* **LangChain**
* **LangGraph**
* **FAISS**
* **Groq LLM (LLaMA 3.1)**
* **FastAPI**
* **Uvicorn**

---

## 📂 Project Structure

```
finsight/
│
├── data/                 # Uploaded PDFs
├── main.py               # Core pipeline + agents
├── api.py                # FastAPI server
├── requirements.txt
├── .env                  # API key
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/finsight.git
cd finsight
```

### 2. Create virtual environment

```bash
python -m venv finsight_env
finsight_env\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
python -m uvicorn api:app --reload
```

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 How to Use

1. Open `/docs`
2. Select **POST /analyze**
3. Click **Try it out**
4. Upload a 10-K PDF
5. Click **Execute**

---

## 📊 Sample Output

```json
{
  "status": "success",
  "file": "nvidia.pdf",
  "analysis": "Balanced Summary: NVIDIA shows strong growth in AI and data centers... Score: 8/10"
}
```

---

## ⚠️ Challenges Solved

### 1. Context Window Overflow

* Limited context using top-K retrieval
* Truncated input to fit LLM constraints

### 2. Hallucination Reduction

* Forced agents to use **retrieved context only**
* No external assumptions allowed

### 3. Agentic Reasoning

* Implemented structured debate using **LangGraph**
* Combined perspectives into a final decision

---

## 🔮 Future Improvements

* 📊 Multi-company comparison (NVIDIA vs Tesla)
* 🧠 Better embeddings (SentenceTransformers)
* 💻 Frontend dashboard (React)
* ☁️ Cloud deployment (Render/AWS)

---

