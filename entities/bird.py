import pygame
import os

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]


class Bird:

    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Inicializa o objeto
        Paramêtro x: posição inicial em x(int)
        Paramêtro y: posição inicial em y(int)
        Sem retorno
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
        Faz com que o pássaro "pule"
        Sem retorno
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        Faz com que o pássaro se movimente
        Sem retorno
        """
        self.tick_count += 1

        # Aceleração para baixo
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # Velocidade terminal
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement == 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        Paramêtro win: Pygame window ou surface
        Sem retorno
        """
        self.img_count += 1

        # Faz com que o pássaro tenha animação no seu movimento, utilizando um loop de 3 imagens
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # Define que o pássaro não baterá as asas quando estiver caindo
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Inclina o pássaro
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """
        Recebe a mask para a imagem atual do pássaro
        Sem retorno
        """
        return pygame.mask.from_surface(self.img)
