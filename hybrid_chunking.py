from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from pathlib import Path


FOLDER_PATH = Path("./data")
file_list = list(FOLDER_PATH.glob("*.pdf")) 

output = []

converter = DocumentConverter(file_path=file_list, chunker=HybridChunker())

for file_path in file_list:
    if file_path.is_file():
        doc_iter = converter.convert(file_path=str(file_path))