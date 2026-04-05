import pdfplumber
with pdfplumber.open('data/raw/IJCBS_04_01_003.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"Page {i+1} has {len(page.images)} images")
