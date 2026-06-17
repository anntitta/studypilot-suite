import os
import chromadb
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv

load_dotenv()

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
chroma_client = chromadb.PersistentClient(path=DB_DIR)

genai_client = genai.Client()
EMBED_MODEL = "text-embedding-004"

collection = chroma_client.get_or_create_collection(name="study_pilot_materials")

def extract_and_index_pdf(file_path: str, file_id: str):
    """Parses text out of incoming PDFs and builds vector storage coordinates."""
    if not os.path.exists(file_path):
        return False
        
    reader = PdfReader(file_path)
    chunks = []
    
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            paragraphs = text.split("\n\n")
            for sub_idx, para in enumerate(paragraphs):
                clean_para = para.strip()
                if len(clean_para) > 20:
                    chunks.append({
                        "id": f"{file_id}_p{page_idx}_c{sub_idx}",
                        "text": clean_para,
                        "metadata": {"source": file_id, "page": page_idx}
                    })

    if not chunks:
        return False

    documents_text = [c["text"] for c in chunks]
    ids_list = [c["id"] for c in chunks]
    metadatas_list = [c["metadata"] for c in chunks]
    
    response = genai_client.models.embed_content(
        model=EMBED_MODEL,
        contents=documents_text
    )
    
    embeddings = [embedding.values for embedding in response.embeddings]
    
    collection.add(
        embeddings=embeddings,
        documents=documents_text,
        ids=ids_list,
        metadatas=metadatas_list
    )
    return True

def query_academic_knowledge(user_query: str, max_results: int = 3) -> str:
    """Queries ChromaDB vectors using cosine similarity for matching text segments."""
    response = genai_client.models.embed_content(
        model=EMBED_MODEL,
        contents=user_query
    )
    query_vector = response.embeddings[0].values
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=max_results
    )
    
    if results and "documents" in results and results["documents"]:
        return "\n---\n".join(results["documents"][0])
        
    return ""