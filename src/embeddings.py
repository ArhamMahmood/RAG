import ollama


MODEL = "all-minilm:latest"


def create_embedding(text):
    response = ollama.embed(
        model=MODEL,
        input=text
    )

    return response["embeddings"][0]


if __name__ == "__main__":

    text = "What is machine learning?"

    embedding = create_embedding(text)

    print("Embedding dimensions:", len(embedding))
    print("First 10 values:", embedding[:10])