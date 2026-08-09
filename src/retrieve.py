import chromadb
import ollama


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="documents"
)


def create_embedding(text):

    response = ollama.embed(
        model="all-minilm:latest",
        input=text
    )

    return response["embeddings"][0]


question = "What is machine learning?"

query_embedding = create_embedding(question)


results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)


for i, document in enumerate(results["documents"][0]):

    metadata = results["metadatas"][0][i]

    print("\n====================")
    print("Result:", i + 1)
    print("Source:", metadata["source"])
    print("Page:", metadata["page"])
    print("--------------------")
    print(document) 