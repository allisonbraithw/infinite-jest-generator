import logging

from typing import List as list
from graphene import Field, ObjectType, String, List, Boolean
from graphene_federation import build_schema
from image_gen.generate_image import generate_image
from inference.character_query import get_character_description_summary
from vector_management.text_processing import limit_docs_by_tokens
from vector_management.weaviate import ChunkType
from vector_management.evaluation import evaluate_relevancy_bespoke
from dependency_factory import dependency_factory as df
from sentence_transformers import SentenceTransformer


class DescriptionEval(ObjectType):
    relevancy = String()
    explanation = String()


class Character(ObjectType):
    full_name = String(required=True)
    alternative_names = List(String)
    sources = List(String, required=True)
    description = String(required=True)
    portrait_link = String()
    evaluation = Field(DescriptionEval)

    def resolve_portrait_link(parent, info):
        return generate_image(parent.description)

    def resolve_evaluation(parent, info):
        # return evaluate_relevancy(query=f"the physical appearance of {parent.full_name}", docs=parent.sources, response=parent.description)
        return evaluate_relevancy_bespoke(character=parent.full_name, response=parent.description)


class Query(ObjectType):
    character = Field(Character, fullName=String(required=True))

    def resolve_character(self, info, fullName):
        logging.info(f"Resolving character {fullName}")
        # Query vectordb
        result_docs = query_texts_weaviate(fullName)
        print(result_docs)
        logging.info(f"Got {len(result_docs)} results")
        # Limit size of results
        token_limited_results = limit_docs_by_tokens(
            result_docs, model="gpt-4", token_limit=1000)
        print(token_limited_results)
        logging.info(f"Getting description for {fullName}")
        # Call to OpenAI
        desc = get_character_description_summary(
            docs=token_limited_results, character=fullName)

        return Character(full_name=fullName, alternative_names=["test"], description=desc, sources=token_limited_results)


def query_texts_chroma(fullName: str) -> list[str]:
    collection = df.chroma_client.get_collection("infinite_jest")
    results = collection.query(
        query_texts=[f"the physical appearance of {fullName}"], n_results=15)
    result_docs = results["documents"][0]
    return result_docs


def query_texts_weaviate(fullName: str) -> list[str]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(f"the pyhsical appearance of {fullName}")
    nearVector = {"vector": embeddings.tolist(), "distance": 0.65}
    results = df.weaviate_client.query.get(ChunkType.CHUNK20.value, [
                                           "text"]).with_near_vector(nearVector).with_limit(20).do()
    logging.info(
        f'returned {len(results["data"]["Get"][ChunkType.CHUNK20.value])} results')
    result_docs = [r["text"]
                   for r in results["data"]["Get"][ChunkType.CHUNK20.value]]
    return result_docs


schema = build_schema(Query)

if __name__ == "__main__":
    from graphql import graphql
    result = graphql(schema, '{ _service { sdl } }')
    print(result.data["_service"]["sdl"].strip())
