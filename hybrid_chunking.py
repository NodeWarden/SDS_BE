from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker


FOLDER_PATH = Path("./data")
file_list = list(FOLDER_PATH.glob("*.pdf")) 

output_path = Path("./data/processed")
output_path.mkdir(parents=True, exist_ok=True)

converter = DocumentConverter()
chunker = HybridChunker()


for file_path in file_list:
    try:
        result = converter.convert(file_path)
        doc = result.document
        chunk_iter = chunker.chunk(doc)
        for i, chunk in enumerate(chunk_iter):
            if chunk.text.startswith("4.1"):
                break
            with open(output_path / f"{file_path.stem}_chunk_{i}.txt", "w", encoding="utf-8") as f:
                f.write(chunk.text)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        continue