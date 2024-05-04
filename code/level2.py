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
from level import *

class Level2(Level):
    def __init__(self, gameStateManager):
        super().__init__(gameStateManager)
        pygame.init() 
        self.font = pygame.font.Font(None,30)
        # Tampilan layar
        self.display_surface = pygame.display.get_surface()
        
        # Camera
        self.visible_sprites = SortingCamera2()
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
            'boundary' : import_csv_layout('../graphics/map/csvFile/map_blocks.csv'),
            'topwall' : import_csv_layout('../graphics/map/csvFile/map_topwall.csv'),
            'entities': import_csv_layout('../graphics/map/csvFile/map_entity.csv') 
        }
        collide_surf = {
            'topwall' : import_folder('../graphics/map/topwall')
        }
        
        for style, layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')   
                        if style == 'topwall' :
                            surf = collide_surf['topwall'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'topwall', surf)
                        if style == 'entities' :
                            if col == '0':
                                self.player = Player((4864,876),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack)#Player
                            else:
                                if col == '1':
                                    self.rakunmalas1 = Enemy('rakunmalas',(4600,2700),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles)
                                    self.rakunmalas2 = Enemy('rakunmalas',(300,270),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles)
                                    self.rakunmalas3 = Enemy('rakunmalas',(4250,453),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles)
                                elif col == '2':
                                    nama_monster = 'bamboo'
                                elif col == '3':
                                    nama_monster = 'squid'
                                else:
                                    nama_monster = 'squid'
                                    
                                self.enemy = Enemy(nama_monster,(x,y),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles)
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.update()
        self.player_atk_logic()
        self.ui.display(self.player)
        self.draw_koordinat()

class SortingCamera2(SortingCamera):
    def __init__(self):
        super().__init__()

        self.__display_surface = pygame.display.get_surface()
        self.__half_width = self.__display_surface.get_size()[0] // 2
        self.__half_height = self.__display_surface.get_size()[1] // 2
        self.__offset = pygame.math.Vector2()
        
        #creating the floor
        self.__floor_surf = pygame.image.load('../graphics/map/ground/ground2.png').convert()
        self.__floor_rect = self.__floor_surf.get_rect(topleft = (0,0))
    
    def custom_draw(self,player):
        
        self.__offset.x = player.rect.centerx - self.__half_width
        self.__offset.y = player.rect.centery - self.__half_height

        #drawing the floor
        self.__display_surface.fill('#bbbbbb')
        floor_offset_pos = self.__floor_rect.topleft - self.__offset
        self.__display_surface.blit(self.__floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image,offset_pos)
            
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)