"""Pré-processamento e segmentação (seções 3 e 4.1 da documentação)."""
import cv2
import numpy as np

from . import config


def padronizar(imagem):
    """Redimensiona para largura fixa, mantendo a proporção."""
    h, w = imagem.shape[:2]
    escala = config.LARGURA_PADRAO / w
    return cv2.resize(imagem, (config.LARGURA_PADRAO, int(h * escala)))


def segmentar(imagem):
    """Retorna os contornos externos dos objetos candidatos."""
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    suave = cv2.GaussianBlur(cinza, (5, 5), 0)
    melhor = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(suave)
    _, binaria = cv2.threshold(melhor, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Garante objeto = branco: se as bordas (fundo) ficaram brancas, inverte.
    borda = np.concatenate([binaria[0], binaria[-1], binaria[:, 0], binaria[:, -1]])
    if borda.mean() > 127:
        binaria = cv2.bitwise_not(binaria)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binaria = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)
    binaria = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel)

    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    area_min = config.AREA_MIN_FRACAO * imagem.shape[0] * imagem.shape[1]
    return [c for c in contornos if cv2.contourArea(c) > area_min]
