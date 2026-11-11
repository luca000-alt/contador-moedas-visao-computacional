"""Calibração px/mm usando uma moeda de R$ 1,00 (27 mm) sozinha no quadro."""
import math

import cv2

from . import config
from .classificador import circularidade
from .processamento import segmentar


def calibrar_com_moeda_de_referencia(imagem):
    """px_por_mm = diâmetro_em_pixels / diâmetro_em_mm. None se não achar."""
    redondos = [c for c in segmentar(imagem)
                if circularidade(c) > config.CIRCULARIDADE_MIN]
    if len(redondos) != 1:
        return None
    diametro_px = 2 * math.sqrt(cv2.contourArea(redondos[0]) / math.pi)
    return diametro_px / config.DIAMETRO_REFERENCIA_MM
