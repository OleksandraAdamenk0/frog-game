import random

import pygame.display
from pygame.sprite import Sprite
from pygame.rect import Rect
from pygame.math import Vector2 as Vector


class Enemy(Sprite):
    def __init__(self, images: list, x: int, y: int):
        Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]

        self.frame_amount = len(self.images)
        self.current_frame = 0

        self.rect: pygame.Rect = self.images[0].get_rect()
        self.rect.center = (x, y)

        self.direction = Vector(random.choice([-1, 1]), random.choice([-1, 1]))
        self.speed = random.randint(1, 2)

    def animation(self):
        self.current_frame += 0.3
        if self.current_frame >= self.frame_amount:
            self.current_frame = 0

        self.image = self.images[int(self.current_frame)]

    def move(self):
        self.rect.x += self.direction.x * self.speed
        if self.rect.x <= 0 and self.direction.x == -1:
            self.rect.x = 0
            self.direction.x = random.choice([1, 1])
        if self.rect.topright[0] >= 600 and self.direction.x == 1:
            self.rect.x = 600 - self.rect.width
            self.direction.x = random.choice([-1, -1])

        self.rect.y += self.direction.y * self.speed
        if self.rect.y <= 0 and self.direction.y == -1:
            self.rect.y = 0
            self.direction.y = random.choice([1, 1])
        if self.rect.bottomleft[1] >= 400 and self.direction.y == 1:
            self.rect.y = 400 - self.rect.height
            self.direction.y = random.choice([-1, -1])

    def change_direction(self):
        random_num = random.randint(1, 1000)
        if random_num == 2:
            # self.direction.x = random.choice([-1, 1])
            # self.direction.y = random.choice([-1, 1])
            self.direction.x = -self.direction.x
            self.direction.y = -self.direction.y

    def update(self):
        self.animation()
        self.change_direction()
        self.move()


