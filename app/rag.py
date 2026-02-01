from app.chunking import chunk_text
from app.embeddings import embed_texts
from app.vector_store import VectorStore
from app.llm import ask_llm
from app.evaluation import evaluate_answer


def answer_question(document, question, cache_path):
    chunks = chunk_text(document)

    store = VectorStore(
        dimension=384,
        cache_path=cache_path
    )

    if not store.loaded_from_cache:
        chunk_embeddings = embed_texts(chunks)
        store.add(chunk_embeddings, chunks)

    query_embedding = embed_texts([question])
    context_chunks = store.search(query_embedding, k=4)

    context = "\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant.
Use the context below to answer the question.
You may rephrase or summarize information from the context.
If the context does not contain enough information, say "I don't know".

Context:
{context}

Question:
{question}
"""

    answer = ask_llm(prompt)

    evaluation = evaluate_answer(question, context, answer)

    return answer, context, evaluation
