import os
import logging

from dotenv import load_dotenv
from flask import Flask
from flask_graphql import GraphQLView
from flask_sockets import Sockets
from graphql_ws.gevent import GeventSubscriptionServer
from graphql.backend import GraphQLCoreBackend
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
    chunks, pages = load_or_open_chunks_and_pages(root_dir="./data/")
    logging.info(f"Got {len(chunks)} chunks")
    logging.info(f"random chunk: {chunks[53]}")
    try:
        initialize_collection(df.chroma_client, pages)
    except Exception:
        return "Error initializing collection", 500
    return "OK", 200


def initialize_wv_vectordb():
    chunks, pages = load_or_open_chunks_and_pages(root_dir="./data/")
    try:
        configure_batches(chunks, chunk_type=ChunkType.CHUNK,
                          purge=True, root_dir="./data/")
        configure_batches(pages, chunk_type=ChunkType.PAGE,
                          purge=False, root_dir="./data/")
    except Exception as e:
        return f"Error configuring batches: {e}", 500
    return "OK", 200


class CustomBackend(GraphQLCoreBackend):
    def __init__(self, executor=None):
        super().__init__(executor)
        self.execute_params["allow_subscriptions"] = True


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

# Setup Sockets
sockets = Sockets(app)
subscription_server = GeventSubscriptionServer(schema)
app.app_protocol = lambda environ_path_info: 'graphql-ws'


@app.route('/')
def health_check():
    return "OK", 200


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    print(os.environ.get("OPENAI_ORG"))
    server = pywsgi.WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
