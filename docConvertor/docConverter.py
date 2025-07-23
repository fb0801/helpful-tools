import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import subprocess
import tempfile
import os

def ocr_pdf(input_pdf, output_pdf):
    """Runs OCR on scanned PDFs using ocrmypdf."""
    try:
        subprocess.run(['ocrmypdf', '--force-ocr', '--skip-text', input_pdf, output_pdf], check=True)
        return True
    except Exception as e:
        print("OCR failed:", e)
        return False

def convert_pdf_to_word(pdf_path, output_path):
    """Converts PDF to Word while preserving layout and page count."""
    cv = Converter(pdf_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()

def is_scanned_pdf(pdf_path):
    """Detects if a PDF is scanned by trying to extract text from the first page."""
    try:
        from pdf2image import convert_from_path
        from pytesseract import image_to_string
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        text = image_to_string(images[0])
        return len(text.strip()) < 5
    except Exception as e:
        print("Scan check failed:", e)
        return False

def process_file():
    """Handles file selection, OCR detection, conversion, and output."""
    pdf_path = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")], title="Select PDF"
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

    status_label.config(text="Processing...")
    root.update()

    try:
        if is_scanned_pdf(pdf_path):
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                if not ocr_pdf(pdf_path, temp_pdf.name):
                    raise Exception("OCR failed.")
                convert_pdf_to_word(temp_pdf.name, output_path)
                os.remove(temp_pdf.name)
            messagebox.showinfo("Success", "Scanned PDF converted with OCR!")
        else:
            convert_pdf_to_word(pdf_path, output_path)
            messagebox.showinfo("Success", "PDF converted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert:\n{e}")
    finally:
        status_label.config(text="")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("PDF to Word Converter (with OCR)")
root.geometry("440x200")
root.configure(bg="#2b2b2b")

tk.Button(
    root,
    text="Select PDF",
    command=process_file,
    font=("Segoe UI", 14),
    bg="#444",
    fg="white"
).pack(pady=30)

status_label = tk.Label(
    root,
    text="",
    bg="#2b2b2b",
    fg="white",
    font=("Segoe UI", 11)
)
status_label.pack()

root.mainloop()
