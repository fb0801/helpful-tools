
#module to use
from pdf2docx import Converter

pdf_file = '' #name of file


name = input("Enter name of file: ")
    
docx_file = (f'{name}.docx')

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file)      # all pages by default
cv.close()
