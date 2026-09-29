"""Ponto de entrada do PixelPet Desktop para Windows."""

import pygame

from desktop_pet import DesktopPet
from incubadora import Incubadora
from menu import MenuPrincipal


def main():
    modo, estado = MenuPrincipal().executar()
    if modo == "ovo":
        estado = Incubadora(estado).executar()
        if estado is None:
            pygame.quit()
            return
    if modo == "pet":
        DesktopPet(estado).executar()
    elif estado is not None:
        DesktopPet(estado).executar()


if __name__ == "__main__":
    main()
