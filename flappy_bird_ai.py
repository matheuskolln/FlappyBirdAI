"""
PT-BR -> Projeto feito utilizando a biblioteca de desenvolvimento de jogos Pygame, e a biblioteca NEAT, que
baseia-se na evolução de redes neurais arbritárias. Inspirado no tutorial do canal Tech with Tim.
EN-US -> The project was made using the Pygame library for game development and the NEAT library, which works
on the evolution of arbitrary neural networks. Inspired by the channel Tech with Tim.
Autor/Author: Matheus Henrique Kolln Nagildo
Última modificação/Last modification: 30/11/2019
"""

from entities.infra.base import Base
from entities.infra.bird import Bird
import pygame
import neat
import os

from entities.pipe import Pipe
from helpers.draw_window import draw_window


WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0


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
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
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
