# ==========================================
# main.py
# ==========================================

import os
from typing import TypedDict

from dotenv import load_dotenv
from groq import Groq

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

from langgraph.graph import StateGraph, END

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found")

client = Groq(api_key=api_key)

# ==========================================
# STATE
# ==========================================
class AgentState(TypedDict):
    context: str
    optimist: str
    skeptic: str
    final: str

# ==========================================
# OPTIMIST AGENT
# ==========================================
def optimist_node(state: AgentState):

    context = state.get("context", "")

    prompt = f"""
You are an optimistic financial analyst.

ONLY use the given context.

Your tasks:
1. Identify strengths
2. Identify growth opportunities
3. Mention positive signals

Context:
{context}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return {
        "optimist": response.choices[0].message.content
    }

# ==========================================
# SKEPTIC AGENT
# ==========================================
def skeptic_node(state: AgentState):

    context = state.get("context", "")

    prompt = f"""
You are a skeptical financial analyst.

ONLY use the given context.

Your tasks:
1. Identify risks
2. Identify weaknesses
3. Mention negative indicators
4. Mention concerns

Context:
{context}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return {
        "skeptic": response.choices[0].message.content
    }

# ==========================================
# JUDGE AGENT
# ==========================================
def judge_node(state: AgentState):

    optimist = state.get("optimist", "")
    skeptic = state.get("skeptic", "")

    prompt = f"""
You are a senior financial analyst.

Below are two analyses.

OPTIMIST VIEW:
{optimist}

SKEPTIC VIEW:
{skeptic}

Generate:
1. Balanced summary
2. Financial health score (0-10)
3. Opportunities
4. Risks
5. Final conclusion
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return {
        "final": response.choices[0].message.content
    }

# ==========================================
# BUILD GRAPH
# ==========================================
graph = StateGraph(AgentState)

graph.add_node("optimist", optimist_node)
graph.add_node("skeptic", skeptic_node)
graph.add_node("judge", judge_node)

graph.set_entry_point("optimist")

graph.add_edge("optimist", "skeptic")
graph.add_edge("skeptic", "judge")
graph.add_edge("judge", END)

app_graph = graph.compile()

# ==========================================
# MAIN PIPELINE
# ==========================================
def run_pipeline(file_path: str):

    # -----------------------------
    # LOAD PDF
    # -----------------------------
    loader = PyPDFLoader(file_path)

    documents = loader.load()

    # -----------------------------
    # CHUNKING
    # -----------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    # -----------------------------
    # PREPARE TEXT
    # -----------------------------
    texts = [doc.page_content for doc in chunks]

    # -----------------------------
    # EMBEDDINGS
    # -----------------------------
    embeddings = FakeEmbeddings(size=384)

    # -----------------------------
    # VECTOR DATABASE
    # -----------------------------
    vector_db = FAISS.from_texts(
        texts=texts,
        embedding=embeddings
    )

    # -----------------------------
    # QUERY
    # -----------------------------
    query = """
    business model,
    revenue,
    risks,
    growth,
    opportunities,
    financial performance
    """

    results = vector_db.similarity_search(query, k=6)

    # -----------------------------
    # BUILD CONTEXT
    # -----------------------------
    context = "\n\n".join(
        [
            f"[Chunk {i+1}]\n{r.page_content}"
            for i, r in enumerate(results)
        ]
    )

    # prevent token overflow
    context = context[:6000]

    # -----------------------------
    # RUN GRAPH
    # -----------------------------
    result = app_graph.invoke({
        "context": context
    })

    return result["final"]

# ==========================================
# LOCAL TESTING
# ==========================================
if __name__ == "__main__":

    os.makedirs("data", exist_ok=True)

    file_name = input(
        "Enter PDF file name (inside data folder): "
    )

    output = run_pipeline(f"data/{file_name}")

    print("\n" + "=" * 60)
    print("📊 FINANCIAL ANALYSIS")
    print("=" * 60 + "\n")

    print(output)