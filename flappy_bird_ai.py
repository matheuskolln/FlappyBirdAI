"""
PT-BR -> Projeto feito utilizando a biblioteca de desenvolvimento de jogos Pygame, e a biblioteca NEAT, que
baseia-se na evolução de redes neurais arbritárias. Inspirado no tutorial do canal Tech with Tim.
EN-US -> The project was made using the Pygame library for game development and the NEAT library, which works
on the evolution of arbitrary neural networks. Inspired by the channel Tech with Tim.
Autor/Author: Matheus Henrique Kolln Nagildo
Última modificação/Last modification: 30/11/2019
"""

from typing import List
from entities.infra.base import Base
from entities.infra.bird import BIRD_IMGS, Bird
import pygame
import neat
import os

from entities.infra.pipe import PIPE_TOP_IMG, Pipe
from helpers.draw_window import draw_window


WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0

MAX_GEN = 50
SCORE_TO_STOP = 20


def main(gens: list, config: neat.config.Config) -> None:
    global GEN
    GEN += 1

    nets = []
    genomes = []
    birds = []
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()
    score = 0


    pygame.display.set_caption("Flappy Bird AI")
    pygame.display.set_icon(BIRD_IMGS[0])

    for _, genome in gens:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        genome.fitness = 0
        genomes.append(genome)

    while True:
        if should_stop(birds, GEN, score):
            break
        clock.tick(30)

        pipe_index = get_pipe_index(birds, pipes)

        for genome_index, bird in enumerate(birds):
            bird.move()
            genomes[genome_index].fitness += 0.1

            bird_location = bird.y
            pipe_top_location = bird.y - pipes[pipe_index].height
            pipe_bottom_location = bird.y - pipes[pipe_index].bottom

            result = nets[genome_index].activate(
                (
                    bird_location,
                    pipe_top_location,
                    pipe_bottom_location,
                )
            )[0]

            if should_jump(result):
                bird.jump()

        pipes_to_remove = []
        for pipe in pipes:
            for genome_index, bird in enumerate(birds):
                if pipe.collide(bird):
                    genomes[genome_index].fitness -= 1
                    birds.pop(genome_index)
                    nets.pop(genome_index)
                    genomes.pop(genome_index)

                if not pipe.passed and bird_passed_pipe(bird.x, pipe.x):
                    pipe.passed = True

                    score += 1
                    for g in genomes:
                        g.fitness += 5
                    pipes.append(Pipe(600))

            if should_remove_pipe(pipe.x):
                pipes_to_remove.append(pipe)

            pipe.move()

        for pipe_to_remove in pipes_to_remove:
            pipes.remove(pipe_to_remove)

        for genome_index, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(genome_index)
                nets.pop(genome_index)
                genomes.pop(genome_index)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)


def run(config_file: str) -> None:
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(show_species_detail=True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, 50)

    print("\nBest genome:\n{!s}".format(winner))


def should_stop(birds: List[Bird], gen: int, score: int) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return True

    return gen >= MAX_GEN or score >= SCORE_TO_STOP or len(birds) <= 0


def bird_passed_pipe(bird_x: float, pipe_x: float) -> bool:
    return bird_x > pipe_x


def should_remove_pipe(pipe_x: float) -> bool:
    return pipe_x + PIPE_TOP_IMG.get_width() < 0


def should_jump(result: float) -> bool:
    return result > 0.5


def get_pipe_index(birds: List[Bird], pipes: List[Pipe]) -> int:
    return (
        1
        if len(birds) > 0
        and len(pipes) > 1
        and birds[0].x > pipes[0].x + PIPE_TOP_IMG.get_width()
        else 0
    )


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
