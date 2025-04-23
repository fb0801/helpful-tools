# merge_pdfs_gui.py

import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

def merge_pdfs(file_paths, output_path):
    merger = PdfMerger()
    for pdf in file_paths:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def select_pdfs():
    files = filedialog.askopenfilenames(
        title="Select PDF files to merge",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if files:
        pdf_listbox.delete(0, tk.END)
        for f in files:
            pdf_listbox.insert(tk.END, f)
        global selected_files
        selected_files = files

def save_pdf():
    if not selected_files:
        messagebox.showerror("Error", "No PDFs selected to merge.")
        return
    output_file = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save merged PDF as"
    )
    if output_file:
        try:
            merge_pdfs(selected_files, output_file)
            messagebox.showinfo("Success", f"Merged PDF saved as:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Initialize GUI
app = tk.Tk()
app.title("PDF Merger")

selected_files = []

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="Select PDFs", command=select_pdfs)
select_button.pack(fill='x')

pdf_listbox = tk.Listbox(frame, width=80)
pdf_listbox.pack(pady=5)

merge_button = tk.Button(frame, text="Merge and Save", command=save_pdf)
merge_button.pack(fill='x', pady=(5,0))

app.mainloop()
