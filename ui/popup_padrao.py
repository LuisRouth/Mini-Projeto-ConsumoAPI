import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class PopupPadrao(ctk.CTkToplevel):
    def __init__(self, master, mensagem, titulo="Aviso", tipo="info", botao="OK", on_close=None):
        super().__init__(master)
        self.title(titulo)
        self.geometry("370x180")
        self.resizable(False, False)
        self.configure(bg="#23272b")
        self.transient(master)
        self.grab_set()

        if tipo == "info":
            cor = "#2196f3"
            icon = "ℹ️"
        elif tipo == "erro":
            cor = "#c62828"
            icon = "❌"
        elif tipo == "sucesso":
            cor = "#43a047"
            icon = "✔️"
        else:
            cor = "#ffb300"
            icon = "⚠️"

        frame = ctk.CTkFrame(self, fg_color="#23272b")
        frame.pack(expand=True, fill="both", padx=14, pady=16)

        icone_label = ctk.CTkLabel(frame, text=icon, text_color=cor, font=("Arial", 44), fg_color="#23272b")
        icone_label.pack(pady=(0,0))

        texto_label = ctk.CTkLabel(frame, text=mensagem, font=("Arial", 13), text_color="white", fg_color="#23272b", wraplength=340)
        texto_label.pack(pady=14)

        botao_ok = ctk.CTkButton(frame, text=botao, font=("Arial", 14), fg_color=cor, text_color="white", hover_color="#ff5252", command=self.fechar)
        botao_ok.pack(pady=(2,4), ipadx=11)

        self.on_close = on_close

    def fechar(self):
        if self.on_close:
            self.on_close()
        self.destroy()
