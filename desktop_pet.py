"""Janela compacta do PixelPet para usar no ambiente de trabalho Windows."""

import ctypes
import sys

import pygame

from data_manager import GestorDados
from pet import Pet
from sprites import GestorAnimacao


LARGURA = 520
ALTURA = 620
FPS = 30
INTERVALO_ATUALIZACAO_MS = 30_000
INTERVALO_EVENTO_MS = 120_000

COR_FUNDO = (13, 15, 28)
COR_PAINEL = (29, 29, 45)
COR_TEXTO = (239, 241, 248)
COR_TEXTO_SECUNDARIO = (169, 175, 193)
COR_DESTAQUE = (33, 190, 146)


class Botao:
    def __init__(self, rect, texto, acao, cor):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.acao = acao
        self.cor = cor

    def desenhar(self, superficie, fonte):
        pygame.draw.rect(superficie, self.cor, self.rect, border_radius=6)
        pygame.draw.rect(superficie, (35, 45, 55), self.rect, width=1, border_radius=6)
        texto = fonte.render(self.texto, True, (255, 255, 255))
        superficie.blit(texto, texto.get_rect(center=self.rect.center))


class DesktopPet:
    """Apresenta o pet numa janela pequena, persistente e sempre visível."""

    def __init__(self, pet: Pet | None = None):
        pygame.init()
        pygame.display.set_caption("PixelPet - Desktop Pet")
        self.ecra = pygame.display.set_mode((LARGURA, ALTURA))
        self._manter_no_topo()

        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("segoeui", 16)
        self.fonte_pequena = pygame.font.SysFont("segoeui", 13, bold=True)
        self.fonte_titulo = pygame.font.SysFont("segoeui", 24, bold=True)
        self.animador = GestorAnimacao(escala=15)
        self.pet = pet or self._carregar_ou_criar_pet()
        self.mensagem = f"Olá, sou o/a {self.pet.nome}."
        self.a_correr = True

        self.evento_atualizar = pygame.USEREVENT + 1
        self.evento_aleatorio = pygame.USEREVENT + 2
        pygame.time.set_timer(self.evento_atualizar, INTERVALO_ATUALIZACAO_MS)
        pygame.time.set_timer(self.evento_aleatorio, INTERVALO_EVENTO_MS)

        self.botoes = [
            Botao((58, 210, 88, 88), "Comer", "alimentar", (188, 148, 239)),
            Botao((160, 210, 88, 88), "Brincar", "brincar", (188, 148, 239)),
            Botao((262, 210, 88, 88), "Limpar", "limpar", (188, 148, 239)),
            Botao((364, 210, 88, 88), "Dormir", "dormir", (188, 148, 239)),
        ]

    def _manter_no_topo(self):
        """Ativa a opção 'sempre no topo' quando a janela corre em Windows."""
        if sys.platform != "win32":
            return
        try:
            janela = pygame.display.get_wm_info()["window"]
            ctypes.windll.user32.SetWindowPos(janela, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
        except (KeyError, AttributeError, OSError):
            pass

    def _carregar_ou_criar_pet(self) -> Pet:
        if GestorDados.existe_save():
            try:
                return GestorDados.carregar()
            except (FileNotFoundError, KeyError, ValueError):
                pass
        return Pet("Pixel")

    def executar(self):
        while self.a_correr:
            self._processar_eventos()
            self._desenhar()
            self.relogio.tick(FPS)

        GestorDados.guardar(self.pet)
        pygame.quit()

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.a_correr = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in self.botoes:
                    if botao.rect.collidepoint(evento.pos):
                        self._executar_acao(botao.acao)
            elif evento.type == self.evento_atualizar:
                self.pet.atualizar_estado()
                GestorDados.guardar(self.pet)
            elif evento.type == self.evento_aleatorio:
                self.mensagem = self.pet.evento_aleatorio()

    def _executar_acao(self, acao):
        acoes = {
            "alimentar": self.pet.alimentar,
            "brincar": self.pet.brincar,
            "limpar": self.pet.limpar,
            "dormir": self.pet.dormir,
        }
        self.mensagem = acoes[acao]()
        GestorDados.guardar(self.pet)

    def _texto_curto(self, texto, largura_maxima):
        while self.fonte.size(texto)[0] > largura_maxima and len(texto) > 3:
            texto = texto[:-4] + "..."
        return texto

    def _medidor(self, centro, valor, cor, rotulo):
        raio = 39
        rect = pygame.Rect(centro[0] - raio, centro[1] - raio, raio * 2, raio * 2)
        pygame.draw.circle(self.ecra, (59, 63, 82), centro, raio, width=8)
        angulo_final = -90 + (360 * valor / 100)
        pygame.draw.arc(self.ecra, cor, rect, -90 * 0.0174533, angulo_final * 0.0174533, 8)
        texto = self.fonte_pequena.render(rotulo, True, COR_TEXTO)
        self.ecra.blit(texto, texto.get_rect(center=centro))
        percentagem = self.fonte_pequena.render(f"{valor}%", True, COR_TEXTO)
        self.ecra.blit(percentagem, percentagem.get_rect(center=(centro[0], centro[1] + 57)))

    def _desenhar_item(self, botao):
        botao.desenhar(self.ecra, self.fonte_pequena)
        cores = {
            "alimentar": (224, 152, 89),
            "brincar": (250, 225, 92),
            "limpar": (104, 195, 237),
            "dormir": (120, 107, 190),
        }
        pygame.draw.circle(self.ecra, cores[botao.acao], botao.rect.center, 18)

    def _desenhar(self):
        self.ecra.fill(COR_FUNDO)
        painel = pygame.Rect(24, 24, LARGURA - 48, ALTURA - 48)
        pygame.draw.rect(self.ecra, COR_PAINEL, painel, border_radius=10)
        titulo = self.fonte_titulo.render(self.pet.nome, True, COR_TEXTO)
        self.ecra.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 46)))

        sprite_x = (LARGURA - self.animador.largura_px()) // 2
        self.animador.desenhar(self.ecra, self.pet.estado_atual(), sprite_x, 337)

        self._medidor((88, 112), self.pet.fome, COR_DESTAQUE, "Fome")
        self._medidor((198, 112), self.pet.energia, COR_DESTAQUE, "Energia")
        self._medidor((308, 112), self.pet.higiene, COR_DESTAQUE, "Higiene")
        self._medidor((418, 112), self.pet.carma, COR_DESTAQUE, "Carma")

        for botao in self.botoes:
            self._desenhar_item(botao)

        mensagem = self._texto_curto(self.mensagem, LARGURA - 70)
        texto = self.fonte.render(mensagem, True, COR_TEXTO_SECUNDARIO)
        caixa = texto.get_rect(center=(LARGURA // 2, 564))
        self.ecra.blit(texto, caixa)
        pygame.display.flip()


if __name__ == "__main__":
    DesktopPet().executar()