from pathlib import Path
from rich.panel import Panel
from rich.console import Console
from docling.document_converter import DocumentConverter
from docling_core.transforms.serializer.markdown import MarkdownDocSerializer

DOC_SOURCE = Path("./guidelines/RC_016_25_Malossi_salute_pag23.pdf")
out_dir = Path("./guidelines/processed")
out_dir.mkdir(parents=True, exist_ok=True)


start_cue = "PERICOLI FISICI"
stop_cue =  " Può provocare sonnolenza o vertigini. "

console =Console()
def print_in_console(text):
    console.print(Panel(text))

converter = DocumentConverter()
doc = converter.convert(source=DOC_SOURCE).document

serializer = MarkdownDocSerializer(doc=doc)
ser_result = serializer.serialize()
ser_text = ser_result.text
with open(out_dir / f"{DOC_SOURCE.stem}_table.txt", "a", encoding="utf-8") as f:
    f.write(ser_text)
# print_in_console(ser_text)