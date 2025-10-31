from pydantic import BaseModel

class TreinadorCreate(BaseModel):
    nome: str

class EscolhaAcao(BaseModel):
    pokemon_nome: str

class AcaoBatalha(BaseModel):
    tipo: str

class BatalhaInfo(BaseModel):
    treinador_id: int
    pokemon_nome: str