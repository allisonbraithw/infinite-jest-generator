from typing import List
from vector_management.text_processing import load_or_generate_embeddings, ChunkType
from dependency_factory import dependency_factory as df


schema = {
    "classes": [
        {
            "class": "Page",
            "vectorizer": "none",
        },
        {
            "class": "Chunk10",
            "vectorizer": "none",
        },
        {
            "class": "Chunk20",
            "vectorizer": "none",
        }
    ]
}


def initialize_schema():
    if df.weaviate_client.schema.get() is None:
        df.weaviate_client.schema.create(schema)


def configure_batches(data: List, chunk_type: ChunkType, purge: bool = True, root_dir: str = "../../data/"):
    if purge:
        df.weaviate_client.schema.delete_all()
        initialize_schema()
    embeddings = load_or_generate_embeddings(
        data, chunk_type=chunk_type, root_dir=root_dir)

    df.weaviate_client.batch.configure(batch_size=100)
    with df.weaviate_client.batch as batch:
        for i, d in enumerate(data):
            properties = {
                "index": i,
                "text": d,
            }
            batch.add_data_object(
                data_object=properties,
                class_name=chunk_type.value,
                vector=embeddings[i].tolist()
            )
