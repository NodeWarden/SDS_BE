#conversione con serializer di tutta la cartella di input fino a sezione 4, successive superflue.

from pathlib import Path
from rich.panel import Panel
from rich.console import Console
from docling.document_converter import DocumentConverter
from docling_core.transforms.serializer.markdown import MarkdownDocSerializer

DOC_SOURCE = Path("./data")
file_list = list(DOC_SOURCE.glob("*.pdf"))
out_dir = Path("./data/processed")
out_dir.mkdir(parents=True, exist_ok=True)


start_cue = "SEZIONE 1"
stop_cue =  "SEZIONE 4"

console =Console()
def print_in_console(text):
    console.print(Panel(text))
for file_path in file_list:
    if file_path.is_file():
        converter = DocumentConverter()
        doc = converter.convert(source=file_path).document

        serializer = MarkdownDocSerializer(doc=doc)
        ser_result = serializer.serialize()
        ser_text = ser_result.text
        with open(out_dir / f"{file_path.stem}_chunk.txt", "w", encoding="utf-8") as f:
            f.write(ser_text[ser_text.find(start_cue) : ser_text.find(stop_cue)])
            print(f"Saved chunk to {out_dir / f'{file_path.stem}_chunk.txt'}")