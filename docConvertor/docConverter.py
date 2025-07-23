import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
import subprocess
import os
import tempfile
import shutil

def ocr_pdf(input_pdf, output_pdf):
    try:
        subprocess.run(['ocrmypdf', '--force-ocr', input_pdf, output_pdf], check=True)
        return True
    except Exception as e:
        print("OCR failed:", e)
        return False

def convert_pdf_to_word(pdf_path, output_path):
    cv = Converter(pdf_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()

def is_scanned_pdf(pdf_path):
    try:
        from pdf2image import convert_from_path
        from pytesseract import image_to_string
        images = convert_from_path(pdf_path, first_page=1, last_page=1)
        text = image_to_string(images[0])
        return len(text.strip()) == 0  # empty text means scanned
    except:
        return False

def process_file():
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
            temp_pdf = tempfile.mktemp(suffix=".pdf")
            success = ocr_pdf(pdf_path, temp_pdf)
            if not success:
                raise Exception("OCR failed.")
            convert_pdf_to_word(temp_pdf, output_path)
            os.remove(temp_pdf)
            messagebox.showinfo("Success", "Scanned PDF converted with OCR!")
        else:
            convert_pdf_to_word(pdf_path, output_path)
            messagebox.showinfo("Success", "PDF converted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert:\n{e}")
    finally:
        status_label.config(text="")

# GUI
root = tk.Tk()
root.title("PDF to Word Converter (with OCR)")
root.geometry("420x200")
root.configure(bg="#2d2d2d")

btn = tk.Button(root, text="Select PDF", command=process_file, font=("Arial", 14), bg="#444", fg="white")
btn.pack(pady=30)

status_label = tk.Label(root, text="", bg="#2d2d2d", fg="white", font=("Arial", 11))
status_label.pack()

root.mainloop()
