import os
import pygame
from config.consts import SPEED

from entities.domain.base import IBase


BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
WIDTH = BASE_IMG.get_width()


class Base(IBase):
    def __init__(self, y) -> None:
        self.initial_x = 0
        self.final_x = WIDTH
        self.y = y

    def move(self) -> None:
        self._decrease_speed()

    def draw(self, win) -> None:
        win.blit(BASE_IMG, (self.initial_x, self.y))
        win.blit(BASE_IMG, (self.final_x, self.y))

    def _decrease_speed(self) -> None:
        self.initial_x -= SPEED
        self.final_x -= SPEED
