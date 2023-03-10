import pytesseract
# from PIL import Image
import PIL.Image as Image

import io
import PyPDF3


def image_to_pdf(input_file, output_file):
    # Open the image file and convert it to text using Tesseract OCR
    with Image.open(input_file) as img:
        text = pytesseract.image_to_string(img)

    # Create a new PDF file and add the text to it using PyPDF3
    pdf = PyPDF3.PdfFileWriter()
    pdf.addPage(PyPDF3.pdf.PageObject.createTextObject(text))

    # Save the PDF file
    with open(output_file, 'wb') as f:
        pdf.write(f)


image_to_pdf('receipt.jpg', 'output.pdf')
