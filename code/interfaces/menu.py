import pygame
from settings.config_settings import Config
import random
from service.game_state_manager import *

class Menu:
    def __init__(self, gameStateManager):
        self.screen = pygame.display.set_mode((Config.WIDTH,Config.HEIGTH))
        self.bg = BackGround(0, 0, '../assets/menu/BgMenu1.jpeg', 1)
        self.title = Title(40, 50, '../assets/menu/Title_4.png', 760, 100)
        self.start_button = Button(30, 300, '../assets/menu/start_btn.png', 0.8)
        self.exit_button = Button(30, 450, '../assets/menu/exit_btn.png', 0.8)
        self.daun = Daun(Config.WIDTH, Config.HEIGTH)
        self.gameStateManager = gameStateManager

    def run(self):
        self.bg.draw(self.screen)
        self.title.draw(self.screen)
        self.daun.update()
        self.daun.draw(self.screen)
        
class Menu_kematian(Menu): #penerapan inheritance
    def __init__(self, gameStateManager):
        super().__init__(gameStateManager)
        self.screen = pygame.display.set_mode((Config.WIDTH,Config.HEIGTH))
        self.retry_button = Button(555, 350, '../assets/menu/Revive_btn.png', 0.215)
        self.exit_button = Button(555, 460, '../assets/menu/exit_btn.png', 0.8)
        self.bg_mati = Title(500, 100, '../assets/menu/Bg_menu_mati2.png', 300, 500) #Kenapa pake Title karena fungsinya sama
        
    def run(self): #penerapan polimorfisme
        self.bg_mati.draw(self.screen)
        
class Menu_pause(Menu):
    def __init__(self, gameStateManager):
        super().__init__(gameStateManager)
        self.screen = pygame.display.set_mode((Config.WIDTH,Config.HEIGTH))
        self.exit_button = Button(555, 409, '../assets/menu/exit_btn.png', 0.8)
        self.bg_mati = BackGround(320, 200, '../assets/menu/Bg_Pause_menu.png', 0.5)
    
    def run(self): #penerapan polimorfisme
        self.bg_mati.draw(self.screen)

class Menu_tamatan(Menu): #penerapan inheritance
    def __init__(self, gameStateManager):
        super().__init__(gameStateManager)
        self.screen = pygame.display.set_mode((Config.WIDTH,Config.HEIGTH))
        self.note_tamat_dapat_A = BackGround(0, 0, '../assets/map/messages/goodbye.png', 1) #Kenapa pake Title karena fungsinya sama
        self.exit_button = Button(1100, 60, '../assets/menu/exit.png', 1)
        
    def run(self): #penerapan polimorfisme
        self.note_tamat_dapat_A.draw(self.screen)


class Button():
    def __init__(self, x, y, file_name, scale):
        self.file_name = file_name
        self.image = pygame.image.load(self.file_name).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self, surface):
        self.surface = surface
        self.action = False
        self.pos = pygame.mouse.get_pos() # mengambil data posisi mouse
        
        if self.rect.collidepoint(self.pos): #mengecek status mouse
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        return self.action

class BackGround():
    def __init__(self, x, y, file_name, scale):
        self.image = pygame.transform.scale(pygame.image.load(file_name).convert_alpha(), (int(Config.WIDTH * scale), int(Config.HEIGTH * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
    def draw(self, surface):
        self.surface = surface
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
  

class Title():
    def __init__(self, x, y, file_name, width, height):
        self.image = pygame.transform.scale(pygame.image.load(file_name).convert_alpha(), (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
  
    def draw(self, surface):
        self.surface = surface
        self.surface.blit(self.image, (self.rect.x, self.rect.y))


class Daun:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.daun_image = pygame.image.load('../assets/menu/daun.png').convert_alpha()
        self.daun_list = []
        self.generate_daun()

    def generate_daun(self):
        for _ in range(10):
            self.size = random.randint(40, 70)
            self.speed = random.randint(1, 5)
            self.x = random.randint(0, self.screen_width)
            self.y = random.randint(-150, -50)
            self.daun_list.append({"image": pygame.transform.scale(self.daun_image, (self.size, self.size)),
                                   "rect": pygame.Rect(self.x, self.y, self.size, self.size),
                                   "speed": self.speed})

    def update(self):
        for self.daun in self.daun_list:
            self.daun["rect"].y += self.daun["speed"]
            if self.daun["rect"].y > self.screen_height:
                self.daun["rect"].y = random.randint(-100, -50)
                self.daun["rect"].x = random.randint(0, self.screen_width)

    def draw(self, screen):
        self.screen = screen
        for self.daun in self.daun_list:
            self.screen.blit(self.daun["image"], self.daun["rect"])