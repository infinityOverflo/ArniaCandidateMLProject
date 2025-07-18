from flask import Flask, request, url_for
from flask_cors import CORS

import dotenv
import os
from pathlib import Path

from my_libs.ai_lib import FileTypeEnum, FileTypeConverter, File, Files, Chunk, Chunks, chunk_texts, chunk_files, ollama_embed
from my_libs.main_lib import print_chunks, process_debug, process_files, save_uploaded_files

dotenv.load_dotenv()
LOCAL_NETWORK_PC = os.getenv("LOCAL_NETWORK_PC")
OLLAMA_API_HOST = LOCAL_NETWORK_PC + ":11434"
embedding_model = 'dengcao/Qwen3-Embedding-4B:Q5_K_M'
textsPath = Path("../Datasets/Source1/processed")

processed_files: dict[str, list[Chunks]] = {}

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/upload", methods=["GET"])
def send_hello_message():
    return {"message": "Hello!"}, 200

@app.route("/upload", methods=["POST"])
def receive_files():
    files = request.files.getlist("files")
    if not files:
        return {"error": "No files uploaded"}, 400
    saved_files_paths = save_uploaded_files(files)
    processed_files: dict[str, list[Chunks]] = process_files(saved_files_paths)
    print_chunks(processed_files)

    return {"message": f"Flask Received Files: {saved_files_paths}"}, 200

@app.route("/debug", methods=["GET"])
def debug():
    process_debug()
    return {"message": "Debug Processed"}, 200