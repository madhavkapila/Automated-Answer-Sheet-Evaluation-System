import fitz  # PyMuPDF
import logging
## Extracting all text from pdf from specified no. of pages
# This code is for extracting text from a PDF file using PyMuPDF (fitz).
# It opens the PDF file, iterates through the pages starting from a specified page number,
# and extracts the text from each page until the end of the document.
# The extracted text is concatenated into a single string and returned.
# The class PDFProcessor is initialized with a starting page number,
# and the extract_text method is used to perform the extraction.
# The extracted text can be used for further processing, such as keyword extraction or analysis.


class PDFProcessor:
    def __init__(self, start_page=1):
        self.start_page = start_page - 1  # 0-based index
        logging.getLogger("pdfminer").setLevel(logging.ERROR)

    def extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_num in range(self.start_page, len(doc)):
            full_text += doc[page_num].get_text()
        return full_text