from flask import Flask, request, url_for
from flask_cors import CORS

import dotenv
import os
from pathlib import Path

from my_libs.ai_lib import FileTypeEnum, FileTypeConverter, File, Files, Chunk, Chunks, chunk_texts, chunk_files, ollama_embed
from my_libs.main_lib import save_uploaded_files

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
    save_uploaded_files(files)
    return {"message": f"Flask Received Files"}, 200

