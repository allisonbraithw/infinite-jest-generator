import logging
import json

from typing import List as list
from graphene import Field, ObjectType, String, List
from graphene_federation import build_schema
from robot.character_query import get_character_description_summary, generate_stability_image
from robot.text_processing import limit_docs_by_tokens
from image_gen.generate_image import generate_image
from inference.character_query import get_character_description_summary
from vector_management.text_processing import limit_docs_by_tokens
from vector_management.weaviate import ChunkType
from dependency_factory import dependency_factory as df


class Character(ObjectType):
    fullName = String(required=True)
    alternativeNames = List(String)
    description = String()
    portraitLink = String()


class Query(ObjectType):
    character = Field(Character, fullName=String(required=True))

    def resolve_character(self, info, fullName):
        logging.info(f"Resolving character {fullName}")
        # Query vectordb
        result_docs = query_texts_weaviate(fullName)
        logging.info(f"Got {len(result_docs)} results")
        # Limit size of results
        token_limited_results = limit_docs_by_tokens(
            result_docs, model="gpt-4", token_limit=1000)
        logging.info(f"Getting description for {fullName}")
        # Call to OpenAI
        desc = get_character_description_summary(
            docs=token_limited_results, character=fullName)

        # Call to image generator
        portrait_link = generate_image(desc)
        return Character(fullName=fullName, alternativeNames=["test"], description=desc, portraitLink=portrait_link)


def query_texts_chroma(fullName: str) -> list[str]:
    collection = df.chroma_client.get_collection("infinite_jest")
    print(collection.count())
    results = collection.query(
        query_texts=[f"the physical appearance of {fullName}"], n_results=15)
    result_docs = results["documents"][0]
    return result_docs


def query_texts_weaviate(fullName: str) -> list[str]:
    results = df.weaviate_client.query.get(ChunkType.PAGE.value, ["text"]).with_near_text(
        {"concepts": [f"the pyhsical appearance of {fullName}"], "distance": 0.2}).with_limit(20).do()
    print(json.dumps(results, indent=2))
    # result_docs = [r["text"]
    #                for r in results["data"]["Get"][ChunkType.PAGE.value]]
    return []  # result_docs


schema = build_schema(Query)

if __name__ == "__main__":
    from graphql import graphql
    result = graphql(schema, '{ _service { sdl } }')
    print(result.data["_service"]["sdl"].strip())
