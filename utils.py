import pyPDF2

def extract_text_from_pdf(file):
    reader = pyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text