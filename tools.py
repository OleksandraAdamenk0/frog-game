import math
import pygame
from pygame.math import Vector2 as Vector
from typing import List


def angel_to_vector(angel: float) -> Vector:
    angle_rad = math.radians(angel)
    return Vector(math.cos(angle_rad), math.sin(angle_rad))

def normalize_angle(angle: float) -> float:
    if angle > 360:
        return normalize_angle(angle - 360.0)
    if angle < 0:
        return normalize_angle(angle + 360.0)
    return angle


class AnimatedImage:

    INITIAL_FRAME_NUMBER = 0.0

    def __init__(self, images: List[pygame.Surface], increment: float, is_active=True):
        self.__frames: List[pygame.Surface] = images
        self.__current_frame: float = AnimatedImage.INITIAL_FRAME_NUMBER
        self.__increment: float = increment
        self.__is_active: bool = is_active

    def is_active(self) -> bool:
        return self.__is_active

    def set_active(self, is_active: bool):
        self.__is_active = is_active

    def get_frame(self) -> pygame.Surface:
        return self.__frames[int(self.__current_frame)]

    def get_current_frame_ind(self) -> float:
        return self.__current_frame

    def get_frame_rect(self) -> pygame.Rect:
        return self.__frames[int(self.__current_frame)].get_rect()

    def update(self, delta_time: float) -> None:
        if not self.__is_active:
            return
        self.__current_frame += self.__increment * delta_time
        if int(self.__current_frame) >= len(self.__frames):
            self.__current_frame = AnimatedImage.INITIAL_FRAME_NUMBER
