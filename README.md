# AskMyDocs - PDF Summarization and Question Answering

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51-red?style=flat-square&logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.1.16-green?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange?style=flat-square&logo=google)
![FAISS](https://img.shields.io/badge/VectorStore-FAISS-purple?style=flat-square)

**A RAG-powered document intelligence system that extracts, embeds, and answers questions about your files using Gemini 2.5 Flash.**

[Live Demo](https://huggingface.co/spaces/faizan20/askmydoc_gemini) 

</div>

---

## Overview

AskMyDocs is a Retrieval-Augmented Generation (RAG) pipeline that lets you upload any PDF, TXT, or Markdown file and ask natural language questions about it. The system extracts text, splits it into chunks, generates vector embeddings, stores them in a FAISS index, and uses Gemini 2.5 Flash to generate grounded, context-aware answers.

---

## Demo

**Query:** What methodology was used in the study?

**Answer:**
> The study used case studies combined with experimental evaluations across three enterprise environments, measuring productivity improvements before and after AI-driven automation was introduced.

---

## Features

- Upload PDF, TXT, or Markdown files up to 50MB
- Full text extraction from PDFs using PyPDF
- Recursive text chunking with configurable size and overlap
- Local embedding generation using `sentence-transformers/all-MiniLM-L6-v2` - no external API needed for embeddings
- FAISS vector store for fast similarity search
- Context-aware question answering using Gemini 2.5 Flash
- Document summarization via natural language queries
- Clean Google-style UI built with Streamlit

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Gemini 2.5 Flash (Google AI Studio) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (local) |
| Vector store | FAISS |
| RAG framework | LangChain |
| Text extraction | PyPDF |
| Text splitting | `RecursiveCharacterTextSplitter` |

---

## Project Structure

```
askmydoc_gemini/
├── apps/
│   ├── app.py                # Streamlit UI
│   ├── rag_pipeline.py       # Core RAG pipeline
│   └── core/
│       ├── config.py         # Environment config and paths
│       └── utils.py          # Text extraction utilities
├── .streamlit/
│   └── config.toml           # Streamlit server config (upload size limit)
├── data/
│   └── uploads/              # Uploaded files (auto-created)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Architecture

```
User uploads file (PDF / TXT / MD)
        |
        v
Text Extraction (utils.py)
  pypdf for PDFs, UTF-8 read for TXT/MD
  Clean and normalize text
        |
        v
Text Splitting (rag_pipeline.py)
  RecursiveCharacterTextSplitter
  chunk_size=800, chunk_overlap=150
        |
        v
Embedding Generation
  HuggingFaceEmbeddings
  model: all-MiniLM-L6-v2 (runs locally)
  output: 384-dimensional vectors
        |
        v
Vector Store
  FAISS IndexFlatL2
  Stores chunk vectors in memory
        |
        v
User asks a question
        |
        v
Retrieval
  FAISS similarity search
  Top 4 most relevant chunks returned
        |
        v
LLM Generation (Gemini 2.5 Flash)
  Retrieved chunks injected as context
  Custom strict prompt - answers only from document
        |
        v
Grounded Answer returned to UI
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/app/apikey) API key (free)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/MohammedFaizan20/askmydoc_gemini.git
cd askmydoc_gemini
```

**2. Create and activate a virtual environment**

```bash
# Windows
py -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

```bash
cp .env.example .env
```

Open `.env` and add your key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey).

### Running the App

```bash
python -m streamlit run apps/app.py
```

The app opens at `http://localhost:8501`.

---

## How to Use

**Step 1 - Upload your document**

Click the upload zone and select a PDF, TXT, or MD file (max 50MB).

**Step 2 - Ingest the document**

Click **Ingest Document**. The system will extract text, split it into chunks, generate embeddings and load them into the FAISS vector store.

**Step 3 - Ask questions**

Type any question about the document and click **Get Answer**. The system retrieves the most relevant chunks and passes them to Gemini 2.5 Flash to generate a grounded answer.

**Example queries:**
- `Summarize this document`
- `What is the main argument?`
- `What methodology was used?`
- `What were the key findings?`

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `python-dotenv` | Load environment variables |
| `langchain` | RAG chain orchestration |
| `langchain-core` | LangChain base abstractions |
| `langchain-community` | FAISS and HuggingFace integrations |
| `langchain-text-splitters` | Recursive text chunking |
| `langchain-google-genai` | Gemini LLM integration |
| `faiss-cpu` | Vector similarity search |
| `sentence-transformers` | Local embedding model |
| `pypdf` | PDF text extraction |

---

## Design Decisions

### Local embeddings over API embeddings

`sentence-transformers/all-MiniLM-L6-v2` runs entirely on CPU with no external API call. This eliminates a second API dependency, keeps embedding fast and free, and demonstrates that embeddings and LLMs do not need to come from the same provider. The model produces 384-dimensional vectors - intentionally compact compared to full-size models like `all-mpnet-base-v2` which produce 768 dimensions with marginally better accuracy but double the memory and compute cost. At 384 dimensions the model strikes the best balance of semantic quality and speed for a local CPU-only RAG pipeline, making it the standard choice across the LangChain and Hugging Face ecosystems for this use case.

### FAISS IndexFlatL2 - exact search

FAISS uses a **Flat L2 index** (`IndexFlatL2`) by default via LangChain - it performs exact nearest-neighbour search using Euclidean distance across all stored vectors. For a single-document session with hundreds of chunks this is optimal: no approximation error, no index training required, and negligible latency at this scale. A production system with millions of chunks would switch to `IndexIVFFlat` or `IndexHNSW` for approximate search with better throughput.

### RecursiveCharacterTextSplitter configuration

`chunk_size=800` with `chunk_overlap=150` was chosen to balance two competing needs: chunks small enough for precise retrieval (large chunks dilute relevance scores) and large enough to preserve sentence-level context (tiny chunks lose meaning). The 150-character overlap prevents answers from being split across chunk boundaries. At `k=4` chunks of 800 characters each, the total context passed to Gemini stays well under 4000 tokens - comfortably within the 1M token context window of Gemini 2.5 Flash, leaving ample room for the prompt template and generated answer.

### Strict grounding prompt

The LLM prompt explicitly instructs the model to answer only from the provided document context and to respond with "The information is not available in the document" if the answer cannot be found. Temperature is set to 0.3. This prevents hallucination and ensures answers are traceable to the source document.

### RetrievalQA with `stuff` chain type

The `stuff` chain concatenates all retrieved chunks into a single prompt. This works well for `k=4` chunks at 800 characters each - total context stays well within Gemini's token limit. For very large documents where context would overflow, a `map_reduce` or `refine` chain type would be more appropriate.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | Yes | Google AI Studio API key for Gemini |
| `EMBEDDING_MODEL` | No | Override embedding model (default: `sentence-transformers/all-MiniLM-L6-v2`) |
| `LLM_MODEL` | No | Override LLM model (default: `gemini-2.5-flash`) |

---
