# merge_pdfs_gui_darkmode_dragdrop.py

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PyPDF2 import PdfMerger
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import io
import os

class PDFMergerAppDragDrop:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger - Dark Mode + Drag & Drop + Preview")
        self.listbox.bind('<<ListboxSelect>>', self.show_preview)
        self.root.bind("<Button-1>", self.on_root_click)


        self.files = []

        # Dark mode colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#ffffff"
        self.button_color = "#444444"
        self.highlight_color = "#666666"

        self.root.configure(bg=self.bg_color)

        frame = tk.Frame(root, bg=self.bg_color)
        frame.pack(padx=10, pady=10, side='left')

        self.select_button = tk.Button(frame, text="Select PDFs", command=self.select_pdfs,
                                       bg=self.button_color, fg=self.fg_color)
        self.select_button.pack(fill='x')

        self.listbox = tk.Listbox(frame, width=50, selectmode=tk.SINGLE, bg=self.bg_color, fg=self.fg_color,
                                  selectbackground=self.highlight_color, selectforeground=self.fg_color)
        self.listbox.pack(pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.show_preview)

        # Enable drag and drop
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.drop_files)

        self.up_button = tk.Button(frame, text="Move Up", command=self.move_up,
                                   bg=self.button_color, fg=self.fg_color)
        self.up_button.pack(fill='x', pady=(5, 0))

        self.down_button = tk.Button(frame, text="Move Down", command=self.move_down,
                                     bg=self.button_color, fg=self.fg_color)
        self.down_button.pack(fill='x')

        self.merge_button = tk.Button(frame, text="Merge and Save", command=self.save_pdf,
                                      bg=self.button_color, fg=self.fg_color)
        self.merge_button.pack(fill='x', pady=(10, 0))

        # Preview area
        preview_frame = tk.Frame(root, bg=self.bg_color)
        preview_frame.pack(padx=10, pady=10, side='right')
        self.preview_label = tk.Label(preview_frame, bg=self.bg_color)
        self.preview_label.pack()

    def select_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if files:
            self.files = list(files)
            self.refresh_listbox()

    def drop_files(self, event):
        dropped_files = self.root.tk.splitlist(event.data)
        for file in dropped_files:
            if file.lower().endswith('.pdf') and file not in self.files:
                self.files.append(file)
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

    def show_preview(self, event):
        selection = self.listbox.curselection()
        if not selection:
            # No selection, clear the preview
            self.preview_label.config(image='')
            return

        index = selection[0]
        filepath = self.files[index]
        try:
            doc = fitz.open(filepath)
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail((400, 400))
            self.preview_img = ImageTk.PhotoImage(img)
            self.preview_label.config(image=self.preview_img)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot preview PDF:\n{e}")

    def on_root_click(self, event):
        widget = event.widget
        # If they clicked *outside* the listbox, clear the preview
        if widget != self.listbox:
            self.listbox.selection_clear(0, tk.END)  # Clear any selection in the list
            self.preview_label.config(image='')  # Clear the preview

    def on_root_click(self, event):
        widget = event.widget
        # If they clicked *outside* the listbox, clear the preview
        if widget != self.listbox:
            self.listbox.selection_clear(0, tk.END)  # Clear any selection in the list
            self.preview_label.config(image='')  # Clear the preview


if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD instead of tk.Tk()
    app = PDFMergerAppDragDrop(root)
    root.mainloop()
