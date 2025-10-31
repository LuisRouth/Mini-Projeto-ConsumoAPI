from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import crud
from .routers import treinador, mundo, batalha

app = FastAPI(
    title="API Pokémon",
    description="Uma API para simular a captura e gerenciamento de Pokémon.",
    version="0.1.0"
)

# --- Configuração do CORS ---
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Roteadores e Endpoints ---
app.include_router(treinador.router)
app.include_router(mundo.router)
app.include_router(batalha.router)

@app.get("/", tags=["Status"])
def ler_raiz():
    return {"status": "API Pokémon está no ar!"}

@app.get("/pokedex", tags=["Pokedex"])
def get_pokedex_completo():
    return crud.get_pokedex()

@app.get("/gamestate", tags=["Status"])
def get_gamestate_completo():
    return crud.get_gamestate()

@app.get("/pokedex/iniciais", tags=["Pokedex"])
def get_iniciais():
    return crud.get_iniciais_from_pokedex()