import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from organizer import organize_folder

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Organizador de Arquivos")
        self.geometry("420x230")
        self.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        pad = {"padx": 10, "pady": 6}

        ttk.Label(self, text="Selecione a pasta").pack(**pad)

        frame = ttk.Frame(self)
        frame.pack(fill="x", **pad)

        ttk.Entry(frame, textvariable=self.folder_path).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(frame, text="Procurar", command=self.select_folder).pack(
            side="left", padx=5
        )

        ttk.Button(self, text="ORGANIZAR", command=self.run).pack(pady=20)

        self.status = ttk.Label(self, text="")
        self.status.pack()

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def run(self):
        if not self.folder_path.get():
            messagebox.showwarning("Atenção", "Selecione uma pasta.")
            return

        try:
            organize_folder(self.folder_path.get())
            self.status.config(text="✔ Arquivos organizados com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    App().mainloop()