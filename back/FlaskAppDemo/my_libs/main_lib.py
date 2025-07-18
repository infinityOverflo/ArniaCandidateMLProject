from pathlib import Path
from my_libs import ai_lib

from werkzeug.datastructures import FileStorage

save_path = Path("Uploads/")

def save_uploaded_files(files: list[FileStorage]):
    temp_path = save_path
    type_check = ai_lib.FileTypeConverter.get_file_type(files[0].filename)
    if type_check == ai_lib.FileTypeEnum.PDF:
        temp_path = save_path / "pdf"
    if not temp_path.exists():
        temp_path.mkdir(parents=True, exist_ok=True)

    for file in files:
        file_path = temp_path / file.filename
        file.save(file_path)

    return [temp_path / file.filename for file in files]

def process_files(file_paths: list[Path]):
    file_type = ai_lib.FileTypeConverter.get_file_type(file_paths[0].name)
    if file_type == ai_lib.FileTypeEnum.PDF:
        read_pdf = ai_lib.Reader(file_paths=file_paths, Reader=ai_lib.ReadPdf())
        read_pdf.read_files()
        dict_files = read_pdf.get_content()
        dict_chunks = ai_lib.chunk_files(dict_files)
        return dict_chunks
    else:
        raise ValueError("Unsupported file type")

def print_chunks(chunks: dict[str, list[ai_lib.Chunks]]):
    for file_name, file_chunks in chunks.items():
        print(f"File: {file_name}")
        for chunk in file_chunks:
            print(f"  Chunk: {chunk.get_chunks_contents()}")