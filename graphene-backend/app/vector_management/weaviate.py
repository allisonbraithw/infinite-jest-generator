from dependency_factory import dependency_factory as df
from enum import Enum
from typing import List


class ChunkType(Enum):
    PAGE = "Page"
    CHUNK = "Chunk"


schema = {
    "classes": [
        {
            "class": "Page",
            "vectorizer": "text2vec-huggingface",
            "moduleConfig": {
                "text2vec-huggingface": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2"},
            }
        },
        {
            "class": "Chunk",
            "vectorizer": "text2vec-huggingface",
            "moduleConfig": {
                "text2vec-huggingface": {
                    "model": "sentence-transformers/all-MiniLM-L6-v2"},
            }
        }
    ]
}


def initialize_schema():
    if df.weaviate_client.schema.get() is None:
        df.weaviate_client.schema.create(schema)


def configure_batches(data: List, type: ChunkType, purge: bool = True):
    if purge:
        df.weaviate_client.schema.delete_all()
        initialize_schema()
    df.weaviate_client.batch.configure(batch_size=100)
    with df.weaviate_client.batch as batch:
        for i, d in enumerate(data):
            properties = {
                "index": i,
                "text": d,
            }
            batch.add_data_object(
                data_object=properties,
                class_name=type.value
            )
