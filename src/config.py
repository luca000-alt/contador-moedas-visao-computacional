"""Parâmetros do sistema (ajuste aqui conforme os testes)."""

# valor (R$) -> (diâmetro em mm, grupo de cor)
# grupos: "bronze", "prata", "bimetalica" (1,00: cor ignorada)
MOEDAS = {
    0.05: (22.0, "bronze"),
    0.10: (20.0, "bronze"),
    0.25: (25.0, "bronze"),
    0.50: (23.0, "prata"),
    1.00: (27.0, "bimetalica"),
}

DIAMETRO_REFERENCIA_MM = 27.0   # moeda de R$ 1,00 usada na calibração
TOLERANCIA_MM = 1.0             # erro máximo aceito no diâmetro
CIRCULARIDADE_MIN = 0.80        # abaixo disso o objeto não é moeda
AREA_MIN_FRACAO = 0.0005        # área mínima = fração da área do quadro
SATURACAO_PRATA = 70            # S (HSV) média abaixo disso => prata
LARGURA_PADRAO = 960            # todo quadro é redimensionado p/ essa largura
