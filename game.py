import random
from typing import List

import pygame

from const import *
from enemy import Enemy
from player import Player


def load_image(filename: str, image_name: str) -> pygame.Surface:
    try:
        image = pygame.image.load(filename)
        return image
    except FileNotFoundError:
        print(f"{image_name} image load error")
        pygame.quit()
        exit(-1)


def load_list_images(dirname: str, images_name: str, amount: int, scale_sizes=(0, 0)) -> List[pygame.Surface]:
    result = []
    if scale_sizes[0] != 0 and scale_sizes[1] != 0:
        for i in range(amount):
            result.append(pygame.transform.scale(load_image(f"{dirname}/{i}.png", images_name), scale_sizes))
    else:
        for i in range(amount):
            result.append(load_image(f"{dirname}/{i}.png", images_name))

    return result


class Game:
    def __init__(self):
        self.w = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        self.s = pygame.Surface((600, 400))
        pygame.display.set_caption("frog game")
        pygame.display.set_icon(pygame.image.load(LOGO_IMG))

        # game logic
        self.running = True
        self.hungry_bar = pygame.Rect(self.s.get_width() / 10, self.s.get_height() / 10, 200, 24)

        # background
        self.backgrounds = {
            "static_background": pygame.transform.scale(load_image(STATIC_BACKGROUND, "background"), self.s.get_size()),
            "first_branch": load_list_images(FIRST_BRANCH, "first_branch", 8, self.s.get_size()),
            "second_branch": load_list_images(SECOND_BRANCH, "second_branch", 8, self.s.get_size()),
            "third_branch": load_list_images(THIRD_BRANCH, "third_branch", 8, self.s.get_size())
        }
        self.is_animated = [False, False, False]
        self.background_frame = 0

        # enemys
        self.enemy_images = []
        self.__load_enemy_images()
        self.enemys = pygame.sprite.Group()
        for i in range(5):
            self.__add_enemy()

        # player
        self.player = Player(self.__load_player_images())

        self.clock = pygame.time.Clock()

    def __load_player_images(self):
        player_image = load_image(PLAYER_IMG, "player")
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

    def __create_more_enemies(self):
        if len(self.enemys) >= 10:
            return
        random_num = random.randint(1, 100)
        if random_num == 2:
            self.__add_enemy()

    def __update_background(self):
        self.background_frame += 0.15
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
                    self.player.active = True

    def __update(self):
        self.__update_background()
        self.enemys.update()
        self.player.update()
        self.player.check_enemies_collision(self.enemys)

        self.__create_more_enemies()

    def __draw_hungry_bar(self):
        if self.player.satiety > 0:
            surface = pygame.Surface((self.player.satiety, self.hungry_bar.height))
            surface.fill((60, 60, 90))
            self.s.blit(surface, self.hungry_bar.topleft)
        pygame.draw.rect(self.s, (25, 25, 40), self.hungry_bar, 4)

    def draw_background(self):
        self.s.blit(self.backgrounds.get("static_background"), (0, 0))

        ind = int(self.background_frame) if self.is_animated[FB_I] else 0
        self.s.blit(self.backgrounds.get("first_branch")[ind], (0, 0))

        ind = int(self.background_frame) if self.is_animated[SB_I] else 0
        self.s.blit(self.backgrounds.get("second_branch")[ind], (0, 0))

        ind = int(self.background_frame) if self.is_animated[TB_I] else 0
        self.s.blit(self.backgrounds.get("third_branch")[ind], (0, 0))


    def __draw(self):
        self.draw_background()
        self.enemys.draw(self.s)
        self.player.draw(self.s)
        self.__draw_hungry_bar()
        self.w.blit(pygame.transform.scale(self.s, self.w.get_size()), (0, 0))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.__event_loop()
            self.__update()
            self.__draw()
            self.clock.tick(60)
        pygame.quit()
        exit(0)
