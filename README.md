# Contador de Moedas de Real com Visão Computacional

Entrega 3 — Protótipo funcional. Detecta moedas de R$ 0,05, 0,10, 0,25, 0,50 e 1,00
pela webcam (ou em foto), identifica o valor de cada uma e mostra a quantidade e o total em tempo real.


**Integrantes:**

Kaio Breno de Freitas Pinho - RA 12724130159
Lucas Ribeiro de Souza Neves - RA 12723130991
Kelvin Oliveira dos Santos - RA 12724122807


## Instalação (Python 3.10+)
```bash
pip install -r requirements.txt
```

## Execução
```bash

python main.py # Webcam em tempo rea

python main.py --imagem foto.jpg --saida resultado.png # Foto (calibra com UMA moeda de R$ 1,00 sozinha na foto)

python main.py --imagem foto.jpg --px-por-mm 5.0 # Foto com escala já conhecida

python main.py --imagem exemplos/teste_sintetico.png --px-por-mm 5 --saida exemplos/resultado.png # Demonstração incluída
```


**Webcam:**

coloque UMA moeda de R$ 1,00 sozinha no quadro e tecle `c` para calibrar;
depois espalhe as demais moedas. Tecle `q` para sair. Se mover a câmera, calibre de novo.

## Como funciona

1. **Captura** e redimensionamento para largura fixa (`processamento.padronizar`).
2. **Pré-processamento:** cinza, desfoque gaussiano 5x5 e CLAHE.
3. **Segmentação:** limiar de Otsu + abertura/fechamento morfológico + contornos; ignora áreas pequenas.

4. **Classificação** (`classificador.py`):
   - circularidade = 4·π·área / perímetro² (> 0,80 → moeda candidata);
   - diâmetro (mm) = 2·√(área/π) / px_por_mm;
   - cor (saturação HSV) separa bronze × prata; escolhe a moeda de menor erro de diâmetro
     (tolerância de 1 mm). Na dúvida, o objeto é ignorado.

5. **Calibração:** px_por_mm = diâmetro_em_pixels / 27 mm (moeda de R$ 1,00).
6. **Resultado:** caixa com o valor em cada moeda, quantidade e total na tela.


## Estrutura

```
main.py              # programa principal (webcam / foto)
src/config.py        # tabela de moedas e limiares (ajuste aqui)
src/processamento.py # pré-processamento e segmentação
src/classificador.py # circularidade, diâmetro, cor e valor
src/calibracao.py    # escala px/mm
src/contador.py      # soma e anotação
tests/               # testes automáticos (pytest)
exemplos/            # imagem de demonstração e resultado
```

## Testes
```bash
pytest
```


## Limitações

Moedas encostadas/empilhadas, sombras fortes, reflexos e moedas muito gastas podem errar.
Fundo liso, boa luz e câmera de cima são necessários. `SATURACAO_PRATA` e `TOLERANCIA_MM`
em `src/config.py` devem ser ajustados com fotos reais.
