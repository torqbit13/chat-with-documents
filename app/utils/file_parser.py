import os
from typing import IO
import PyPDF2


def parse_file(file: IO) -> str:
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        reader = PyPDF2.PdfReader(file.file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        return text
    elif ext == ".txt":
        return file.file.read().decode("utf-8")
    elif ext == ".docx":
        raise ValueError(
            "DOCX parsing is not supported. Please upload PDF or TXT files."
        )
    else:
        raise ValueError("Unsupported file type. Only PDF and TXT are supported.")
