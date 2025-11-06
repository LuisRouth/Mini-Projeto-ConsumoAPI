TYPE_CHART = {
    "Normal":   {"Pedra": 0.5, "Fantasma": 0.2, "Aço": 0.5},
    "Lutador":  {"Normal": 2, "Voador": 0.5, "Venenoso": 0.5, "Pedra": 2, "Inseto": 0.5, "Fantasma": 0.2, "Aço": 2, "Psíquico": 0.5, "Gelo": 2, "Sombrio": 2, "Fada": 0.5},
    "Voador":   {"Lutador": 2, "Pedra": 0.5, "Inseto": 2, "Aço": 0.5, "Grama": 2, "Elétrico": 0.5},
    "Venenoso": {"Venenoso": 0.5, "Terrestre": 0.5, "Pedra": 0.5, "Fantasma": 0.5, "Aço": 0.2, "Grama": 2, "Fada": 2},
    "Terrestre":{"Voador": 0.2, "Venenoso": 2, "Pedra": 2, "Inseto": 0.5, "Aço": 2, "Fogo": 2, "Grama": 0.5, "Elétrico": 2},
    "Pedra":    {"Lutador": 0.5, "Voador": 2, "Terrestre": 0.5, "Inseto": 2, "Aço": 0.5, "Fogo": 2, "Gelo": 2},
    "Inseto":   {"Lutador": 0.5, "Voador": 0.5, "Venenoso": 0.5, "Fantasma": 0.5, "Aço": 0.5, "Fogo": 0.5, "Grama": 2, "Psíquico": 2, "Sombrio": 2, "Fada": 0.5},
    "Fantasma": {"Normal": 0.2, "Fantasma": 2, "Psíquico": 2, "Sombrio": 0.5},
    "Aço":      {"Pedra": 2, "Aço": 0.5, "Fogo": 0.5, "Água": 0.5, "Elétrico": 0.5, "Gelo": 2, "Fada": 2},
    "Fogo":     {"Pedra": 0.5, "Inseto": 2, "Aço": 2, "Fogo": 0.5, "Água": 0.5, "Grama": 2, "Gelo": 2, "Dragão": 0.5},
    "Água":     {"Terrestre": 2, "Pedra": 2, "Fogo": 2, "Água": 0.5, "Grama": 0.5, "Dragão": 0.5},
    "Grama":   {"Voador": 0.5, "Venenoso": 0.5, "Terrestre": 2, "Pedra": 2, "Inseto": 0.5, "Aço": 0.5, "Fogo": 0.5, "Água": 2, "Grama": 0.5, "Dragão": 0.5},
    "Elétrico": {"Voador": 2, "Terrestre": 0.2, "Água": 2, "Grama": 0.5, "Elétrico": 0.5, "Dragão": 0.5},
    "Psíquico": {"Lutador": 2, "Venenoso": 2, "Aço": 0.5, "Psíquico": 0.5, "Sombrio": 0.2},
    "Gelo":     {"Voador": 2, "Terrestre": 2, "Aço": 0.5, "Fogo": 0.5, "Água": 0.5, "Grama": 2, "Gelo": 0.5, "Dragão": 2},
    "Dragão":   {"Aço": 0.5, "Dragão": 2, "Fada": 0.2},
    "Sombrio":  {"Lutador": 0.5, "Fantasma": 2, "Psíquico": 2, "Sombrio": 0.5, "Fada": 0.5},
    "Fada":     {"Lutador": 2, "Venenoso": 0.5, "Aço": 0.5, "Fogo": 0.5, "Dragão": 2, "Sombrio": 2}
}
def calcular_multiplicador(tipo_ataque: str, tipos_defesa: list[str]) -> float:
    """
    Calcula o multiplicador de dano total com base no tipo do ataque
    e nos tipos do Pokémon defensor (considerando dual-types).
    """
    multiplicador_total = 1.0
    
    # Se o tipo do atacante não tiver interações especiais, retorna 1.0
    if tipo_ataque not in TYPE_CHART:
        return multiplicador_total

    # Itera sobre cada tipo do Pokémon defensor
    for tipo_defesa in tipos_defesa:
        multiplicador_parcial = TYPE_CHART[tipo_ataque].get(tipo_defesa, 1.0)
        multiplicador_total *= multiplicador_parcial

    return multiplicador_total