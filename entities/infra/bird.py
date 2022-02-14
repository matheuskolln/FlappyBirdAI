import pygame
import os

from entities.domain.bird import IBird

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

MAX_POSSIBLE_IMAGE_INDEX = len(BIRD_IMGS) - 1

MAX_ROTATION = 25
ROTATION_SPEED = 20
ANIMATION_TIME = 5

SPEED_TO_DECREASE_WHEN_JUMP = -10.5


class Bird(IBird):

    inclination = 0
    tick_count = 0
    image_count = 0
    image = BIRD_IMGS[0]

    def __init__(self, x: float, y: float) -> None:
        self.speed = 0
        self.x = x
        self.y = y

    def jump(self) -> None:
        self.speed = SPEED_TO_DECREASE_WHEN_JUMP
        self.tick_count = 0

    def move(self) -> None:
        self.tick_count += 1
        displacement = self._manage_displacement()
        self.y = self.y + displacement
        self._manage_inclination(displacement)

    def draw(self, win) -> None:
        self.image_count += 1
        image_index = self._get_image_index()
        self.image = BIRD_IMGS[image_index]
        self._draw_image(win)

    def get_mask(self) -> pygame.mask.Mask:
        return pygame.mask.from_surface(self.image)

    def _get_displacement(self) -> float:
        displacement = self.speed * self.tick_count + 1.5 * self.tick_count**2
        return displacement

    def _manage_displacement(self) -> float:
        displacement = self._get_displacement()

        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement == 2

        return displacement

    def _manage_inclination(self, displacement: float) -> None:
        if displacement < 0 or self.y < self.y + 50 - displacement:
            if self.inclination < MAX_ROTATION:
                self.inclination = MAX_ROTATION
        else:
            if self.inclination > -90:
                self.inclination -= ROTATION_SPEED

    def _get_image_index(self) -> int:
        if self.inclination <= -80:
            self.image_count = ANIMATION_TIME * 2
            return 1

        intervals_for_image_count = [
            number for number in range(0, ANIMATION_TIME * 4, ANIMATION_TIME)
        ]

        format_index_to_image_index = (
            lambda index: index
            if index <= MAX_POSSIBLE_IMAGE_INDEX
            else index - MAX_POSSIBLE_IMAGE_INDEX
        )

        for index in range(0, len(intervals_for_image_count)):
            if self.image_count <= intervals_for_image_count[index]:
                return format_index_to_image_index(index)

        self.image_count = 0
        return 0

    def _draw_image(self, win) -> None:
        rotated_image = pygame.transform.rotate(self.image, self.inclination)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)
