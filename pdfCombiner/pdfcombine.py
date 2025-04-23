# merge_pdfs_gui_advanced.py

import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced PDF Merger")
        
        self.files = []

        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)

        self.select_button = tk.Button(frame, text="Select PDFs", command=self.select_pdfs)
        self.select_button.pack(fill='x')

        self.listbox = tk.Listbox(frame, width=80, selectmode=tk.SINGLE)
        self.listbox.pack(pady=5)

        self.up_button = tk.Button(frame, text="Move Up", command=self.move_up)
        self.up_button.pack(fill='x', pady=(5,0))

        self.down_button = tk.Button(frame, text="Move Down", command=self.move_down)
        self.down_button.pack(fill='x')

        self.merge_button = tk.Button(frame, text="Merge and Save", command=self.save_pdf)
        self.merge_button.pack(fill='x', pady=(10,0))

    def select_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if files:
            self.files = list(files)
            self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for f in self.files:
            self.listbox.insert(tk.END, f)

    def move_up(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == 0:
            return
        index = selected[0]
        self.files[index - 1], self.files[index] = self.files[index], self.files[index - 1]
        self.refresh_listbox()
        self.listbox.selection_set(index - 1)

    def move_down(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == len(self.files) - 1:
            return
        index = selected[0]
        self.files[index + 1], self.files[index] = self.files[index], self.files[index + 1]
        self.refresh_listbox()
        self.listbox.selection_set(index + 1)

    def save_pdf(self):
        if not self.files:
            messagebox.showerror("Error", "No PDFs selected to merge.")
            return
        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save merged PDF as"
        )
        if output_file:
            try:
                merger = PdfMerger()
                for pdf in self.files:
                    merger.append(pdf)
                merger.write(output_file)
                merger.close()
                messagebox.showinfo("Success", f"Merged PDF saved as:\n{output_file}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
