from app.utils.embedding import get_vectorstore, get_context_from_query
import os
from dotenv import load_dotenv



load_dotenv()

def build_prompt(context: str, query: str) -> str:
    return f"""
You are a helpful assistant for FinNova's internal team. You have access to internal marketing documents.

Use the following context to answer the user's question truthfully and concisely. If the context does not contain the answer, respond with "I'm not sure based on the current data."

Context:
{context}

User Question: "{query}"

Answer:
"""


from transformers import pipeline

# One-time load
rag_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",  # or "flan-t5-large"
    max_length=512
)

def query_rag(query: str, role: str):
    vectorstore = get_vectorstore(role)
    context, sources = get_context_from_query(vectorstore, query)
    prompt = build_prompt(context, query)

    response = rag_pipeline(prompt)[0]["generated_text"]
    return response, sources


# def query_rag(query: str, role: str):
#     # Load vectorstore for this role
#     vectorstore = get_vectorstore(role)

#     # Search for relevant chunks
#     context, sources = get_context_from_query(vectorstore, query)

#     # Build prompt
#     prompt = build_prompt(context, query)

#     # Hugging Face model config
#     llm = HuggingFaceHub(
#     repo_id="tiiuae/falcon-7b-instruct",
#     model_kwargs={"temperature": 0.5, "max_new_tokens": 512},
#     huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
#     )


#     # Get answer from LLM
#     answer = llm(prompt)
#     return answer, sources
