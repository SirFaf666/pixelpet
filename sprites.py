"""
sprites.py
Define a "pixel art" do pet como matrizes (listas de listas) de cores.
Cada célula da matriz é desenhada como um pequeno quadrado no ecrã,
por isso não precisamos de nenhum ficheiro de imagem externo.
"""

import pygame

# Paleta de cores reutilizada nos sprites (código -> cor RGB)
PALETA = {
    ".": None,               # transparente / fundo
    "K": (30, 30, 30),       # contorno
    "B": (255, 214, 170),    # corpo (bege)
    "O": (255, 150, 60),     # detalhe laranja
    "W": (255, 255, 255),    # branco (olhos)
    "R": (200, 40, 40),      # vermelho (boca triste / zangado)
    "P": (255, 105, 180),    # rosa (feliz / coraçõezinhos)
    "Z": (120, 170, 255),    # azul (zzz / sono)
    "G": (120, 200, 120),    # verde (fofo/normal)
}

TAMANHO_GRELHA = 16  # sprites 16x16 "pixels"


def _grelha_vazia():
    return [["." for _ in range(TAMANHO_GRELHA)] for _ in range(TAMANHO_GRELHA)]


def _corpo_base(cor_corpo="B"):
    """Gera uma grelha com um corpo ovalado simples, reutilizado por todos os estados."""
    grelha = _grelha_vazia()
    for y in range(4, 13):
        largura = {4: 6, 5: 8, 6: 9, 7: 10, 8: 10, 9: 10, 10: 9, 11: 8, 12: 6}[y]
        inicio = (TAMANHO_GRELHA - largura) // 2
        for x in range(inicio, inicio + largura):
            grelha[y][x] = cor_corpo
    return grelha


def _contornar(grelha):
    """Acrescenta um contorno preto (K) à volta de qualquer pixel preenchido."""
    vizinhos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    nova = [linha[:] for linha in grelha]
    for y in range(TAMANHO_GRELHA):
        for x in range(TAMANHO_GRELHA):
            if grelha[y][x] != ".":
                continue
            for dy, dx in vizinhos:
                ny, nx = y + dy, x + dx
                if 0 <= ny < TAMANHO_GRELHA and 0 <= nx < TAMANHO_GRELHA:
                    if grelha[ny][nx] != ".":
                        nova[y][x] = "K"
                        break
    return nova


def _sprite_normal():
    g = _corpo_base()
    g[7][6], g[7][10] = "K", "K"          # olhos
    g[9][7], g[9][8], g[9][9] = "K", "K", "K"  # boca reta
    return _contornar(g)


def _sprite_muito_feliz():
    g = _corpo_base()
    g[7][6], g[7][10] = "K", "K"          # olhos
    g[9][6] = g[9][7] = g[9][8] = g[9][9] = g[9][10] = "K"
    g[10][7] = g[10][9] = "K"             # sorriso curvo
    g[2][4] = g[2][11] = "P"              # coraçõezinhos
    return _contornar(g)


def _sprite_triste():
    g = _corpo_base()
    g[7][6], g[7][10] = "K", "K"
    g[10][7], g[10][8], g[10][9] = "K", "K", "K"
    g[9][6] = g[9][10] = "K"              # boca curva para baixo
    return _contornar(g)


def _sprite_esfomeado():
    g = _corpo_base(cor_corpo="O")
    g[7][6], g[7][10] = "K", "K"
    g[9][8] = "R"                          # boca pequena vermelha
    return _contornar(g)


def _sprite_sujo():
    g = _corpo_base(cor_corpo="G")
    g[7][6], g[7][10] = "K", "K"
    g[9][7], g[9][8], g[9][9] = "K", "K", "K"
    for (y, x) in [(6, 5), (8, 11), (11, 6)]:
        g[y][x] = "K"                      # manchas de sujidade
    return _contornar(g)


def _sprite_a_dormir():
    g = _corpo_base(cor_corpo="B")
    g[7][6], g[7][10] = "K", "K"           # olhos fechados (linhas)
    g[2][12] = "Z"
    g[1][13] = "Z"
    return _contornar(g)


def _sprite_morto():
    g = _corpo_base(cor_corpo="B")
    g[7][6] = g[7][7] = "K"                # X no olho esquerdo
    g[7][9] = g[7][10] = "K"               # X no olho direito
    g[10][7], g[10][8], g[10][9] = "R", "R", "R"
    return _contornar(g)


# Mapa estado -> sprite (gerado uma única vez, como uma "sprite sheet")
SPRITES = {
    "normal": _sprite_normal(),
    "muito_feliz": _sprite_muito_feliz(),
    "triste": _sprite_triste(),
    "esfomeado": _sprite_esfomeado(),
    "sujo": _sprite_sujo(),
    "a_dormir": _sprite_a_dormir(),
    "morto": _sprite_morto(),
}


class GestorAnimacao:
    """Responsável por desenhar o sprite certo no ecrã, com uma pequena
    animação de "respiração" (o pet aumenta e diminui ligeiramente)."""

    def __init__(self, escala: int = 14):
        self.escala = escala
        self.contador_frames = 0

    def largura_px(self):
        return TAMANHO_GRELHA * self.escala

    def altura_px(self):
        return TAMANHO_GRELHA * self.escala

    def desenhar(self, superficie: pygame.Surface, estado: str, pos_x: int, pos_y: int):
        grelha = SPRITES.get(estado, SPRITES["normal"])

        # Pequena animação: desloca 1px para cima e para baixo (respiração)
        self.contador_frames += 1
        deslocamento = 2 if (self.contador_frames // 20) % 2 == 0 else 0

        for y, linha in enumerate(grelha):
            for x, codigo in enumerate(linha):
                cor = PALETA.get(codigo)
                if cor is None:
                    continue
                rect = pygame.Rect(
                    pos_x + x * self.escala,
                    pos_y + y * self.escala + deslocamento,
                    self.escala,
                    self.escala,
                )
                pygame.draw.rect(superficie, cor, rect)
