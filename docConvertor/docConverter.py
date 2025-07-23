import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
from docx import Document
import os

def is_scanned_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        text = pytesseract.image_to_string(images[0])
        return len(text.strip()) > 0
    except Exception:
        return False

def convert_pdf_to_word(pdf_path, output_path):
    try:
        # Try direct conversion
        cv = Converter(pdf_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        return True
    except Exception as e:
        print("Direct conversion failed:", e)
        return False

def convert_pdf_to_word_ocr(pdf_path, output_path):
    images = convert_from_path(pdf_path)
    doc = Document()

    for img in images:
        text = pytesseract.image_to_string(img)
        doc.add_paragraph(text)

    doc.save(output_path)

def select_pdf():
    pdf_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")],
        title="Select a PDF to Convert"
    )

    if not pdf_path:
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".docx",
        filetypes=[("Word Documents", "*.docx")],
        title="Save As"
    )

    if not output_path:
        return

    try:
        status_label.config(text="Converting...")
        root.update()

        if convert_pdf_to_word(pdf_path, output_path):
            messagebox.showinfo("Success", f"PDF converted to Word:\n{output_path}")
        else:
            # Fall back to OCR if direct conversion fails
            convert_pdf_to_word_ocr(pdf_path, output_path)
            messagebox.showinfo("OCR Used", f"Scanned PDF converted with OCR:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e}")
    finally:
        status_label.config(text="")

# GUI setup
root = tk.Tk()
root.title("PDF to Word Converter with OCR")

root.geometry("400x200")
root.configure(bg="#2e2e2e")

btn = tk.Button(root, text="Select PDF", command=select_pdf, bg="#444", fg="white", font=("Arial", 14))
btn.pack(pady=30)

status_label = tk.Label(root, text="", bg="#2e2e2e", fg="white", font=("Arial", 12))
status_label.pack()

root.mainloop()
