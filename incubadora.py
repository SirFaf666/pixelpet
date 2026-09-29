"""Ecrã de incubação que transforma um ovo num pet."""

import pygame

from data_manager import GestorDados
from ovo import Ovo


class Incubadora:
    def __init__(self, ovo: Ovo):
        self.ovo = ovo
        pygame.display.set_caption("PixelPet - Incubadora")
        self.ecra = pygame.display.set_mode((340, 420))
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("segoeui", 17)
        self.fonte_titulo = pygame.font.SysFont("segoeui", 24, bold=True)
        self.botao_cuidar = pygame.Rect(40, 315, 125, 42)
        self.botao_chocar = pygame.Rect(175, 315, 125, 42)
        self.mensagem = "Dá calor ao ovo para o preparar."

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.botao_cuidar.collidepoint(evento.pos):
                        self.mensagem = self.ovo.incubar()
                        GestorDados.guardar_ovo(self.ovo)
                    if self.botao_chocar.collidepoint(evento.pos) and self.ovo.pronto_a_chocar:
                        pet = self.ovo.chocar()
                        GestorDados.guardar(pet)
                        GestorDados.apagar_ovo()
                        return pet
            self._desenhar()
            self.relogio.tick(30)

    def _desenhar(self):
        self.ecra.fill((250, 242, 224))
        titulo = self.fonte_titulo.render("Incubadora", True, (70, 75, 65))
        self.ecra.blit(titulo, titulo.get_rect(center=(170, 35)))
        pygame.draw.ellipse(self.ecra, (245, 204, 113), (105, 75, 130, 180))
        pygame.draw.ellipse(self.ecra, (130, 100, 60), (105, 75, 130, 180), width=3)
        for x, y in ((145, 125), (185, 160), (155, 205)):
            pygame.draw.circle(self.ecra, (225, 145, 80), (x, y), 9)

        progresso = self.fonte.render(
            f"Calor: {self.ovo.cuidados}/{self.ovo.CUIDADOS_NECESSARIOS}", True, (70, 75, 65)
        )
        self.ecra.blit(progresso, progresso.get_rect(center=(170, 275)))
        mensagem = self.fonte.render(self.mensagem, True, (70, 75, 65))
        self.ecra.blit(mensagem, mensagem.get_rect(center=(170, 295)))

        for rect, texto, cor in (
            (self.botao_cuidar, "Dar calor", (204, 135, 64)),
            (self.botao_chocar, "Chocar", (76, 145, 120)),
        ):
            if texto == "Chocar" and not self.ovo.pronto_a_chocar:
                cor = (155, 165, 155)
            pygame.draw.rect(self.ecra, cor, rect, border_radius=6)
            texto_render = self.fonte.render(texto, True, (255, 255, 255))
            self.ecra.blit(texto_render, texto_render.get_rect(center=rect.center))
        pygame.display.flip()