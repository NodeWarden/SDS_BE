import re
from pathlib import Path
from langchain_docling import DoclingLoader

FOLDER_PATH = Path("./data")
file_list = list(FOLDER_PATH.glob("*.pdf"))
out_dir = Path("./data/processed")
out_dir.mkdir(parents=True, exist_ok=True)

loader = DoclingLoader(file_path = file_list)

for file_path in file_list:
    if file_path.is_file():
        loader = DoclingLoader(file_path = str(file_path))
        doc_iter = loader.lazy_load()
        for d in doc_iter:
            if d.page_content.startswith("4.1"):
                break
            if d.page_content.startswith("1.1"):
                product_name = re.search("Nome commerciale.:")
            print(f"Document:  {d.metadata['source']}: {d.page_content=}")
            with open(out_dir / f"{file_path.stem}_chunk.txt", "a", encoding="utf-8") as f:
                f.write(d.page_content)
                f.write("\n")
                print(f"Saved chunk to {out_dir / f'{file_path.stem}_chunk.txt'}")
