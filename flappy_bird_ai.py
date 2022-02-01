"""
PT-BR -> Projeto feito utilizando a biblioteca de desenvolvimento de jogos Pygame, e a biblioteca NEAT, que
baseia-se na evolução de redes neurais arbritárias. Inspirado no tutorial do canal Tech with Tim.
EN-US -> The project was made using the Pygame library for game development and the NEAT library, which works
on the evolution of arbitrary neural networks. Inspired by the channel Tech with Tim.
Autor/Author: Matheus Henrique Kolln Nagildo
Última modificação/Last modification: 30/11/2019
"""

import pygame
import neat
import os
import random

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("Agency FB", 50)


class Bird:
    """
    Classe que representa o Flappy Bird
    """

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


class Base:
    """
    Representa o chão que se move no jogo
    """

    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        """
        Inicializa o objeto Base
        Paramêtro y: int
        Sem retorno
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        Move o chão como se estivesse "rolando"
        Sem retorno
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        Coloca o chão na tela, fazendo com que as duas imagens movam-se juntas
        Paramêtro win: Pygame win/surface
        Sem retorno
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


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


def main(genomes, config):
    """
    Roda a simulação da população atual de pássaros e estabelece seu fitness baseado
    na distância em que eles chegam no jogo
    """
    global GEN
    GEN += 1

    # Começa criando listas que contém o próprio genoma
    # e a rede neural associada ao genoma e o objeto de
    # pássaro que utiliza desta rede para jogar
    nets = []
    ge = []
    birds = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        genome.fitness = 0  # Começa com o nível de fitness igual a 0
        ge.append(genome)

    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(birds) > 0:
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):  # Determina se usa o primeiro ou o segundo
                pipe_ind = 1  # cano na tela para o input da rede neural
        else:
            run = False
            break

        for x, bird in enumerate(
            birds
        ):  # Dá para cada pássaro 0.1 de fitness por frame que permanece vivo
            bird.move()
            ge[x].fitness += 0.1

            # Manda a localização do pássaro, localização do topo do cano, base do cano e determinado pela rede neural pula ou não
            output = nets[x].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_ind].height),
                    abs(bird.y - pipes[pipe_ind].bottom),
                )
            )

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_file):
    """
    Roda o algoritmo NEAT para treinar a rede neural que jogará flappy bird
    Paramêtro config_file: Localização do arquivo de configuração
    Sem retorno
    """
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # Cria a população, que é o objeto de maior nível para execução NEAT
    p = neat.Population(config)

    # Adiciona um stdout reporter para mostrar o progresso no terminal.
    p.add_reporter(neat.StdOutReporter(show_species_detail=True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Roda o jogo até 50 gerações
    winner = p.run(main, 50)

    # Mostra as estatísticas finais
    print("\nBest genome:\n{!s}".format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
