import os
import pygame

from entities.domain.base import IBase


BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
WIDTH = BASE_IMG.get_width()
SPEED_TO_DECREASE_ON_MOVE = 5


class Base(IBase):
    def __init__(self, y):
        self.initial_x = 0
        self.final_x = WIDTH
        self.y = y

    def move(self):
        self._decrease_speed()

    def draw(self, win):
        win.blit(BASE_IMG, (self.initial_x, self.y))
        win.blit(BASE_IMG, (self.final_x, self.y))

    def _decrease_speed(self):
        self.initial_x -= SPEED_TO_DECREASE_ON_MOVE
        self.final_x -= SPEED_TO_DECREASE_ON_MOVE

    def _manage_x_coordinates(self):
        self.initial_x += (
            self.final_x + WIDTH if self._is_out_of_screen(self.initial_x) < 0 else 0
        )
        self.final_x += (
            self.initial_x + WIDTH
            if self._is_out_of_screen(self.initial_x) + WIDTH < 0
            else 0
        )

    def _is_out_of_screen(self, x):
        return x + WIDTH < 0
