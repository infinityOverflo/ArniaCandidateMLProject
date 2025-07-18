from abc import ABC, abstractmethod

from multiprocessing import Pool

import os
from enum import Enum
from pathlib import Path
import shutil
import requests
import json
import dotenv
import pypdf
from kaggle.api.kaggle_api_extended import KaggleApi
from ollama import Client, EmbedResponse

class MetaData:
    def __init__(self):
        self.model_name = 'dengcao/Qwen3-Embedding-4B:Q5_K_M'
        self.embed_size = 2560
        self.local_network_pc = "localhost"
        self.ollama_api_host = f"{self.local_network_pc}:11434"

class FileTypeEnum(Enum):
    NAF = 0
    TEXT = 1
    PDF = 2

class FileTypeConverter:
    def __init__(self, file_type: FileTypeEnum):
        self.file_type: FileTypeEnum = file_type

    type_suffix_conversion: dict[FileTypeEnum, str] = {
            FileTypeEnum.NAF: "",
            FileTypeEnum.TEXT: ".txt",
            FileTypeEnum.PDF: ".pdf",
        }
    suffix_type_conversion: dict[str, FileTypeEnum] = {v: k for k, v in type_suffix_conversion.items() if v}

    @staticmethod
    def get_file_type(file_name: str) -> FileTypeEnum | None:
        suffix = Path(file_name).suffix
        return FileTypeConverter.from_suffix(suffix)

    @staticmethod
    def from_suffix(suffix: str) -> FileTypeEnum | None:
        return FileTypeConverter.suffix_type_conversion.get(suffix)

    @staticmethod
    def to_suffix(file_type: FileTypeEnum) -> str:
        return FileTypeConverter.type_suffix_conversion.get(file_type, "")
    
class Chunk:
    def __init__(self, content: str = ""):
        self.content: str = content
        self.embeddings: list[float] = []

    def set_content(self, content: str) -> None:
        self.content = content
    def set_embeddings(self, embeddings: list[float]) -> None:
        self.embeddings = embeddings

    def get_content(self) -> str:
        return self.content
    def get_embeddings(self) -> list[float]:
        return self.embeddings
    
class Chunks:
    def __init__(self, chunks: list[Chunk] = None):
        self.chunks: list[Chunk] = chunks if chunks is not None else []

    def add_chunk(self, chunk: Chunk) -> None:
        self.chunks.append(chunk)

    def get_chunks(self) -> list[Chunk]:
        return self.chunks

    def get_chunks_contents(self) -> list[str]:
        return [chunk.get_content() for chunk in self.chunks]
    
    def get_chunks_embeddings(self) -> list[list[float]]:
        return [chunk.get_embeddings() for chunk in self.chunks]
    
class File:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self.content: str = ""
        self.chunks: list[Chunk] = []

    def __getitem__(self, idx: int) -> str:
        if idx >= len(self.content):
            raise IndexError("Index out of range")
        return self.content[idx]
    
    def __len__(self) -> int:
        return len(self.content)
    
    def __iter__(self):
        return iter(self.content)
    
class Files:
    def __init__(self, files_type: FileTypeEnum = FileTypeEnum.NAF) -> None:
        self.files_type: FileTypeEnum = files_type
        self.files: list[File] = []
        
    def __getitem__(self, index: int) -> File:
        return self.files[index]
    
    def __len__(self) -> int:
        return len(self.files)
    
    def __iter__(self):
        return iter(self.files)

    def get_type(self) -> FileTypeEnum:
        return self.files_type
    
    def get_file(self, index: int) -> File:
        return self.files[index]
    
    def get_files(self) -> list[File]:
        return self.files
    
    def add_file(self, file: File) -> None:
        self.files.append(file)

    def add_files(self, files: list[File]) -> None:
        self.files.extend(files)

class AbstractReaderType(ABC):
    @abstractmethod
    def get_type(self) -> FileTypeEnum:
        raise NotImplementedError("This method should be overridden by subclasses")
    @abstractmethod
    def read_dir(self) -> Files:
        raise NotImplementedError("This method should be overridden by subclasses")
    @abstractmethod
    def read_files(self) -> Files:
        raise NotImplementedError("This method should be overridden by subclasses")
    
class ReadPdf(AbstractReaderType):
    def __init__(self) -> None:
        self.files: Files = Files(FileTypeEnum.PDF)

    def get_type(self) -> FileTypeEnum:
        return FileTypeEnum.PDF

    def read_dir(self, dir_path: Path) -> Files:
        self.files = Files(FileTypeEnum.PDF)
        for pdf_file in dir_path.iterdir():
            if pdf_file.is_file() and pdf_file.suffix == FileTypeConverter.to_suffix(FileTypeEnum.PDF):
                reader = pypdf.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            if text:
                file = File(pdf_file)
                file.content = text
                self.files.add_file(file)
        return self.files

    def read_files(self, file_paths: list[Path]) -> Files:
        self.files = Files(FileTypeEnum.PDF)
        for pdf_file in file_paths:
            if pdf_file.is_file() and pdf_file.suffix == FileTypeConverter.to_suffix(FileTypeEnum.PDF):
                reader = pypdf.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            if text:
                file = File(pdf_file)
                file.content = text
                self.files.add_file(file)
        return self.files

class Reader:
    def __init__(self, Reader: AbstractReaderType, dir_path: Path = None, file_paths: list[Path] = None) -> None:
            self.reader: AbstractReaderType = Reader
            self.dir_path: Path = dir_path if dir_path else Path()
            self.file_paths: list[Path] = file_paths if file_paths else []

            self.content: dict[str, Files] = {}

    def read_dir(self) -> None:
        for child_dir in self.dir_path.iterdir():
            if child_dir.is_file():
                continue
            self.content[child_dir.name] = self.reader.read_dir(child_dir)
    
    def read_files(self) -> None:
        for child_file in self.file_paths:
            if child_file.is_dir():
                continue
            self.content[child_file.name] = self.reader.read_files([child_file])

    def get_content(self) -> dict[str, Files]:
        return self.content
    
def read_text_files(texts_dir_path: Path) -> dict[str, list[str]]:
    texts_dict: dict[str, list[str]] = {}
    for dir in texts_dir_path.iterdir():
        if not dir.is_dir():
            continue
        texts_dict[dir.name] = []
        for file in dir.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                texts_dict[dir.name].append(f.read())
    return texts_dict

def chunk_sliding_window(text: str, window_size: int = 150, step_size: int = 100) -> Chunks:
    chunks =  Chunks(
        [Chunk(text[i:i + window_size]) for i in range(0, len(text), step_size) if i + window_size <= len(text)]
    )
    if len(text) > 0 and (len(text) - window_size) % step_size != 0 and (len(text) - 1) % step_size != 0:
        last_start = ((len(text) - 1) // step_size) * step_size
        if last_start < len(text) - 1:
            chunks.add_chunk(Chunk(text[last_start:]))
    return chunks

def chunk_files(files_dict: dict[str, Files]) -> dict[str, list[Chunks]]:
    window_size = 150
    step_size = 100
    chunks_dict: dict[str, list[Chunks]] = {}
    
    for key in files_dict.keys():
        chunks_dict[key] = []
        files_with_key = files_dict[key]
        for file in files_with_key.get_files():
            text = file.content
            chunks = chunk_sliding_window(text, window_size, step_size)
            chunks_dict[key].append(chunks)
    return chunks_dict

def chunk_texts(texts_dict: dict[str, list[str]]) -> dict[str, list[Chunks]]:
    window_size = 150
    step_size = 100
    chunks_dict: dict[str, list[Chunks]] = {}
    
    for key in texts_dict.keys():
        chunks_dict[key] = []
        for text in texts_dict[key]:
            chunks = chunk_sliding_window(text, window_size, step_size)
            chunks_dict[key].append(chunks)
    return chunks_dict

def ollama_embed(client: Client, with_input: list[str], embedding_model: str) -> EmbedResponse:
    response = client.embed(model=embedding_model, 
                                    input=with_input)
    return response

def main():
    dotenv.load_dotenv()
    LOCAL_NETWORK_PC = os.getenv("LOCAL_NETWORK_PC")
    OLLAMA_API_HOST = LOCAL_NETWORK_PC + ":11434"
    kg_api = KaggleApi()
    kg_api.authenticate()

    DatasetSavePath = Path("../Datasets/Source1/raw/data")
    datasetPath = DatasetSavePath
    embedding_model = 'dengcao/Qwen3-Embedding-4B:Q5_K_M'

    textsPath = Path("../Datasets/Source1/processed")
    texts_dict = read_text_files(textsPath)

    chunked_texts = chunk_texts(texts_dict)
    tst = chunked_texts["accountant"][0].get_chunks_contents()
    print(tst[0])

    OllamaClient = Client(
        host=OLLAMA_API_HOST,
    )
    with_input = "TEST"

    response = ollama_embed(OllamaClient, with_input, embedding_model)
    print(response)