from abc import ABC, abstractmethod
import pygame

class Entity(ABC, pygame.sprite.Sprite): #abstrak
    def __init__(self, groups, obstacle_sprites=None):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites
    
    @abstractmethod
    def import_graphics(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def collision(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def wave_value(self):
        pass

    @abstractmethod
    def animate(self):
        pass