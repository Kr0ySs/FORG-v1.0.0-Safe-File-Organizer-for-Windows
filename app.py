import tkinter as tk
import os
import winsound
from tkinter import ttk, filedialog, messagebox

from organizer import (
    organize_folder,
    is_critical_path,
    set_safe_mode,
    get_safe_mode,
)
from i18n import load_language, t


# ================== SONS ==================


def play_success_sound():
    winsound.MessageBeep(winsound.MB_ICONASTERISK)


def play_error_sound():
    winsound.MessageBeep(winsound.MB_ICONHAND)


def play_confirm_sound():
    winsound.MessageBeep(winsound.MB_ICONQUESTION)


# ================== APP ==================


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        load_language("pt_BR")

        self.language_var = tk.StringVar(value="pt_BR")

        self.title(t("title"))
        self.geometry("420x260")
        self.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.safe_mode_var = tk.BooleanVar(value=get_safe_mode())

        self.create_widgets()
        self.update_safe_mode_ui()

    # -------- LANGUAGE SELECTOR ----------

    def change_language(self, event=None):
        lang = self.language_var.get()
        load_language(lang)

        for widget in self.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.update_safe_mode_ui()


    # ---------- SAFE MODE ----------

    def update_safe_mode_ui(self):
        ativo = self.safe_mode_var.get()
        set_safe_mode(ativo)

        if ativo:
            self.safe_status_value.config(
                text=t("safe_enabled"),
                fg="green",
            )
        else:
            self.safe_status_value.config(
                text=t("safe_disabled"),
                fg="red",
            )

    # ---------- UI ----------

    def create_widgets(self):
        pad = {"padx": 10, "pady": 6}

        # -------- LANGUAGE SELECT --------
        lang_frame = ttk.Frame(self)
        lang_frame.pack(pady=(5, 0))

        ttk.Label(lang_frame, text=t("language")).pack(side="left", padx=(0, 5))

        self.language_select = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            state="readonly",
            width=10,
            values=["pt_BR", "en_US"],
        )
        self.language_select.pack(side="left")
        self.language_select.bind("<<ComboboxSelected>>", self.change_language)


        ttk.Label(self, text=t("select_folder")).pack(**pad)

        frame = ttk.Frame(self)
        frame.pack(fill="x", **pad)

        ttk.Entry(frame, textvariable=self.folder_path).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            frame,
            text=t("browse"),
            command=self.select_folder,
        ).pack(side="left", padx=5)

        ttk.Button(
            self,
            text=t("organize"),
            command=self.run,
        ).pack(pady=15)

        self.status = tk.Label(self, text="", font=("Segoe UI", 9))
        self.status.pack()

        self.safe_checkbox = ttk.Checkbutton(
            self,
            text=t("safe_checkbox"),
            variable=self.safe_mode_var,
            command=self.update_safe_mode_ui,
        )
        self.safe_checkbox.pack(pady=(10, 5))

        self.safe_status = tk.Label(self, text=t("safe_label"))
        self.safe_status.pack()

        self.safe_status_value = tk.Label(
            self,
            font=("Segoe UI", 9, "bold"),
        )
        self.safe_status_value.pack()

    # ---------- ACTIONS ----------

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_path.set(path)

    def run(self):
        pasta = self.folder_path.get()

        if not pasta:
            self.status.config(text=t("error_no_folder"), fg="red")
            play_error_sound()
            return

        if is_critical_path(pasta):
            self.status.config(text=t("error_critical_path"), fg="red")
            play_error_sound()
            return

        arquivos = [
            f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))
        ]

        if not arquivos:
            self.status.config(text=t("error_no_files"), fg="red")
            play_error_sound()
            return

        if not get_safe_mode():
            play_confirm_sound()
            resposta_extra = messagebox.askyesno(
                t("warning"),
                t("safe_disabled_warning"),
            )

            if not resposta_extra:
                self.status.config(text=t("operation_cancelled"), fg="red")
                play_error_sound()
                return

        play_confirm_sound()
        resposta = messagebox.askyesno(
            t("confirmation"),
            t("confirm_action", folder=pasta),
        )

        if not resposta:
            self.status.config(text=t("operation_cancelled"), fg="red")
            play_error_sound()
            return

        try:
            arquivos_movidos, pastas_criadas = organize_folder(pasta)

            self.status.config(
                text=t(
                    "success_message",
                    files=arquivos_movidos,
                    folders=pastas_criadas,
                ),
                fg="green",
            )
            play_success_sound()

        except RuntimeError:
            self.status.config(text=t("safe_mode_active"), fg="orange")
            play_error_sound()

        except Exception as e:
            self.status.config(
                text=t("unexpected_error", error=str(e)),
                fg="red",
            )
            play_error_sound()


# ================== START ==================

if __name__ == "__main__":
    app = App()
    app.mainloop()
