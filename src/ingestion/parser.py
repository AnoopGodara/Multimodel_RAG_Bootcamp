import pdfplumber
import os
from src.models.gemini_client import GeminiClient
from src.utils.resource_manager import ResourceManager
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    def __init__(self):
        self.gemini = GeminiClient()

    def parse_page(self, pdf, page, page_num, file_name):
        chunks = []
        img_dir = 'data/preprocessed/images'
        os.makedirs(img_dir, exist_ok=True)

        # Text Extraction
        text = page.extract_text()
        if text:
            chunks.append({
                "content": f"Text from {file_name} (Page {page_num}): {text}",
                "metadata": {"source": file_name, "page": page_num, "type": "text"}
            })

        # Table Extraction
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            table_str = "\\n".join([" | ".join([str(cell or "") for cell in row]) for row in table])
            table_summary = self.gemini.summarize_table(table_str)
            chunks.append({
                "content": f"Table from {file_name} (Page {page_num}, Table {j+1}): {table_summary}",
                "metadata": {"source": file_name, "page": page_num, "type": "table"}
            })

        # Image Extraction
        if page.images:
            img_path = f"{img_dir}/{file_name}_page_{page_num}.png"
            page.to_image(resolution=150).save(img_path)
            img_summary = self.gemini.summarize_image(img_path)
            chunks.append({
                "content": f"Image/Diagram from {file_name} (Page {page_num}): {img_summary}",
                "metadata": {"source": file_name, "page": page_num, "type": "image"}
            })
        return chunks

    def parse(self, file_path: str):
        all_chunks = []
        file_name = os.path.basename(file_path)
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                all_chunks.extend(self.parse_page(pdf, page, i+1, file_name))
        return all_chunks
