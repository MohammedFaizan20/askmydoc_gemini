from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from apps.core.config import EMBEDDING_MODEL, LLM_MODEL, GOOGLE_API_KEY
from apps.core.utils import extract_text


class RAGPipeline:
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise RuntimeError("Missing GOOGLE_API_KEY in .env")

        # Embeddings still run locally via sentence-transformers
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectorstore = None

        # Gemini replaces Mistral
        self.llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3,
            max_output_tokens=512,
        )

        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an AI assistant that answers strictly based on the provided document context.
If the answer is not present in the document, respond with:
'The information is not available in the document.'
Provide concise and factual responses.

Context:
{context}

Question: {question}
Answer:"""
        )

    def ingest_file(self, file_path: Path):
        text = extract_text(file_path)
        if not text:
            raise ValueError("The document is empty or unreadable.")

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = splitter.split_text(text)

        self.vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            metadatas=[{"source": file_path.name}] * len(chunks),
        )

    def ask(self, query: str) -> str:
        if not self.vectorstore:
            return "Please ingest a document first."

        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            chain_type="stuff",
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template},
        )

        result = qa_chain.invoke({"query": query})
        return result.get("result", "No answer found.")


rag_pipeline = RAGPipeline()