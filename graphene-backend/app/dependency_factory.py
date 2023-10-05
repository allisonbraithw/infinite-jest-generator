import chromadb
import os


class DependencyFactory:

    # Service Clients
    _chroma_client = None

    @property
    def chroma_client(self):
        if self._chroma_client is None:
            self._chroma_client = chromadb.HttpClient(host=os.environ.get(
                "CHROMA_HOST"), port=os.environ.get("CHROMA_PORT"))
        return self._chroma_client


dependency_factory = DependencyFactory()
