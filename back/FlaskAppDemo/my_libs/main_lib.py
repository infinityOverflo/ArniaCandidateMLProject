import inspect
from pathlib import Path

import psycopg
from werkzeug.datastructures import FileStorage

from .ai_lib import FileTypeEnum, FileTypeConverter, MetaData, Reader, ReadPdf, Chunk, Chunks, Files, Files, chunk_files, ollama_embed
from ollama import Client, EmbedResponse


save_path = Path("Uploads/")

def save_uploaded_files(files: list[FileStorage]):
    temp_path = save_path
    type_check = FileTypeConverter.get_file_type(files[0].filename)
    if type_check == FileTypeEnum.PDF:
        temp_path = save_path / "pdf"
    if not temp_path.exists():
        temp_path.mkdir(parents=True, exist_ok=True)

    for file in files:
        file_path = temp_path / file.filename
        file.save(file_path)

    return [temp_path / file.filename for file in files]

def process_files(file_paths: list[Path]):
    file_type = FileTypeConverter.get_file_type(file_paths[0].name)
    if file_type == FileTypeEnum.PDF:
        read_pdf = Reader(file_paths=file_paths, Reader=ReadPdf())
        read_pdf.read_files()
        dict_files = read_pdf.get_content()
        dict_chunks = chunk_files(dict_files)
        return dict_chunks
    else:
        raise ValueError("Unsupported file type")

def print_chunks(chunks: dict[str, list[Chunks]]):
    for file_name, file_chunks in chunks.items():
        print(f"File: {file_name}")
        for chunk in file_chunks:
            print(f"  Chunk: {chunk.get_chunks_contents()}")

def handle_db():
    # Connect to an existing database
    with psycopg.connect(f"dbname=test user=postgres") as conn:
        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Execute a command: this creates a new table
            cur.execute("""
                CREATE TABLE test (
                    id serial PRIMARY KEY,
                    num integer,
                    data text)
                """)
            # Pass data to fill a query placeholders and let Psycopg perform
            # the correct conversion (no SQL injections!)
            cur.execute(
                "INSERT INTO test (num, data) VALUES (%s, %s)",
                (100, "abc'def"))
            # Query the database and obtain data as Python objects.
            cur.execute("SELECT * FROM test")
            print(cur.fetchone())
            # will print (1, 100, "abc'def")
            # You can use `cur.executemany()` to perform an operation in batch
            cur.executemany(
                "INSERT INTO test (num) values (%s)",
                [(33,), (66,), (99,)])
            # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
            # of several records, or even iterate on the cursor
            cur.execute("SELECT id, num FROM test order by num")
            for record in cur:
                print(record)
            # Make the changes to the database persistent
            conn.commit()

def embed_chunks(processed_files: dict[str, list[Chunks]]) -> dict[str, list[Chunks]]:
    metadata = MetaData()
    ollama_client = Client(
        host=metadata.ollama_api_host,
    )

    for chunks_list in processed_files.values():
        for chunks in chunks_list:
            for chunk_in_chunks in chunks.get_chunks():
                if chunk_in_chunks:
                    ollama_response = ollama_embed(ollama_client, chunk_in_chunks.get_content(), metadata.model_name)
                    chunk_in_chunks.set_embeddings(ollama_response.embeddings)
                    print(chunk_in_chunks.get_embeddings())
                    # print(len(ollama_response.embeddings[0]))
    
    return processed_files

def add_embeddings_to_db(processed_files: dict[str, list[Chunks]]):
    metadata = MetaData()
    with psycopg.connect(f"dbname=postgres user=postgres") as conn:
        with conn.cursor() as cur:
            print("CONNECTED TO DB")
            for file_name, chunks_list in processed_files.items():
                for chunks in chunks_list:
                    for chunk_in_chunks in chunks.get_chunks():
                        if chunk_in_chunks.get_embeddings():
                            cur.execute(
                                "INSERT INTO items (file_name, embedding) VALUES (%s, %s)",
                                (file_name, chunk_in_chunks.get_embeddings())
                            )
        conn.commit()

def do_more(*args, **kwargs):
    # # handle_db()
    # metadata = MetaData()
    # OllamaClient = Client(
    #     host=metadata.ollama_api_host,
    # )

    # if "dict_chunks" in kwargs:
    #     dict_chunks = kwargs["dict_chunks"]
    #     for file_name, chunks_list in dict_chunks.items():
    #         for chunks in chunks_list:
    #             for chunk_in_chunks in chunks.get_chunks():
    #                 if chunk_in_chunks:
    #                     # Assuming ollama_embed is a function that takes a Client and content
    #                     ollama_response = ollama_embed(OllamaClient, chunk_in_chunks.get_content(), metadata.model_name)
    #                     chunk_in_chunks.set_embeddings(ollama_response.embeddings)
    #                     print(len(ollama_response.embeddings[0]))
                        # print(f"Processed chunk from {file_name}: {chunk_in_chunks[:50]}...")  # Print first 50 chars

    # ollama_response = ollama_embed(OllamaClient, "Hello World", metadata.model_name)
    # # print(f"Ollama Embed Response: {ollama_response}")
    # pass
    pass

def debug_with(*args, **kwargs):
    for arg in args:
        if inspect.isfunction(arg):
            # print(inspect.getfullargspec(arg))
            pass
        else:
            if isinstance(arg, dict):
                # print_chunks(arg)
                pass

def debug(*args, **kwargs):
    debug_with(*args, **kwargs)
    do_more(*args, **kwargs)

    print("Debug Processed")