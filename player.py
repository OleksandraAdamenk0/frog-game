from typing import List

import pygame


class Player:
    def __init__(self, images: List[pygame.Surface]):
        self.satiety = 200
        self.hungry_counter = 0

        self.images = images
        self.image = self.images[0]

        self.frame_amount = len(self.images)
        self.current_frame = 0
        self.active = False
        self.active_frames_range = (4, 7)

        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 180
        self.tongue = pygame.Rect(self.rect.x + self.rect.width, self.rect.y + self.rect.height / 4, self.rect.width, self.rect.height / 2)

    def animation(self):
        if not self.active:
            return

        self.current_frame += 0.3
        if self.current_frame >= self.frame_amount:
            self.current_frame = 0
            self.active = False

        self.image = self.images[int(self.current_frame)]

        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def hungry(self):
        self.hungry_counter += 1
        if self.hungry_counter >= 120:
            self.hungry_counter = 0
            self.satiety -= 5

    def check_enemies_collision(self, enemies: pygame.sprite.Group):
        if not self.active or not (self.active_frames_range[0] < self.current_frame < self.active_frames_range[1]):
            return
        for enemy in enemies.sprites():
            if self.tongue.colliderect(enemy.rect):
                enemies.remove(enemy)
                self.satiety += 5
                if self.satiety > 200:
                    self.satiety = 200

    def update(self):
        self.animation()
        self.hungry()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
        # test = pygame.Surface((self.tongue.width, self.tongue.height))
        # test.fill("red")
        # surface.blit(test, self.tongue)
