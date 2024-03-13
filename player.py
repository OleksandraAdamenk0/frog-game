import pygame
from typing import List
from tools import AnimatedImage
from const import MAX_PLAYER_SATIETY


class Player:
    def __init__(self, images: List[pygame.Surface]):
        self.__satiety = MAX_PLAYER_SATIETY
        self.__active_frames_range = (4, 7)
        self.__image = AnimatedImage(images, 0.02, False)

        self.__rect = self.__image.get_frame_rect()
        self.__rect.x = 200
        self.__rect.y = 180
        self.__tongue = pygame.Rect(self.__rect.x + self.__rect.width, self.__rect.y + self.__rect.height / 4, self.__rect.width, self.__rect.height / 2)

    def get_satiety(self):
        return self.__satiety

    def __update_rect(self):
        pos = self.__rect.topleft
        self.__rect = self.__image.get_frame_rect()
        self.__rect.x = pos[0]
        self.__rect.y = pos[1]

    def __animation(self, delta_time: float):
        if not self.__image.is_active():
            return

        self.__image.update(delta_time)
        if self.__image.get_current_frame_ind() == AnimatedImage.INITIAL_FRAME_NUMBER:
            self.__image.set_active(False)
        self.__update_rect()

    def __hunger(self, delta_time: float):
        self.__satiety -= 2 / (1000 / delta_time)

    def on_primary_action(self):
        self.__image.set_active(True)

    def check_enemies_collision(self, enemies: pygame.sprite.Group):
        if not self.__image.is_active() or not (self.__active_frames_range[0] < self.__image.get_current_frame_ind() < self.__active_frames_range[1]):
            return
        for enemy in enemies.sprites():
            if not self.__tongue.colliderect(enemy.rect):
                continue
            enemies.remove(enemy)
            self.__satiety += 5
            if self.__satiety > MAX_PLAYER_SATIETY:
                self.__satiety = MAX_PLAYER_SATIETY

    def update(self, delta_time: float):
        self.__animation(delta_time)
        self.__hunger(delta_time)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.__image.get_frame(), self.__rect)
        # test = pygame.Surface((self.tongue.width, self.tongue.height))
        # test.fill("red")
        # surface.blit(test, self.tongue)
