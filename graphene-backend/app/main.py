import os

import chromadb
from dotenv import load_dotenv
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS

from schema.schema import schema
from robot.text_processing import load_or_open_chunks_and_pages
from robot.chroma import initialize_collection
from dependency_factory import dependency_factory as df

load_dotenv()


def initialize_vectordb():
    _, pages = load_or_open_chunks_and_pages(root_dir="./data/")
    initialize_collection(df.chroma_client, pages)


class App:
    def __init__(self):
        # Set up flask app
        app = Flask(__name__)
        CORS(app, origins=["http://localhost:5173",
             "https://ij-frontend-ka2xis5sma-uc.a.run.app"])
        app.debug = True
        app.add_url_rule(
            '/graphql',
            view_func=GraphQLView.as_view(
                'graphql',
                schema=schema,
                graphiql=True
            )
        )
        app.add_url_rule(
            '/initialize_collection',
            view_func=initialize_vectordb
        )
        self.app = app

    def run(self, port):
        self.app.run(host='0.0.0.0', port=port)


app = App()


@app.app.route('/')
def health_check():
    return "OK", 200


if __name__ == '__main__':
    # chunks, pages = load_or_open_chunks_and_pages(root_dir="./data/")
    # collection = initialize_collection(df.chroma_client, pages)
    # test = df.chroma_client.get_collection("infinite_jest")
    # print(test.count())
    app.run(os.environ.get('PORT', 8000))
