import os
from typing import List, Tuple
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# Constants
CHROMA_DIR = "vectorstore"

def get_vectorstore(role: str):
    """
    Load or create vectorstore for a given role (finance, marketing, etc.)
    """
    persist_dir = f"{CHROMA_DIR}/{role}"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(persist_dir):
        return Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        return ingest_docs(role, persist_dir, embeddings)

def ingest_docs(role: str, persist_dir: str, embeddings):
    """
    Loads docs from `resources/data/<role>`, splits, embeds and stores them
    """
    load_dotenv()
    source_dir = f"resources/data/{role}"

    loader = DirectoryLoader(source_dir, glob="**/*.md", show_progress=True, use_multithreading=True)
    documents = loader.load()

    # 3. Inject source metadata (sometimes missing by default)
    print(f"[INFO] Loaded {len(documents)} documents for role: {role}")
    for doc in documents:
        print(f"[DOC] {doc.metadata.get('source')}: {doc.page_content[:80]}...")
        doc.metadata["source"] = os.path.basename(doc.metadata.get("source", "unknown"))

    # 4. Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    print(f"[INFO] Split into {len(docs)} chunks")


    # 5. Embed and save to Chroma
    vectordb = Chroma.from_documents(
        docs,
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        persist_directory=persist_dir,
    )
    vectordb.persist()
    return vectordb

def get_context_from_query(vectordb, query: str) -> Tuple[str, List[str]]:
    """
    Queries the vectordb and returns matched context chunks + their sources
    """
    results = vectordb.similarity_search_with_score(query, k=3)
    print(f"[QUERY] {query}")
    print(f"[RESULTS] {len(results)} hits")
    for doc, score in results:
        print(f"[MATCH] {score:.4f} | {doc.metadata.get('source')} | {doc.page_content[:100]}")
    chunks = [doc.page_content for doc, score in results]
    sources = [doc.metadata.get('source', 'unknown') for doc, score in results]
    print(f"[DEBUG] Source: {sources}")
    return "\n\n".join(chunks), sources




























# import os
# from typing import List, Tuple
# from langchain.document_loaders import DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain.vectorstores import Chroma


# # Constants
# CHROMA_DIR = "vectorstore"

# def get_vectorstore(role: str):
#     """
#     Load or create vectorstore for a given role (finance, marketing, etc.)
#     """
#     persist_dir = f"{CHROMA_DIR}/{role}"
#     if os.path.exists(persist_dir):
#         return Chroma(persist_directory=persist_dir, embedding_function=OpenAIEmbeddings())
#     else:
#         return ingest_docs(role, persist_dir)

# def ingest_docs(role: str, persist_dir: str):
#     """
#     Loads docs from `resources/data/<role>`, splits, embeds and stores them
#     """
#     from dotenv import load_dotenv
#     import os

#     load_dotenv()
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")

#     source_dir = f"resources/data/{role}"
#     loader = DirectoryLoader(source_dir, glob="**/*.md")
#     documents = loader.load()

#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     docs = splitter.split_documents(documents)

#     vectordb = Chroma.from_documents(
#         docs, 
#         embedding=OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")), 
#         persist_directory=persist_dir
#     )
#     vectordb.persist()
#     return vectordb

# def get_context_from_query(vectordb, query: str) -> Tuple[str, List[str]]:
#     """
#     Queries the vectordb and returns matched context chunks + their sources
#     """
#     results = vectordb.similarity_search_with_score(query, k=3)
#     chunks = [doc.page_content for doc, score in results]
#     sources = [doc.metadata.get('source', 'unknown') for doc, score in results]
#     return "\n\n".join(chunks), sources
