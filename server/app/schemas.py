from pydantic import BaseModel

class TreinadorCreate(BaseModel):
    nome: str

class EscolhaAcao(BaseModel):
    pokemon_nome: str

class AcaoBatalha(BaseModel):
    tipo: str

class AcaoTroca(BaseModel):
    id_captura_para_troca: int

class BatalhaInfo(BaseModel):
    treinador_id: int
    pokemon_nome: str
    nivel_encontrado: int
    area_id: str