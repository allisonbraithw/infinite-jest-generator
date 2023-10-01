import os

import chromadb
from flask import Flask
from flask_graphql import GraphQLView

from schema.schema import schema
from robot.text_processing import load_or_open_chunks_and_pages
from robot.chroma import initialize_collection
from dependency_factory import dependency_factory as df


class App:
    def __init__(self):
        # Set up flask app
        app = Flask(__name__)
        app.debug = True
        app.add_url_rule(
            '/graphql',
            view_func=GraphQLView.as_view(
                'graphql',
                schema=schema,
                graphiql=True
            )
        )
        self.app = app

    def run(self, port):
        self.app.run(port=port)


app = App()


if __name__ == '__main__':
    chunks, pages = load_or_open_chunks_and_pages(root_dir="../data/")
    collection = initialize_collection(df.chroma_client, pages)
    test = df.chroma_client.get_collection("infinite_jest")
    print(test.count())
    app.run(os.environ.get('PORT', 8000))
