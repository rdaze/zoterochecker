import tkinter as tk
from tkinter import filedialog, messagebox
from logic import run_check  # your core logic

def run_gui():
    def select_bib():
        path = filedialog.askopenfilename(filetypes=[("BibTeX files", "*.bib")])
        if path:
            bib_path.set(path)

    def select_txt():
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            txt_path.set(path)

    def run_checker_click():
        bpath = bib_path.get()
        tpath = txt_path.get()
        if not bpath or not tpath:
            messagebox.showerror("Missing Input", "Please select both files.")
            return

        try:
            run_check(bpath, tpath)
            messagebox.showinfo("Done", "Check the terminal and zotero_check_result.txt.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    root = tk.Tk()
    root.title("Zotero Checker")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    bib_path = tk.StringVar()
    txt_path = tk.StringVar()

    tk.Label(frame, text="Zotero BibTeX File:").grid(row=0, column=0, sticky="w")
    tk.Entry(frame, textvariable=bib_path, width=50).grid(row=0, column=1)
    tk.Button(frame, text="Browse", command=select_bib).grid(row=0, column=2)

    tk.Label(frame, text="Link List (.txt):").grid(row=1, column=0, sticky="w", pady=(10, 0))
    tk.Entry(frame, textvariable=txt_path, width=50).grid(row=1, column=1, pady=(10, 0))
    tk.Button(frame, text="Browse", command=select_txt).grid(row=1, column=2, pady=(10, 0))

    tk.Button(frame, text="Run Checker", command=run_checker_click, width=20).grid(row=2, column=0, columnspan=3, pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
