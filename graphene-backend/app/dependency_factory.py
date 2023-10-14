import chromadb
import weaviate
import os


class DependencyFactory:

    # Service Clients
    _chroma_client = None
    _weaviate_client = None

    @property
    def chroma_client(self):
        if self._chroma_client is None:
            self._chroma_client = chromadb.HttpClient(host=os.environ.get(
                "CHROMA_HOST"), port=os.environ.get("CHROMA_PORT"))
        return self._chroma_client

    @property
    def weaviate_client(self):
        if self._weaviate_client is None:
            auth_config = weaviate.AuthApiKey(
                api_key=os.environ.get("WEAVIATE_API_KEY"))
            self._weaviate_client = weaviate.Client(
                url=os.environ.get("WEAVIATE_HOST"),
                auth_client_secret=auth_config,
                additional_headers={
                    "X-OpenAI-Api-Key": os.environ.get("OPENAI_API_KEY")
                })
        return self._weaviate_client


dependency_factory = DependencyFactory()
