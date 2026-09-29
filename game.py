"""
game.py
Ciclo principal do jogo: cria a janela, desenha o pet, os botões de
ação e as barras de estado, e liga tudo à classe Pet.
"""

import sys
import pygame

from pet import Pet
from sprites import GestorAnimacao
from data_manager import GestorDados


LARGURA_JANELA = 480
ALTURA_JANELA = 520
COR_FUNDO = (235, 245, 250)

FPS = 30
INTERVALO_ATUALIZACAO_MS = 4000  # a cada 4s o pet "envelhece" um pouco 


class Botao:
    """Um botão retangular simples e clicável."""

    def __init__(self, rect, texto, acao, cor=(90, 160, 220)):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.acao = acao
        self.cor = cor

    def desenhar(self, superficie, fonte):
        pygame.draw.rect(superficie, self.cor, self.rect, border_radius=8)
        pygame.draw.rect(superficie, (30, 30, 30), self.rect, width=2, border_radius=8)
        texto_render = fonte.render(self.texto, True, (255, 255, 255))
        pos = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, pos)

    def clicado(self, pos_rato):
        return self.rect.collidepoint(pos_rato)


class Jogo:
    """Classe principal que gere o loop do jogo (Programação Orientada a Objetos)."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PixelPet")
        self.ecra = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("arial", 18)
        self.fonte_pequena = pygame.font.SysFont("arial", 14)
        self.fonte_titulo = pygame.font.SysFont("arial", 26, bold=True)

        self.animador = GestorAnimacao(escala=14)
        self.pet = self._carregar_ou_criar_pet()
        self.mensagem = f"Bem-vindo(a), {self.pet.nome}!"

        self.a_correr = True
        self.evento_atualizar = pygame.USEREVENT + 1
        pygame.time.set_timer(self.evento_atualizar, INTERVALO_ATUALIZACAO_MS)

        self.botoes = [
            Botao((20, 420, 100, 45), "Alimentar", "alimentar", (80, 180, 100)),
            Botao((130, 420, 100, 45), "Brincar", "brincar", (240, 170, 60)),
            Botao((240, 420, 100, 45), "Limpar", "limpar", (80, 160, 220)),
            Botao((350, 420, 110, 45), "Dormir", "dormir", (120, 100, 200)),
            Botao((20, 470, 130, 40), "Repreender", "repreender", (200, 70, 70)),
            Botao((160, 470, 150, 40), "Gravar jogo", "gravar", (90, 90, 90)),
            Botao((320, 470, 140, 40), "Ver gráfico", "grafico", (60, 140, 140)),
        ]

    def _carregar_ou_criar_pet(self) -> Pet:
        if GestorDados.existe_save():
            try:
                return GestorDados.carregar()
            except (FileNotFoundError, KeyError, ValueError):
                pass
        return Pet(nome="Pixel")

    # ------------------------------------------------------------------
    def executar(self):
        while self.a_correr:
            self._processar_eventos()
            self._desenhar()
            self.relogio.tick(FPS)

        GestorDados.guardar(self.pet)
        pygame.quit()
        sys.exit()

    # ------------------------------------------------------------------
    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.a_correr = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in self.botoes:
                    if botao.clicado(evento.pos):
                        self._executar_acao(botao.acao)

            elif evento.type == self.evento_atualizar:
                self.pet.atualizar_estado()

    def _executar_acao(self, acao: str):
        if acao == "alimentar":
            self.mensagem = self.pet.alimentar()
        elif acao == "brincar":
            self.mensagem = self.pet.brincar()
        elif acao == "limpar":
            self.mensagem = self.pet.limpar()
        elif acao == "dormir":
            self.mensagem = self.pet.dormir()
        elif acao == "repreender":
            self.mensagem = self.pet.repreender()
        elif acao == "gravar":
            GestorDados.guardar(self.pet)
            self.mensagem = "Jogo gravado com sucesso!"
        
    # ------------------------------------------------------------------
    def _barra(self, superficie, x, y, valor, cor, rotulo):
        largura_total = 180
        pygame.draw.rect(superficie, (220, 220, 220), (x, y, largura_total, 18), border_radius=4)
        largura_preenchida = int(largura_total * valor / 100)
        pygame.draw.rect(superficie, cor, (x, y, largura_preenchida, 18), border_radius=4)
        pygame.draw.rect(superficie, (30, 30, 30), (x, y, largura_total, 18), width=1, border_radius=4)
        texto = self.fonte_pequena.render(f"{rotulo}: {valor}", True, (20, 20, 20))
        superficie.blit(texto, (x, y - 18))

    def _desenhar(self):
        self.ecra.fill(COR_FUNDO)

        titulo = self.fonte_titulo.render(f"PixelPet — {self.pet.nome}", True, (40, 40, 40))
        self.ecra.blit(titulo, (20, 15))

        # Sprite do pet, centrado
        estado = self.pet.estado_atual()
        px = (LARGURA_JANELA - self.animador.largura_px()) // 2
        py = 60
        self.animador.desenhar(self.ecra, estado, px, py)

        # Barras de estado
        self._barra(self.ecra, 20, 300, self.pet.fome, (80, 180, 100), "Fome")
        self._barra(self.ecra, 260, 300, self.pet.energia, (240, 170, 60), "Energia")
        self._barra(self.ecra, 20, 350, self.pet.higiene, (80, 160, 220), "Higiene")
        self._barra(self.ecra, 260, 350, self.pet.carma, (220, 70, 130), "Carma")

        carma_texto = self.fonte.render(
            f"Como o pet se sente em relação a ti: {self.pet.nivel_carma_texto()}",
            True, (60, 60, 60)
        )
        self.ecra.blit(carma_texto, (20, 385))

        if not self.pet.vivo:
            aviso = self.fonte.render("O teu pet fugiu por negligência... 💔", True, (200, 30, 30))
            self.ecra.blit(aviso, (20, 385))

        for botao in self.botoes:
            botao.desenhar(self.ecra, self.fonte_pequena)

        msg_render = self.fonte_pequena.render(self.mensagem, True, (50, 50, 50))
        self.ecra.blit(msg_render, (20, 500))  # linha de estado (última mensagem)

        pygame.display.flip()


if __name__ == "__main__":
    Jogo().executar()
