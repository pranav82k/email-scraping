# To extract information from PDFs and images, you can use third-party libraries like PyPDF3 and Pillow.
# Here's an example of how to extract text from a PDF using PyPDF3:

import PyPDF3


def extract_pdf_text(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF3.PdfFileReader(f)
        # print(pdf_reader.getNumPages())
        text = ""
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            # print(page)
            text += page.extractText()
        return text


text = extract_pdf_text('sample.pdf')
print(text)
