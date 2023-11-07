import os
import logging

from dotenv import load_dotenv
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
import google.cloud.logging

from schema.schema import schema
from vector_management.text_processing import load_or_open_chunks_and_pages
from vector_management.weaviate import initialize_schema, configure_batches, ChunkType
from vector_management.chroma import initialize_collection
from dependency_factory import dependency_factory as df

load_dotenv()


def initialize_chroma_vectordb():
    logging.info("Hello here i am")
    pages, chunks20, chunks10 = load_or_open_chunks_and_pages(
        root_dir="./data/")
    logging.info(f"Got {len(chunks20)} 20 sentance chunks")
    logging.info(f"Got {len(chunks10)} 10 sentance chunks")
    try:
        initialize_collection(df.chroma_client, pages)
    except Exception:
        return "Error initializing collection", 500
    return "OK", 200


def initialize_wv_vectordb():
    pages, chunks20, chunks10 = load_or_open_chunks_and_pages(
        root_dir="./data/")
    try:
        configure_batches(chunks20, chunk_type=ChunkType.CHUNK20,
                          purge=True, root_dir="../data/")
        configure_batches(chunks10, chunk_type=ChunkType.CHUNK10,
                          purge=False, root_dir="../data/")
        configure_batches(pages, chunk_type=ChunkType.PAGE,
                          purge=False, root_dir="../data/")
    except Exception as e:
        return f"Error configuring batches: {e}", 500
    return "OK", 200


class App:
    def __init__(self):
        # Set up flask app
        app = Flask(__name__)
        CORS(app, origins=["http://localhost:5173",
             "https://ij-frontend-ka2xis5sma-uc.a.run.app", "https://infinite-jest.arb.haus"])
        app.debug = True
        app.add_url_rule(
            '/graphql',
            view_func=GraphQLView.as_view(
                'graphql',
                schema=schema,
                graphiql=True
            )
        )
        # Set up logging
        if os.environ.get("ENV") != "development":
            logging_client = google.cloud.logging.Client()
            logging_client.setup_logging()

        # Initialize collection
        match os.environ.get("VECTORDB", "chroma"):
            case "chroma":
                initialize_chroma_vectordb()
            case "weaviate":
                initialize_schema()
                app.add_url_rule(
                    '/reinitialize_vectordb',
                    view_func=initialize_wv_vectordb
                )
        self.app = app

    def run(self, port):
        self.app.run(host='0.0.0.0', port=port)


app = App()


@app.app.route('/')
def health_check():
    return "OK", 200


if __name__ == '__main__':
    app.run(os.environ.get('PORT', 8000))
