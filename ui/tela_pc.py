import customtkinter as ctk
from ui.ctk_messagebox import CTkMessageBox
from PIL import Image, ImageTk
import requests
import io

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TelaPC(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.title("PC de Pokémon")
        self.attributes('-fullscreen', True)
        self.protocol("WM_DELETE_WINDOW", self.fechar)
        self.transient(master)
        self.grab_set()

        self.feedback_label = ctk.CTkLabel(self, text="Selecione um Pokémon",
            font=("Arial", 16), text_color="#EEEEEE", fg_color="#393e46", corner_radius=8)
        self.feedback_label.pack(pady=14)

        self.pc_frame = ctk.CTkFrame(self, fg_color="#222831", corner_radius=12)
        box_label = ctk.CTkLabel(self.pc_frame, text="Box: 1", font=("Arial", 17, "bold"), text_color="#00adb5")
        box_label.pack(pady=6)
        self.pc_frame.pack(padx=10, pady=4)

        ctk.CTkButton(self, text="Fechar PC", font=("Arial", 15, "bold"),
            command=self.fechar, corner_radius=14, fg_color="#ff3a5c", hover_color="#c80035").pack(pady=14)

        self.redesenhar_widgets()

    def redesenhar_widgets(self):
        for widget in self.pc_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel): continue
            widget.destroy()

        pc_list = self.controller.get_treinador_pc()
        linhas, colunas = 6, 4
        total_slots = linhas * colunas

        print(f"DEBUG colunas={colunas}, linhas={linhas}, total_slots={total_slots}")


        for i in range(total_slots):
            pokemon = pc_list[i] if i < len(pc_list) and pc_list[i] is not None else None
            slot_widget = self.criar_slot_pc_grid(self.pc_frame, pokemon, i)
            slot_widget.grid(row=i // colunas, column=i % colunas, padx=7, pady=7)


    def criar_slot_pc_grid(self, parent, pokemon, index):
        slot_frame = ctk.CTkFrame(parent, fg_color="#393e46", corner_radius=11)
        # Gerar imagem do sprite
        img = None
        if pokemon and "pokedex_id" in pokemon:
            poke_id = pokemon["pokedex_id"]
            try:
                img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{poke_id}.png"
                response = requests.get(img_url)
                pil_img = Image.open(io.BytesIO(response.content)).resize((64,64))
                img = ImageTk.PhotoImage(pil_img)
            except Exception:
                img = None
                CTkMessageBox(self, "Erro", f"Não foi possível baixar sprite de {pokemon['nome']}", icon="error")
        img_label = ctk.CTkLabel(slot_frame, text="", width=68, height=68, fg_color="#333333")
        if img:
            img_label.configure(image=img)
            img_label.image = img  # Evita garbage collector
        img_label.pack(pady=6)
        nome = pokemon["nome"] if pokemon else "- Vazio -"
        level = f" Nv.{pokemon['nivel']}" if pokemon else ""
        nome_label = ctk.CTkLabel(slot_frame, text=nome + level, font=("Arial", 11, "bold"),
                                  text_color="#F8AD19" if pokemon else "#888888")
        nome_label.pack(pady=(0,5))
        return slot_frame

    def fechar(self, event=None):
        if self.controller:
            self.controller.handle_fechar_pc()
            self.controller.pc_window = None
        self.destroy()
