import random
import pygame
from typing import List
from sys import exit
from const import *
from enemy import Enemy
from player import Player


def _load_image(filename: str, image_name: str) -> pygame.Surface:
    try:
        image = pygame.image.load(filename)
        return image
    except FileNotFoundError:
        print(f"{image_name} image load error")
        pygame.quit()
        exit(-1)


def _load_list_images(dirname: str, images_name: str, amount: int, scale_sizes=(0, 0)) -> List[pygame.Surface]:
    result = []
    if scale_sizes[0] != 0 and scale_sizes[1] != 0:
        for i in range(amount):
            result.append(pygame.transform.scale(_load_image(f"{dirname}/{i}.png", images_name), scale_sizes))
    else:
        for i in range(amount):
            result.append(_load_image(f"{dirname}/{i}.png", images_name))

    return result


def _load_player_images():
    player_image = _load_image(PLAYER_IMG, "player")
    player_images = [
        player_image.subsurface(pygame.Rect(0, 0, 32, 24)),
        player_image.subsurface(pygame.Rect(32, 0, 32, 24)),
        player_image.subsurface(pygame.Rect(64, 0, 32, 24)),
        player_image.subsurface(pygame.Rect(96, 0, 32, 24)),
        player_image.subsurface(pygame.Rect(128, 0, 32, 24)),
        player_image.subsurface(pygame.Rect(160, 0, 64, 24)),
        player_image.subsurface(pygame.Rect(224, 0, 64, 24)),
        player_image.subsurface(pygame.Rect(288, 0, 48, 24)),
        player_image.subsurface(pygame.Rect(336, 0, 32, 24)),
        player_image.subsurface(pygame.Rect(368, 0, 32, 24))
    ]
    for index, image in enumerate(player_images):
        player_images[index] = pygame.transform.scale(image, (image.get_size()[0] * 3, image.get_size()[1] * 3))
    return player_images


class Game:
    def __init__(self):
        self.w = pygame.display.set_mode((MAIN_SURFACE_SIZE[0], MAIN_SURFACE_SIZE[1]), pygame.RESIZABLE)
        self.s = pygame.Surface((MAIN_SURFACE_SIZE[0], MAIN_SURFACE_SIZE[1]))
        pygame.display.set_caption("frog game")
        pygame.display.set_icon(pygame.image.load(LOGO_IMG))

        # game logic
        self.running = True
        self.hungry_bar = pygame.Rect(self.s.get_width() / 10, self.s.get_height() / 10, 200, 24)

        # background
        self.backgrounds = {
            "static_background": pygame.transform.scale(_load_image(STATIC_BACKGROUND, "background"), self.s.get_size()),
            "first_branch": _load_list_images(FIRST_BRANCH, "first_branch", 8, self.s.get_size()),
            "second_branch": _load_list_images(SECOND_BRANCH, "second_branch", 8, self.s.get_size()),
            "third_branch": _load_list_images(THIRD_BRANCH, "third_branch", 8, self.s.get_size())
        }
        self.is_animated = [False, False, False]
        self.background_frame = 0

        # enemys
        self.enemy_images = []
        self.__load_enemy_images()
        self.enemys = pygame.sprite.Group()
        for i in range(INITIAL_ENEMIES_AMOUNT):
            self.__add_enemy()

        # player
        self.player = Player(_load_player_images())

        self.clock = pygame.time.Clock()

    def __load_enemy_images(self):
        try:
            enemy_animation_image = pygame.image.load("images/enemy.png")
        except FileNotFoundError:
            print("enemy image load error")
            pygame.quit()
            exit(-1)

        rect = pygame.Rect(0, 0, 7, 7)
        for i in range(8):
            rect.x = i * 7
            self.enemy_images.append(pygame.transform.scale(enemy_animation_image.subsurface(rect), (24, 24)))

    def __add_enemy(self):
        self.enemys.add(
            Enemy(self.enemy_images, random.randrange(0, self.s.get_width()), random.randrange(0, self.s.get_height())))

    def __create_more_enemies(self, delta_time: float):

        if len(self.enemys) >= 10:
            return
        min_num = min(int(delta_time), 100)
        max_num = max(int(delta_time), 100)
        random_num = random.randint(min_num, max_num)
        if random_num == min_num:
            self.__add_enemy()

    def __update_background(self, delta_time: float):
        self.background_frame += 0.009 * delta_time
        if self.background_frame >= 8:
            self.background_frame = 0
            self.is_animated[FB_I] = random.choice([True, False])
            self.is_animated[SB_I] = random.choice([True, False])
            self.is_animated[TB_I] = random.choice([True, False])

    def __event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.on_primary_action()

    def __update(self, delta_time: float):
        self.__update_background(delta_time)
        self.enemys.update(delta_time)
        self.player.update(delta_time)
        self.player.check_enemies_collision(self.enemys)

        self.__create_more_enemies(delta_time)

    def __draw_hungry_bar(self):
        if self.player.get_satiety() > 0:
            surface = pygame.Surface((self.player.get_satiety(), self.hungry_bar.height))
            surface.fill((60, 60, 90))
            self.s.blit(surface, self.hungry_bar.topleft)
        pygame.draw.rect(self.s, (25, 25, 40), self.hungry_bar, 4)

    def __draw_background(self):
        self.s.blit(self.backgrounds.get("static_background"), (0, 0))

        ind = int(self.background_frame) if self.is_animated[FB_I] else 0
        self.s.blit(self.backgrounds.get("first_branch")[ind], (0, 0))

        ind = int(self.background_frame) if self.is_animated[SB_I] else 0
        self.s.blit(self.backgrounds.get("second_branch")[ind], (0, 0))

        ind = int(self.background_frame) if self.is_animated[TB_I] else 0
        self.s.blit(self.backgrounds.get("third_branch")[ind], (0, 0))

    def __draw(self):
        self.__draw_background()
        self.player.draw(self.s)
        self.enemys.draw(self.s)
        self.__draw_hungry_bar()
        self.w.blit(pygame.transform.scale(self.s, self.w.get_size()), (0, 0))
        pygame.display.flip()

    def __draw_loading(self):
        self.s.fill((140, 170, 56))
        self.w.blit(pygame.transform.scale(self.s, self.w.get_size()), (0, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            fps: float = self.clock.get_fps()

            if fps == 0:
                self.__draw_loading()
                self.clock.tick(FPS)
                continue

            delta: float = 1000 / fps if (fps != 0) else 16
            self.__event_loop()
            self.__update(delta)
            self.__draw()
            self.clock.tick(FPS)

        pygame.quit()
        exit(0)
