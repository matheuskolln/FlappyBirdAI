import random
import pygame
import os

from entities.domain.pipe import IPipe
from config.consts import SPEED

PIPE_BOTTOM_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png"))
)
PIPE_TOP_IMG = pygame.transform.flip(PIPE_BOTTOM_IMG, False, True)
GAP = 150


class Pipe(IPipe):
    def __init__(self, x) -> None:
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.passed = False
        self.set_height()

    def set_height(self) -> None:
        self.height = random.randrange(50, 450)
        self.top = self.height - PIPE_TOP_IMG.get_height()
        self.bottom = self.height + GAP

    def move(self) -> None:
        self.x -= SPEED

    def draw(self, win) -> None:
        win.blit(PIPE_TOP_IMG, (self.x, self.top))
        win.blit(PIPE_BOTTOM_IMG, (self.x, self.bottom))

    def collide(self, bird) -> bool:
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(PIPE_TOP_IMG)
        bottom_mask = pygame.mask.from_surface(PIPE_BOTTOM_IMG)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_collides = bird_mask.overlap(bottom_mask, bottom_offset)
        top_collides = bird_mask.overlap(top_mask, top_offset)

        if bottom_collides or top_collides:
            return True

        return False
