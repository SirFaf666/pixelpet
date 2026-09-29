"""Menu gráfico apresentado antes de abrir o Desktop Pet."""

import pygame

from data_manager import GestorDados
from ovo import Ovo


LARGURA = 440
ALTURA = 420


class MenuPrincipal:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PixelPet - Menu")
        self.ecra = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont("segoeui", 18)
        self.fonte_titulo = pygame.font.SysFont("segoeui", 32, bold=True)
        self.nome = "Pixel"
        self.campo_nome = pygame.Rect(95, 130, 250, 38)
        self.botoes = [
            (pygame.Rect(95, 190, 250, 44), "novo_ovo", "Novo ovo"),
            (pygame.Rect(95, 246, 250, 44), "continuar", "Continuar"),
            (pygame.Rect(95, 302, 250, 44), "sair", "Sair"),
        ]

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None, None
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        self.nome = self.nome[:-1]
                    elif evento.key == pygame.K_RETURN:
                        return "ovo", self._criar_ovo()
                    elif evento.unicode.isprintable() and len(self.nome) < 16:
                        self.nome += evento.unicode
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for rect, acao, _ in self.botoes:
                        if rect.collidepoint(evento.pos):
                            if acao == "novo_ovo":
                                return "ovo", self._criar_ovo()
                            if acao == "continuar":
                                return self._continuar()
                            return None, None
            self._desenhar()
            self.relogio.tick(30)

    def _criar_ovo(self):
        GestorDados.apagar_save()
        ovo = Ovo(self.nome.strip() or "Pixel")
        GestorDados.guardar_ovo(ovo)
        return ovo

    def _continuar(self):
        if GestorDados.existe_ovo():
            return "ovo", GestorDados.carregar_ovo()
        if GestorDados.existe_save():
            return "pet", GestorDados.carregar()
        return "ovo", self._criar_ovo()

    def _desenhar(self):
        self.ecra.fill((232, 242, 244))
        pygame.draw.rect(self.ecra, (45, 70, 82), (0, 0, LARGURA, 92))
        titulo = self.fonte_titulo.render("PixelPet", True, (255, 255, 255))
        self.ecra.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 34)))
        subtitulo = self.fonte.render("O teu companheiro de ambiente de trabalho", True, (202, 230, 232))
        self.ecra.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 68)))

        rotulo = self.fonte.render("Nome do proximo pet", True, (45, 55, 65))
        self.ecra.blit(rotulo, (95, 105))
        pygame.draw.rect(self.ecra, (255, 255, 255), self.campo_nome, border_radius=5)
        pygame.draw.rect(self.ecra, (90, 120, 135), self.campo_nome, width=2, border_radius=5)
        nome = self.fonte.render(self.nome, True, (35, 45, 55))
        self.ecra.blit(nome, (self.campo_nome.x + 10, self.campo_nome.y + 8))

        tem_progresso = GestorDados.existe_ovo() or GestorDados.existe_save()
        for rect, acao, texto in self.botoes:
            cor = (75, 145, 120) if acao == "novo_ovo" else (75, 105, 145)
            if acao == "sair":
                cor = (135, 80, 80)
            if acao == "continuar" and not tem_progresso:
                cor = (145, 155, 160)
            pygame.draw.rect(self.ecra, cor, rect, border_radius=6)
            texto_render = self.fonte.render(texto, True, (255, 255, 255))
            self.ecra.blit(texto_render, texto_render.get_rect(center=rect.center))
        pygame.display.flip()