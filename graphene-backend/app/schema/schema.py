from graphene import Field, ObjectType, String, List
from graphene_federation import build_schema
from robot.character_query import get_character_description_summary
from robot.text_processing import limit_docs_by_tokens
from dependency_factory import dependency_factory as df


class Character(ObjectType):
    fullName = String(required=True)
    alternativeNames = List(String)
    description = String()


class Query(ObjectType):
    character = Field(Character, fullName=String(required=True))

    def resolve_character(self, info, fullName):
        collection = df.chroma_client.get_collection("infinite_jest")
        print(collection.count())
        results = collection.query(
            query_texts=[f"the physical appearance of {fullName}"], n_results=15)
        result_docs = results["documents"][0]
        token_limited_results = limit_docs_by_tokens(result_docs)
        desc = get_character_description_summary(
            docs=token_limited_results, character=fullName)
        return Character(fullName=fullName, alternativeNames=["test"], description=desc)


schema = build_schema(Query)

if __name__ == "__main__":
    from graphql import graphql
    result = graphql(schema, '{ _service { sdl } }')
    print(result.data["_service"]["sdl"].strip())
