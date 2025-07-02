
from pathlib import Path
from langchain_docling import DoclingLoader


FOLDER_PATH = Path("./guidelines")
file_list = list(FOLDER_PATH.glob("*")) 
loader = DoclingLoader(file_path = file_list)


for file_path in file_list:
    if file_path.is_file():
        loader = DoclingLoader(file_path = str(file_path))
        doc_iter = loader.lazy_load()
        for d in doc_iter:
            print(f"Document: {d.metadata['source']}: {d.page_content=}")