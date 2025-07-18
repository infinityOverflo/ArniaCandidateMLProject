from flask import Flask, request, url_for, current_app
from flask_cors import CORS

import dotenv
import os
from pathlib import Path

from my_libs.ai_lib import FileTypeEnum, FileTypeConverter, File, Files, Chunk, Chunks, chunk_texts, chunk_files, ollama_embed
from my_libs.main_lib import add_embeddings_to_db, process_files, save_uploaded_files, embed_chunks, do_more, debug

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins=["http://localhost:3000"])

    dotenv.load_dotenv()
    app.config.from_mapping(
        SQL_P = os.getenv("SQL_PASSWORD", "default_password"),
    )

    processed_files = {}

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile('config.py', silent=True)
        pass
    else:
        # load the test config if passed in
        # app.config.from_mapping(test_config)
        pass

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/upload", methods=["GET"])
    def send_hello_message():
        return {"message": "Hello!"}, 200

    @app.route("/upload", methods=["POST"])
    def receive_files():
        global processed_files

        files = request.files.getlist("files")
        if not files:
            return {"error": "No files uploaded"}, 400
        saved_files_paths = save_uploaded_files(files)
        processed_files = process_files(saved_files_paths)
        embedded_chunks = embed_chunks(processed_files)
        add_embeddings_to_db(embedded_chunks)
        return {"message": f"Flask Received Files: {saved_files_paths}"}, 200

    @app.route("/debug", methods=["GET"])
    def do_debug():
        global processed_files
        debug(dict_chunks=processed_files)
        return {"message": "Debug Processed"}, 200

    return app
