"""Testes com imagens sintéticas (escala fixa de 5 px/mm)."""
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calibracao import calibrar_com_moeda_de_referencia
from src.contador import contar

ESCALA = 5.0
BRONZE, PRATA = (60, 120, 190), (190, 190, 190)


def cena(moedas):
    """moedas: lista de (diâmetro_mm, cor, (x, y))."""
    img = np.full((600, 960, 3), (40, 40, 40), np.uint8)
    for d, cor, centro in moedas:
        cv2.circle(img, centro, int(d * ESCALA / 2), cor, -1)
    return img


def test_soma_mista():
    img = cena([(22, BRONZE, (120, 120)), (20, BRONZE, (300, 120)),
                (25, BRONZE, (480, 120)), (23, PRATA, (660, 120)),
                (27, (80, 170, 200), (840, 120))])
    total, contagem, _ = contar(img, ESCALA)
    assert total == 1.90 and sum(contagem.values()) == 5


def test_ignora_objeto_nao_circular():
    img = cena([(25, BRONZE, (200, 200))])
    cv2.rectangle(img, (500, 100), (700, 160), (200, 200, 200), -1)
    total, _, _ = contar(img, ESCALA)
    assert total == 0.25


def test_ignora_diametro_fora_da_tabela():
    total, _, _ = contar(cena([(35, BRONZE, (300, 300))]), ESCALA)
    assert total == 0.0


def test_calibracao():
    escala = calibrar_com_moeda_de_referencia(cena([(27, PRATA, (400, 300))]))
    assert abs(escala - ESCALA) < 0.1


if __name__ == "__main__":
    for nome, fn in list(globals().items()):
        if nome.startswith("test_"):
            fn(); print("OK", nome)
