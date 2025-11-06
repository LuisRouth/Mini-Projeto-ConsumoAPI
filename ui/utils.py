# MINI-.../ui/utils.py

import os
import requests
import io
from PIL import Image
import customtkinter as ctk
import shutil

DIRETORIO_CACHE = os.path.join(os.path.dirname(__file__), 'image_cache')
os.makedirs(DIRETORIO_CACHE, exist_ok=True)
# ------------------------------


def carregar_imagem_pokemon(nome_pokemon, tamanho=(160, 100)):
    nome_formatado = nome_pokemon.lower()
    caminho_arquivo_cache = os.path.join(DIRETORIO_CACHE, f"{nome_formatado}.png")
    if os.path.exists(caminho_arquivo_cache):
        try:
            imagem_pil = Image.open(caminho_arquivo_cache)
            return ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=tamanho)
        except Exception as e:
            print(f"Erro ao carregar imagem do cache '{caminho_arquivo_cache}': {e}")
    url = f"https://img.pokemondb.net/artwork/large/{nome_formatado}.jpg"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        dados_da_imagem = io.BytesIO(response.content)
        imagem_pil = Image.open(dados_da_imagem)
        imagem_pil.resize(tamanho, Image.Resampling.LANCZOS)
        imagem_pil.save(caminho_arquivo_cache, "PNG")
        
        return ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=tamanho)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar a imagem do Pokémon '{nome_pokemon}' da web: {e}")
        return None
    
def limpar_cache_imagens():
    if os.path.exists(DIRETORIO_CACHE):
        try:
            shutil.rmtree(DIRETORIO_CACHE)
            os.makedirs(DIRETORIO_CACHE, exist_ok=True)
            print("Cache de imagens limpo com sucesso!")
            return True
        except Exception as e:
            print(f"Erro ao tentar limpar o cache: {e}")
            return False
    else:
        print("Pasta de cache não encontrada. Nada a fazer.")
        return False