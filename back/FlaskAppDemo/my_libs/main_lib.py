from pathlib import Path
from my_libs import ai_lib

from werkzeug.datastructures import FileStorage

save_path = Path("Data/Uploads/")

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
    if file_type == ai_lib.FileTypeEnum.TEXT:
        return ai_lib.chunk_texts(file_paths)
    elif file_type == ai_lib.FileTypeEnum.PDF:
        return ai_lib.chunk_files(file_paths)
    else:
        raise ValueError("Unsupported file type")