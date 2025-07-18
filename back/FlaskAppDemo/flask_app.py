from flask import Flask, request, url_for
from flask_cors import CORS

import dotenv
import os
from pathlib import Path

from my_libs.ai_lib import FileTypeEnum, FileTypeConverter, File, Files, Chunk, Chunks, chunk_texts, chunk_files, ollama_embed
from my_libs.main_lib import process_files, save_uploaded_files

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

dotenv.load_dotenv()
LOCAL_NETWORK_PC = os.getenv("LOCAL_NETWORK_PC")
OLLAMA_API_HOST = LOCAL_NETWORK_PC + ":11434"
embedding_model = 'dengcao/Qwen3-Embedding-4B:Q5_K_M'

textsPath = Path("../Datasets/Source1/processed")

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
    for processed_files_name, processed_files_chunks in processed_files.items():
        for chunk in processed_files_chunks:
            chunk_contents = chunk.get_chunks_contents()
            print(f"Processed {processed_files_name} with chunks: {chunk_contents}")
    return {"message": f"Flask Received Files: {saved_files_paths}"}, 200