import logging
import pandas as pd
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker


FOLDER_PATH = Path("./data")
file_list = list(FOLDER_PATH.glob("*"))
out_dir = Path("./data/processed")
out_dir.mkdir(parents=True, exist_ok=True)

converter = DocumentConverter()
chunker = HybridChunker()

for file_path in file_list:
    if file_path.is_file():
        loader = DoclingLoader(file_path = str(file_path))
        doc_iter = loader.lazy_load()
        for d in doc_iter:
            if d.page_content.startswith("3.2"):
                # conv_res = converter.convert(d.page_content)
                for table_ix, table in enumerate(d.tables):
                    table_df: pd.DataFrame = table.export_to_dataframe()
                    print(f" ## Table {table_ix}")
                    print(table_df.to_markdown())
                    with open(out_dir / f"{file_path.stem}_chunk.txt", "a", encoding="utf-8") as f:
                        f.write(table_df.to_markdown())
                        print(f"Saved table to {out_dir / f'{file_path.stem}_chunk.txt_'}")
                break
            print(f"Document:  {d.metadata['source']}: {d.page_content=}")
            with open(out_dir / f"{file_path.stem}_chunk.txt", "a", encoding="utf-8") as f:
                f.write(d.page_content)
                print(f"Saved chunk to {out_dir / f'{file_path.stem}_chunk.txt'}")
