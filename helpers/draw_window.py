import os
from typing import List
import pygame
from entities.infra.base import Base

from entities.infra.bird import Bird
from entities.infra.pipe import Pipe

pygame.font.init()

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("Agency FB", 50)


def draw_window(
    win: pygame.Surface,
    birds: List[Bird],
    pipes: List[Pipe],
    base: Base,
    score: int,
    gen: int,
):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Gen: " + str(gen), True, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(text, (10, 70))

    text = STAT_FONT.render(f"Alive: {len(birds)}/20", True, (255, 255, 255))
    win.blit(text, (10, 130))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
