import customtkinter as ctk

class CTkMessageBox(ctk.CTkToplevel):
    def __init__(self, master, title, message, icon="info"):
        super().__init__(master)
        self.title(title)
        self.geometry("360x160")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        cor = {"info": "#2196F3", "warning": "#F8AD19", "error": "#F44336"}
        txt_cor = {"info": "#ffffff", "warning": "#393e46", "error": "#ffffff"}
        color = cor.get(icon, "#2196F3")
        text_color = txt_cor.get(icon, "#ffffff")
        ctk.CTkLabel(self, text=title, font=("Arial", 16, "bold"), text_color=color).pack(anchor="w", padx=18, pady=(15,0))
        ctk.CTkLabel(self, text=message, font=("Arial", 13), text_color=text_color, wraplength=320).pack(anchor="center", pady=12, padx=20)
        ctk.CTkButton(self, text="OK", command=self.destroy, fg_color=color, text_color=text_color).pack(pady=(6,18))
        self.grab_set()
        self.transient(master)
