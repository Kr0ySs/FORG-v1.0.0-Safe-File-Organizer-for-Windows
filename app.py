import tkinter as tk
import os
import winsound
from tkinter import ttk, filedialog, messagebox
from organizer import organize_folder, is_critical_path, set_safe_mode, get_safe_mode

def play_success_sound():
    winsound.MessageBeep(winsound.MB_ICONASTERISK)

def play_error_sound():
    winsound.MessageBeep(winsound.MB_ICONHAND)

def play_confirm_sound():
    winsound.MessageBeep(winsound.MB_ICONQUESTION)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Organizador de Arquivos")
        self.geometry("420x230")
        self.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.safe_mode_var = tk.BooleanVar(value=get_safe_mode())
        self.create_widgets()
        
    def update_safe_mode_ui(self):
        ativo = self.safe_mode_var.get()
        set_safe_mode(ativo)
        if ativo:
            self.safe_status_value.config(
                text="Ativado",
                fg="green"
            )
        else:
            self.safe_status_value.config(
                text="Desativado",
                fg="red"
            )


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

        self.status = tk.Label(self, text="", font=("Segoe UI", 9))
        self.status.pack()

        # Checkbox SAFE MODE
        self.safe_checkbox = ttk.Checkbutton(
            self,
            text="Ativar SAFE MODE (recomendado)",
            variable=self.safe_mode_var,
            command=self.update_safe_mode_ui
        )
        self.safe_checkbox.pack(pady=(0, 5))

        # Status SAFE MODE
        self.safe_status = tk.Label(
            self,
            text="SAFE MODE:",
            font=("Segoe UI", 9)
        )
        self.safe_status.pack()

        self.safe_status_value = tk.Label(
            self,
            font=("Segoe UI", 9, "bold")
        )
        self.safe_status_value.pack()

        self.update_safe_mode_ui()


    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def run(self):
        pasta = self.folder_path.get()
        
        if is_critical_path(pasta):
            self.status.config(
                text="Erro: por segurança, pastas do sistema não podem ser organizadas.",
                fg="red"
            )
            play_error_sound()
            return


        if not pasta:
            self.status.config(
                text="Erro: nenhuma pasta selecionada.",
                fg="red"
            )
            play_error_sound()
            return

        # verifica se há arquivos na pasta
        arquivos = [
            f for f in os.listdir(pasta)
            if os.path.isfile(os.path.join(pasta, f))
        ]

        if not arquivos:
            self.status.config(
                text="Erro: a pasta não contém arquivos para organizar.",
                fg="red"
            )
            play_error_sound()
            return
        if not get_safe_mode():
            self.bell()
            resposta_extra = messagebox.askyesno(
                "Atenção",
                "O SAFE MODE está DESATIVADO.\n\n"
                "Arquivos reais serão movidos.\n"
                "Deseja continuar mesmo assim?"
            )

            if not resposta_extra:
                self.status.config(
                    text="Operação cancelada: SAFE MODE desativado.",
                    fg="red"
                )
                play_error_sound()
                return

        self.bell()
        resposta = messagebox.askyesno(
            "Confirmação",
            f"A seguinte pasta será organizada:\n\n"
            f"{pasta}\n\n"
            "Essa ação irá mover arquivos dentro dessa pasta.\n"
            "Recomenda-se fazer backup antes de continuar.\n\n"
            "Deseja continuar?"
)


        if not resposta:
            self.status.config(
                text="Operação cancelada pelo usuário.",
                fg="red"
            )
            play_error_sound()
            return

        try:
            arquivos_movidos, pastas_criadas = organize_folder(pasta)

            self.status.config(
                text=f"✔ {arquivos_movidos} arquivos organizados em {pastas_criadas} pastas.",
                fg="green"
            )
            play_success_sound()

        except RuntimeError as e:
            self.status.config(
                text=str(e),
                fg="red"
            )
            play_error_sound()

        except Exception as e:
            self.status.config(
                text=f"Erro inesperado: {str(e)}",
                fg="red"
            )

if __name__ == "__main__":
    App().mainloop()