import os
import pygame

pygame.font.init()

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("Agency FB", 50)

def draw_window(win, birds, pipes, base, score, gen):
    """
    Coloca as janelas para o jogo
    Paramêtro win: Pygame window surface
    Paramêtro birds: O conjunto de pássaros(objeto pássaro)
    Paramêtro pipes: Canos
    Paramêtro base: Chão do jogo
    Paramêtro score: Pontuação do jogo(int)
    Paramêtro gen: Geração atual da rede neural(int)
    """
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    # Geração atual da rede neural
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    # Pontuação do melhor pássaro da geração
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (10, 70))

    # Quantidade de pássaros vivo da geração
    text = STAT_FONT.render(f"Alive: {len(birds)}/20", 1, (255, 255, 255))
    win.blit(text, (10, 130))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
