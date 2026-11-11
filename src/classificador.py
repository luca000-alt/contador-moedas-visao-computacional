"""Classificação de moedas (seção 4.2 da documentação)."""
import math

import cv2
import numpy as np

from . import config

DESCONHECIDO = None


def circularidade(contorno):
    area = cv2.contourArea(contorno)
    perimetro = cv2.arcLength(contorno, True)
    if perimetro == 0:
        return 0.0
    return 4 * math.pi * area / perimetro ** 2


def diametro_mm(contorno, px_por_mm):
    """Diâmetro equivalente: 2 * raiz(área / pi), convertido para mm."""
    area = cv2.contourArea(contorno)
    return (2 * math.sqrt(area / math.pi)) / px_por_mm


def saturacao_media(contorno, imagem):
    """Saturação média (HSV) do miolo da moeda."""
    mascara = np.zeros(imagem.shape[:2], np.uint8)
    cv2.drawContours(mascara, [contorno], -1, 255, -1)
    mascara = cv2.erode(mascara, np.ones((9, 9), np.uint8))
    hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)
    return float(cv2.mean(hsv, mask=mascara)[1])


def grupo_de_cor(saturacao):
    return "prata" if saturacao < config.SATURACAO_PRATA else "bronze"


def moeda_mais_proxima(d_mm, saturacao):
    """Escolhe a moeda de menor erro de diâmetro, compatível com a cor."""
    grupo = grupo_de_cor(saturacao)
    melhor, menor_erro = DESCONHECIDO, config.TOLERANCIA_MM
    for valor, (diam, grupo_ref) in config.MOEDAS.items():
        if grupo_ref != "bimetalica" and grupo_ref != grupo:
            continue
        erro = abs(d_mm - diam)
        if erro <= menor_erro:
            melhor, menor_erro = valor, erro
    return melhor


def classificar(contorno, imagem, px_por_mm):
    """Retorna o valor da moeda ou None (desconhecido => ignorado)."""
    if circularidade(contorno) <= config.CIRCULARIDADE_MIN:
        return DESCONHECIDO
    d = diametro_mm(contorno, px_por_mm)
    return moeda_mais_proxima(d, saturacao_media(contorno, imagem))
