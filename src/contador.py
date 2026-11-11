"""Soma dos valores e anotação da imagem (seção 4.4 da documentação)."""
from collections import Counter

import cv2

from .classificador import classificar
from .processamento import segmentar


def contar(imagem, px_por_mm):
    """Retorna (total, contagem_por_valor, lista de (contorno, valor))."""
    total, contagem, itens = 0.0, Counter(), []
    for contorno in segmentar(imagem):
        valor = classificar(contorno, imagem, px_por_mm)
        if valor is not None:
            total += valor
            contagem[valor] += 1
            itens.append((contorno, valor))
    return round(total, 2), contagem, itens


def anotar(imagem, total, contagem, itens):
    saida = imagem.copy()
    for contorno, valor in itens:
        x, y, w, h = cv2.boundingRect(contorno)
        cv2.rectangle(saida, (x, y), (x + w, y + h), (0, 200, 0), 2)
        cv2.putText(saida, f"R$ {valor:.2f}", (x, max(y - 6, 15)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 0), 2)
    qtd = sum(contagem.values())
    cv2.rectangle(saida, (0, 0), (330, 62), (0, 0, 0), -1)
    cv2.putText(saida, f"Moedas: {qtd}", (10, 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(saida, f"Total: R$ {total:.2f}", (10, 52),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    return saida
