import sys, os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from pathlib import Path
import streamlit as st
from apps.rag_pipeline import rag_pipeline
from apps.core.config import UPLOAD_DIR

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="AskMyDoc",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Serif+Display&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background: #f6f5f1 !important;
    color: #1a1918 !important;
}

.stApp { min-height: 100vh; overflow-x: hidden; }

.block-container {
    padding: 0 0 60px !important;
    max-width: 680px !important;
}

/* hide "200MB per file • PDF, TXT, MD" text */
[data-testid="stFileUploader"] > div > small {
    display: none !important;
}

/* fallback in case Streamlit changes structure */
[data-testid="stFileUploader"] small {
    display: none !important;
}

#MainMenu, footer, header, .stDeployButton,
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
label { display: none !important; }
.stSpinner { display: none !important; }

/* ── NAV ── */
.amd-nav {
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    background: #fff;
    border-bottom: 1px solid #e8e6e0;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    margin-bottom: 0;
}

.amd-nav-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #1a1918;
    letter-spacing: -0.02em;
}

.amd-nav-logo span { color: #1a6ef5; }

.amd-nav-tag {
    font-size: 11px;
    color: #9b9790;
    background: #f0ede8;
    border-radius: 100px;
    padding: 3px 11px;
    letter-spacing: 0.03em;
    font-weight: 400;
}

/* ── HERO ── */
.amd-hero {
    text-align: center;
    padding: 48px 24px 32px;
}

.amd-hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.5rem;
    color: #1a1918;
    letter-spacing: -0.03em;
    line-height: 1.15;
}

.amd-hero-title span { color: #1a6ef5; }

.amd-hero-sub {
    margin-top: 10px;
    font-size: 14px;
    color: #7a7672;
    font-weight: 300;
    line-height: 1.6;
}

/* ── DIVIDER ── */
.amd-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e0ddd8, transparent);
    margin: 4px 0 24px;
}

/* ── STEP LABEL ── */
.amd-step {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}

.amd-step-num {
    width: 24px; height: 24px;
    border-radius: 50%;
    background: #eef2ff;
    border: 1.5px solid #c7d7fa;
    color: #1a6ef5;
    font-size: 10px;
    font-weight: 600;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-variant-numeric: tabular-nums;
}

.amd-step-label {
    font-size: 11px;
    font-weight: 500;
    color: #9b9790;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── UPLOAD ZONE ── */
[data-testid="stFileUploader"] { background: transparent !important; }

[data-testid="stFileUploaderDropzone"] {
    background: #fff !important;
    border: 1.5px dashed #d8d5ce !important;
    border-radius: 12px !important;
    padding: 20px 16px 14px !important;
    transition: all 0.2s !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #1a6ef5 !important;
    box-shadow: 0 0 0 3px rgba(26,110,245,0.08) !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #9b9790 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    background: transparent !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: #f0ede8 !important;
    border: 1px solid #d8d5ce !important;
    border-radius: 6px !important;
    padding: 4px 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    position: relative;

    color: transparent !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    display: none !important;
}



[data-testid="stFileUploaderDropzone"] button::after {
    content: "Upload";
    font-size: 12px;
    color: #3d3c3a;
}

[data-testid="stFileUploaderDropzone"] > small,
[data-testid="stFileUploader"] > small { display: none !important; }

[data-testid="stFileUploaderDropzone"]::after {
    content: "PDF · TXT · MD — 50MB max";
    display: block;
    color: #c0bbb4;
    font-size: 11px;
    text-align: center;
    font-weight: 300;
    margin-top: 6px;
    letter-spacing: 0.02em;
}

/* ── TEXTAREA ── */
.stTextArea > div { background: transparent !important; }

.stTextArea textarea {
    background: #fff !important;
    border: 1.5px solid #d8d5ce !important;
    border-radius: 12px !important;
    color: #1a1918 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 14px 16px !important;
    transition: all 0.2s !important;
    caret-color: #1a6ef5;
    resize: none !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

.stTextArea textarea:focus {
    border-color: #1a6ef5 !important;
    box-shadow: 0 0 0 3px rgba(26,110,245,0.1) !important;
    outline: none !important;
}

.stTextArea textarea::placeholder { color: #c0bbb4 !important; }

/* ── BUTTON ── */
.stButton {
    display: flex !important;
    justify-content: flex-start !important;
    margin-top: 12px !important;
}

.stButton > button {
    background: #1a6ef5 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 100px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 0 22px !important;
    height: 38px !important;
    width: auto !important;
    min-width: unset !important;
    max-width: fit-content !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(26,110,245,0.25) !important;
    white-space: nowrap !important;
}

.stButton > button:hover {
    background: #155de0 !important;
    box-shadow: 0 4px 14px rgba(26,110,245,0.35) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ── ALERTS ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    margin-top: 10px !important;
}

/* ── LOADER ── */
.amd-loader-overlay {
    position: fixed; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: rgba(246,245,241,0.82);
    backdrop-filter: blur(8px);
    z-index: 9999; gap: 18px;
    animation: fadeIn 0.2s ease;
}

.amd-loader-text {
    font-size: 13px; color: #7a7672;
    font-family: 'DM Sans', sans-serif;
    font-weight: 300; letter-spacing: 0.02em;
}

.dots { display: flex; gap: 7px; align-items: center; }

.dots span {
    width: 9px; height: 9px;
    border-radius: 50%;
    animation: dotBounce 1.4s ease-in-out infinite;
}

.dots span:nth-child(1) { background: #1a6ef5; animation-delay: 0s; }
.dots span:nth-child(2) { background: #ea4335; animation-delay: 0.18s; }
.dots span:nth-child(3) { background: #fbbc04; animation-delay: 0.36s; }
.dots span:nth-child(4) { background: #34a853; animation-delay: 0.54s; }

/* ── ANSWER CARD ── */
.answer-card {
    background: #fff;
    border: 1px solid #e0ddd8;
    border-top: 3px solid #1a6ef5;
    border-radius: 12px;
    padding: 18px 20px;
    margin-top: 4px;
    font-size: 14px;
    line-height: 1.75;
    color: #2d2c2a;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    animation: slideUp 0.35s cubic-bezier(0.4, 0, 0.2, 1) both;
}

.answer-top {
    display: flex; align-items: center; gap: 8px; margin-bottom: 12px;
}

.answer-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #1a6ef5;
    box-shadow: 0 0 0 3px rgba(26,110,245,0.12);
    flex-shrink: 0;
}

.answer-lbl {
    font-size: 11px; font-weight: 600; color: #1a6ef5;
    text-transform: uppercase; letter-spacing: 0.08em;
}

.answer-model {
    margin-left: auto; font-size: 11px; color: #c0bbb4;
    font-weight: 300;
}

.answer-sep {
    height: 1px; background: #f0ede8;
    border: none; margin: 0 0 14px;
}

/* ── ANIMATIONS ── */
@keyframes dotBounce {
    0%,60%,100% { transform: translateY(0); opacity: 0.3; }
    30% { transform: translateY(-8px); opacity: 1; }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; } to { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="amd-nav">
    <div class="amd-nav-logo">AskMy<span>Doc</span></div>
    <div class="amd-nav-tag">RAG · Gemini 2.5 Flash</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="amd-hero">
    <div class="amd-hero-title">Ask anything about<br><span>your documents.</span></div>
    <div class="amd-hero-sub">Upload a file, ingest it into a vector store,<br>and get AI-powered answers grounded in your content.</div>
</div>
<div class="amd-divider"></div>
""", unsafe_allow_html=True)


loader_slot = st.empty()

# ── STEP 1: UPLOAD ────────────────────────────────────────────────────────────
st.markdown("""
<div class="amd-step">
    <div class="amd-step-num">1</div>
    <div class="amd-step-label">Upload &amp; Ingest Document</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "file", type=["pdf", "txt", "md"],
    label_visibility="collapsed",
)

ingest_msg = st.empty()

if uploaded_file:
    if uploaded_file.size > 50 * 1024 * 1024:
        ingest_msg.error("File exceeds 50MB limit.")
        st.stop()

    dest_path = UPLOAD_DIR / uploaded_file.name
    dest_path.write_bytes(uploaded_file.read())
    ingest_msg.success(f"**{uploaded_file.name}** uploaded successfully.")

    if st.button("Ingest Document"):
        loader_slot.markdown("""
        <div class="amd-loader-overlay">
            <div class="dots"><span></span><span></span><span></span><span></span></div>
            <div class="amd-loader-text">Chunking and embedding document...</div>
        </div>
        """, unsafe_allow_html=True)
        try:
            rag_pipeline.ingest_file(dest_path)
            loader_slot.empty()
            ingest_msg.success(f"**{uploaded_file.name}** ingested. Ready to answer questions.")
        except Exception as e:
            loader_slot.empty()
            ingest_msg.error(f"Ingestion failed: {e}")

# ── DIVIDER ──────────────────────────────────────────────────────────────────
st.markdown('<div class="amd-divider" style="margin-top:24px"></div>', unsafe_allow_html=True)

# ── STEP 2: QUESTION ─────────────────────────────────────────────────────────
st.markdown("""
<div class="amd-step">
    <div class="amd-step-num">2</div>
    <div class="amd-step-label">Ask a Question</div>
</div>
""", unsafe_allow_html=True)

query = st.text_area(
    "q",
    placeholder="What is the main topic of this document?",
    height=96,
    label_visibility="collapsed",
)

answer_slot = st.empty()

if st.button("Get Answer"):
    if not query.strip():
        answer_slot.warning("Please enter a question first.")
    else:
        loader_slot.markdown("""
        <div class="amd-loader-overlay">
            <div class="dots"><span></span><span></span><span></span><span></span></div>
            <div class="amd-loader-text">Retrieving context and generating answer...</div>
        </div>
        """, unsafe_allow_html=True)
        try:
            answer = rag_pipeline.ask(query.strip())
            loader_slot.empty()
            answer_slot.markdown(f"""
            <div class="answer-card">
                <div class="answer-top">
                    <div class="answer-dot"></div>
                    <div class="answer-lbl">Answer</div>
                    <div class="answer-model">gemini-2.5-flash</div>
                </div>
                <hr class="answer-sep">
                {answer}
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            loader_slot.empty()
            answer_slot.error(f"Query failed: {e}")
