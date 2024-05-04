import pygame, sys
from config import *
from tile import Tile
from player import Player
from weapon import Weapon
from extfunction import *
from enemy import Enemy
from ui import UI
from particles import AnimationPlayer
from random import choice, randint
from level import SortingCamera

class Island:
    def __init__(self, gameStateManager):
        pygame.init() 
        self.font = pygame.font.Font(None,30)
        # Tampilan layar
        self.gameStateManager = gameStateManager
        self.display_surface = pygame.display.get_surface()
        
        # Camera
        self.visible_sprites = SortingCamera3()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # Setup attack 
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group() #sprite senjata dan logic
        self.attackable_sprites = pygame.sprite.Group() #sprite musuh. mengecek 2 collision  atk dan atkable
        
        #Setup Map dan Enemy
        self.startup = True
        self.create_map()
        
        # user interface
        self.ui = UI()

        #particles
        self.animation_player = AnimationPlayer()
     
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('../graphics/map/island/CSVfile/map_blocks.csv'),
        }
        
        for style, layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')   
        self.player = Player((1024, 632),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack)
        
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites]) 

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def draw_koordinat(self):
        Player.koordinat(self.player.rect.x,1120,10,'x',self.font)
        Player.koordinat(self.player.rect.y,1200,10,'y',self.font)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)
        self.draw_koordinat()


class SortingCamera3(SortingCamera):
    def __init__(self):
        super().__init__()
    
        self.__display_surface = pygame.display.get_surface()
        self.__half_width = self.__display_surface.get_size()[0] // 2
        self.__half_height = self.__display_surface.get_size()[1] // 2
        self.__offset = pygame.math.Vector2()
        
        self.__floor_surf = pygame.image.load('../graphics/map/island/ground.png').convert()
        self.__floor_rect = self.__floor_surf.get_rect(topleft = (0,0))
    
    def custom_draw(self,player):
        
        self.__offset.x = player.rect.centerx - self.__half_width
        self.__offset.y = player.rect.centery - self.__half_height

        self.__display_surface.fill('#71ddee')
        floor_offset_pos = self.__floor_rect.topleft - self.__offset
        self.__display_surface.blit(self.__floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image,offset_pos)