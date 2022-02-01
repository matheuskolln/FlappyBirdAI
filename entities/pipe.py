import random
import pygame
import os

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

class Pipe:
    """
    Classe que representa o objeto cano
    """

    GAP = 150
    VEL = 5

    def __init__(self, x):
        """
        Inicializa o objeto cano
        Paramêtro x: posição x do cano(int)
        Sem retorno
        """
        self.x = x
        self.height = 0
        self.gap = 100

        # Onde se localiza o topo e a base do cano
        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

        self.set_height()

    def set_height(self):
        """
        Estabelece a altura do cano, a partir do topo da tela
        Sem retorno
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        Move o cano baseado na velocidade
        Sem retorno
        """
        self.x -= self.VEL

    def draw(self, win):
        """
        Põe na tela o topo e a base do cano
        Paramêtro win: Pygame window or surface
        Sem retorno
        """
        # Põe o topo
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # Põe a base
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """
        Retorna se um ponto está colidindo com o cano
        Paramêtro bird: Objeto bird
        Retorna: lógico
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False
