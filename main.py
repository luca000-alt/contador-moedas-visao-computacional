import argparse
import sys

import cv2

from src.calibracao import calibrar_com_moeda_de_referencia
from src.contador import anotar, contar
from src.processamento import padronizar


def parse():
    p = argparse.ArgumentParser(description=__doc__)
    fonte = p.add_mutually_exclusive_group()
    fonte.add_argument("--imagem", help="caminho de uma foto")
    fonte.add_argument("--camera", type=int, default=0, help="índice da webcam")
    p.add_argument("--px-por-mm", type=float, help="escala já conhecida")
    p.add_argument("--saida", help="salva a imagem anotada (modo foto)")
    p.add_argument("--sem-janela", action="store_true", help="não abrir janela")
    return p.parse_args()


def modo_foto(args):
    imagem = cv2.imread(args.imagem)
    if imagem is None:
        sys.exit(f"Erro: não foi possível abrir '{args.imagem}'.")
    imagem = padronizar(imagem)
    escala = args.px_por_mm or calibrar_com_moeda_de_referencia(imagem)
    if not escala:
        sys.exit("Erro: use --px-por-mm ou deixe só UMA moeda de R$ 1,00 na foto.")
    total, contagem, itens = contar(imagem, escala)
    print(f"Escala: {escala:.3f} px/mm")
    for valor in sorted(contagem):
        print(f"  {contagem[valor]} x R$ {valor:.2f}")
    print(f"Moedas: {sum(contagem.values())} | Total: R$ {total:.2f}")
    saida = anotar(imagem, total, contagem, itens)
    if args.saida:
        cv2.imwrite(args.saida, saida)
    if not args.sem_janela:
        cv2.imshow("Contador de moedas", saida)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def modo_camera(args):
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        sys.exit("Erro: não foi possível abrir a câmera.")
    escala = args.px_por_mm
    print("Teclas: [c] calibrar (só 1 moeda de R$ 1,00 no quadro) | [q] sair")
    while True:
        ok, quadro = cap.read()
        if not ok:
            break
        quadro = padronizar(quadro)
        limpo = quadro.copy()
        if escala:
            total, contagem, itens = contar(quadro, escala)
            quadro = anotar(quadro, total, contagem, itens)
        else:
            cv2.putText(quadro, "Calibre: 1 moeda de R$1 e tecle [c]", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Contador de moedas", quadro)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord("q"):
            break
        if tecla == ord("c"):
            nova = calibrar_com_moeda_de_referencia(limpo)
            escala = nova or escala
            print(f"Escala: {escala:.3f} px/mm" if escala else "Calibração falhou.")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    args = parse()
    modo_foto(args) if args.imagem else modo_camera(args)
