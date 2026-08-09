import chromadb
import ollama


LLM_MODEL = "qwen2.5:3b"
EMBEDDING_MODEL = "all-minilm:latest"


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="documents"
)


def create_embedding(text):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]


def retrieve(question, n_results=5):

    embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    documents = results["documents"][0]

    return documents


def generate_answer(question, documents):

    context = "\n\n".join(documents)

    prompt = f"""
The following context is from a resume document.
Answer the question using only the context below.
If the answer is not in the context, respond with "I don't know.".
Do not make up facts.
Keep the answer short and direct.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False,
        options={
            "num_predict": 120,
            "temperature": 0.0
        }
    )

    return response["message"]["content"]


def main():

    question = input("\nAsk a question: ")

    documents = retrieve(question)

    answer = generate_answer(
        question,
        documents
    )

    print("\n====================")
    print("ANSWER")
    print("====================")
    print(answer)


if __name__ == "__main__":
    main()