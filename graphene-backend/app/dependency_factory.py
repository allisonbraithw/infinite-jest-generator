import chromadb


class DependencyFactory:

    # Service Clients
    _chroma_client = None

    @property
    def chroma_client(self):
        if self._chroma_client is None:
            self._chroma_client = chromadb.Client()
        return self._chroma_client


dependency_factory = DependencyFactory()
