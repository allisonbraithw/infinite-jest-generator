import pickle
import os

from dependency_factory import dependency_factory as df
from enum import Enum
from typing import List

import PyPDF2 as pdf
from sentence_transformers import SentenceTransformer


class ChunkType(Enum):
    PAGE = "Page"
    CHUNK = "Chunk"


schema = {
    "classes": [
        {
            "class": "Page",
            "vectorizer": "none",
        },
        {
            "class": "Chunk",
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


def load_or_generate_embeddings(
    infiniteJestChunks: list, book_name: str = "infinite-jest", chunk_type: ChunkType = ChunkType.CHUNK, root_dir: str = "../../data/"
):
    print(f"Checking for {chunk_type.value} embeddings")
    # todo(arb) this currently does not work, using default embeddings for now
    embeddings_file_name = f"{root_dir}{book_name}-{chunk_type.value}-embeddings.txt"

    if os.path.isfile(embeddings_file_name):
        with open(embeddings_file_name, "rb") as ije:
            embeddings = pickle.load(ije)
    else:
        print(" Embeddings not found, generating now")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(infiniteJestChunks)
        with open(embeddings_file_name, "wb") as ije:
            pickle.dump(embeddings, ije)
    return embeddings
