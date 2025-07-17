from pathlib import Path
from my_libs import ai_lib

from werkzeug.datastructures import FileStorage

save_path = Path("Data/Uploads/")

def save_uploaded_files(files: list[FileStorage]):
    # save files to a specific directory
    for file in files:
        path = save_path / file.filename
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        file.save(path)