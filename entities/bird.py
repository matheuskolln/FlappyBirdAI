import pygame
import os

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

MAX_ROTATION = 25
ROTATION_SPEED = 20
ANIMATION_TIME = 5


class Bird:
    def __init__(self, x, y):
        """
        Inicializa o objeto
        Paramêtro x: posição inicial em x(int)
        Paramêtro y: posição inicial em y(int)
        Sem retorno
        """
        self.x = x
        self.y = y
        self.inclination = 0
        self.tick_count = 0
        self.speed = 0
        self.height = self.y
        self.image_count = 0
        self.image = BIRD_IMGS[0]

    def jump(self):
        """
        Faz com que o pássaro "pule"
        Sem retorno
        """
        self.speed = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        displacement = self.speed * self.tick_count + 1.5 * self.tick_count**2

        # Velocidade terminal
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement == 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.inclination < MAX_ROTATION:
                self.inclination = MAX_ROTATION
        else:
            if self.inclination > -90:
                self.inclination -= ROTATION_SPEED

    def draw(self, win):
        """
        Paramêtro win: Pygame window ou surface
        Sem retorno
        """
        self.image_count += 1

        # Faz com que o pássaro tenha animação no seu movimento, utilizando um loop de 3 imagens
        if self.image_count < ANIMATION_TIME:
            self.image = BIRD_IMGS[0]
        elif self.image_count < ANIMATION_TIME * 2:
            self.image = BIRD_IMGS[1]
        elif self.image_count < ANIMATION_TIME * 3:
            self.image = BIRD_IMGS[2]
        elif self.image_count < ANIMATION_TIME * 4:
            self.image = BIRD_IMGS[1]
        elif self.image_count == ANIMATION_TIME * 4 + 1:
            self.image = BIRD_IMGS[0]
            self.image_count = 0

        # Define que o pássaro não baterá as asas quando estiver caindo
        if self.inclination <= -80:
            self.image = BIRD_IMGS[1]
            self.image_count = ANIMATION_TIME * 2

        # Inclina o pássaro
        rotated_image = pygame.transform.rotate(self.image, self.inclination)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """
        Recebe a mask para a imagem atual do pássaro
        Sem retorno
        """
        return pygame.mask.from_surface(self.image)
