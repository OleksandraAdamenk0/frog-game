import random
import pygame.display
from pygame.sprite import Sprite
from typing import List
from const import MAIN_SURFACE_SIZE
from tools import AnimatedImage, angel_to_vector, normalize_angle


class Enemy(Sprite):

    ENEMY_SCREEN_BORDERS = (-50, - 50, MAIN_SURFACE_SIZE[0] + 50, MAIN_SURFACE_SIZE[1] + 50)

    def __init__(self, images: list, x: int, y: int):
        Sprite.__init__(self)
        # animation
        self.__animated_image = AnimatedImage(images, 0.02, True)

        # image and rect for drawing all group in draw method from Sprite class
        self.image = self.__animated_image.get_frame()
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (x, y)

        # movement
        self.__speed: float = random.randint(1, 2) * 0.1
        self.__direction: float = 0.0
        self.__set_new_direction()

    def __move(self, delta_time: float) -> None:
        movement_vector = angel_to_vector(self.__direction)

        self.rect.x += movement_vector.x * (self.__speed * delta_time)

        # checking horizontal borders
        if self.rect.x <= Enemy.ENEMY_SCREEN_BORDERS[0] and movement_vector.x < 0:
            self.__set_custom_direction([135, 225])
        if self.rect.topright[0] >= Enemy.ENEMY_SCREEN_BORDERS[2] and movement_vector.x > 0:
            self.__set_custom_direction([135, 225])

        self.rect.y += movement_vector.y * self.__speed * delta_time

        # checking vertical borders
        if self.rect.y <= Enemy.ENEMY_SCREEN_BORDERS[1] and movement_vector.y < 0:
            self.__set_custom_direction([135, 225])
        if self.rect.bottomleft[1] >= Enemy.ENEMY_SCREEN_BORDERS[3] and movement_vector.y > 0:
            self.__set_custom_direction([135, 225])

    def __set_custom_direction(self, direction_range: List[int]) -> None:
        self.__direction += random.randrange(direction_range[0], direction_range[1], 10)
        self.__direction = normalize_angle(self.__direction)

    def __set_new_direction(self) -> None:
        self.__direction += random.randrange(10, 360, 10)
        self.__direction = normalize_angle(self.__direction)

    def __change_direction(self, delta_time: float) -> None:
        probability = int(1000 / delta_time * 4)
        random_num = random.randint(0, probability)
        if random_num == 0:
            self.__direction += random.randrange(10, 360, 10)
            self.__direction = normalize_angle(self.__direction)

    def update(self, delta_time: float) -> None:
        self.__animated_image.update(delta_time)
        self.image = self.__animated_image.get_frame()
        self.__change_direction(delta_time)
        self.__move(delta_time)
