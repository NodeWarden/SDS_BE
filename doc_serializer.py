#file temporaneo per test & gestione di file singoli per casi isolati

from pathlib import Path

DOC_SOURCE = Path("./guidelines/INALATORIA.pdf")
out_dir = Path("./guidelines/processed")
out_dir.mkdir(parents=True, exist_ok=True)

# ===========================SERIALIZER=========================================
from rich.panel import Panel
from rich.console import Console
from docling.document_converter import DocumentConverter
from docling_core.transforms.serializer.markdown import MarkdownDocSerializer

start_cue = "FATTORE DI GRAVITÀ (M)"
stop_cue =  " Può provocare sonnolenza o vertigini. "

console =Console()
def print_in_console(text):
    console.print(Panel(text))

converter = DocumentConverter()
doc = converter.convert(source=DOC_SOURCE).document

serializer = MarkdownDocSerializer(doc=doc)
ser_result = serializer.serialize()
ser_text = ser_result.text
with open(out_dir / f"{DOC_SOURCE.stem}.txt", "w", encoding="utf-8") as f:
    f.write(ser_text[ser_text.find(start_cue) :])
print_in_console(ser_text)




#===========================TABLE_CONVERTER_HYBRID====================================
# import pandas as pd 
# from docling.document_converter import DocumentConverter
# from docling.chunking import HybridChunker
# converter = DocumentConverter()
# conv_res = converter.convert(DOC_SOURCE)
# doc_filename = conv_res.input.file.stem

# for table_ix, table in enumerate(conv_res.document.tables):
#     table_df : pd.DataFrame = table.export_to_dataframe()
#     print(f"## Table {table_ix}")
#     print(table.export_to_markdown())
#     with open(out_dir / f"{DOC_SOURCE.stem}_conv.txt", "w", encoding="utf-8") as f:
#         f.write(table_df.to_markdown())




#=============================AUTO OCR DETECTION======================================
# from docling.datamodel.base_models import InputFormat
# from docling.datamodel.pipeline_options import (PdfPipelineOptions, TesseractCliOcrOptions)
# from docling.document_converter import DocumentConverter, PdfFormatOption
# def main():
#     ocr_options = TesseractCliOcrOptions(lang=["auto"])
#     pipeline_options = PdfPipelineOptions(
#         do_ocr=True, force_full_page_ocr=True, ocr_options=ocr_options
#     )

#     converter = DocumentConverter(
#         format_options = {
#             InputFormat.PDF: PdfFormatOption(
#                 pipeline_options=pipeline_options,
#             )
#         }
#     )

#     doc = converter.convert(DOC_SOURCE).document
#     md = doc.export_to_markdown()
#     print(md)
#     with open(out_dir / f"{DOC_SOURCE.stem}_ocr.md", "w", encoding="utf-8") as f:
#         f.write(md)


#==================================SIMPLE MARKDOWN=====================================
# from docling.document_converter import DocumentConverter

# converter = DocumentConverter()
# doc = converter.convert(DOC_SOURCE).document
# with open(out_dir / f"{DOC_SOURCE.stem}_simple.txt", "w", encoding="utf-8") as f:
#     f.write(doc.export_to_markdown())



#================================SMOL DOCLING================================
# import torch
# from transformers import AutoProcessor,AutoModelForVision2Seq

# device = "cuda" if torch.cuda.is_available() else "cpu"

# processor = AutoProcessor.from_pretrained("ds4sd/SmolDocling-256M-preview")
# model = AutoModelForVision2Seq.from_pretrained(
#     "ds4sd/SmolDocling-256M-preview",
#     torch_dtype = torch.bfloat16,
#     _attn_implementation = "flash_attention_2" if device == "cuda" else "eager",
#     ).to(device)