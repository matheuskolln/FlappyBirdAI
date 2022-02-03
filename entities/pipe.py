import random
import pygame
import os

from entities.domain.pipe import IPipe

PIPE_BOTTOM_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png"))
)
PIPE_TOP_IMG = pygame.transform.flip(PIPE_BOTTOM_IMG, False, True)
GAP = 150
SPEED = 5


class Pipe(IPipe):
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - PIPE_TOP_IMG.get_height()
        self.bottom = self.height + GAP

    def move(self):
        self.x -= SPEED

    def draw(self, win):
        win.blit(PIPE_TOP_IMG, (self.x, self.top))
        win.blit(PIPE_BOTTOM_IMG, (self.x, self.bottom))

    def collide(self, bird):
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
