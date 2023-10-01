import chromadb


def initialize_vector_db(chunks: list):
    id_list = [str(item) for item in range(0, len(chunks))]
    # todo(arb): this step takes a while, should just store it somewhere
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="infinite_jest")
    collection.add(
        documents=chunks,
        ids=id_list,
    )

    return chroma_client, collection


def initialize_collection(client, chunks: list, embeddings: list = None):
    id_list = [str(item) for item in range(0, len(chunks))]
    # todo(arb): this step takes a while, should just store it somewhere
    collection = client.create_collection(name="infinite_jest")
    collection.add(
        documents=chunks,
        ids=id_list,
    )

    return collection
