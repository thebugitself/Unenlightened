import pygame
from settings.config_settings import Config
from interfaces.tile import Tile
from entity.player import Player
from settings.extfunction import *
from entity.enemy import Enemy
from interfaces.ui import UI
from interfaces.particles import AnimationPlayer
from random import choice, randint
from level.dungeon import *

class IceDungeon(Dungeon): #inheritance
    def __init__(self, gameStateManager):
        pygame.init()
        super().__init__(gameStateManager)

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
        
     
    def create_map(self): #polimorfisme
        layouts = {
            'boundary' : import_csv_layout('../assets/map/csvFile/map_blocks.csv'),
            'topwall' : import_csv_layout('../assets/map/csvFile/map_topwall.csv'),
            'entities': import_csv_layout('../assets/map/csvFile/map_entity.csv') 
        }
        collide_surf = {
            'topwall' : import_folder('../assets/map/topwall')
        }
        self.initial_spawn2 = self.load_player_location()
        self.malas1_health = self.load_rakunmalas_health('1')
        self.malas2_health = self.load_rakunmalas_health('2')
        self.malas3_health = self.load_rakunmalas_health('3')
        
        for style, layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * Config.TILESIZE
                        y = row_index * Config.TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')   
                        if style == 'topwall' :
                            surf = collide_surf['topwall'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'topwall', surf)
                        if style == 'entities' :
                            if col == '0':
                                self.player = Player(self.initial_spawn2,[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack)#Player
                            else:
                                if col == '1':
                                    self.rakunmalas1 = Enemy('rakunmalas',(4600,2700),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, self.malas1_health)
                                    self.rakunmalas2 = Enemy('rakunmalas',(504,2750),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, self.malas2_health)
                                    self.rakunmalas3 = Enemy('rakunmalas',(4250,453),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, self.malas3_health)
                                elif col == '2':
                                    nama_monster = 'bamboo'
                                elif col == '3':
                                    nama_monster = 'squid'
                                else:
                                    nama_monster = 'squid'
                                    
                                self.enemy = Enemy(nama_monster,(x,y),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, 600)
    
    def save_player_location(self):#polimorfisme
        player_pos = f"{self.player.rect.x}:{self.player.rect.y}:IceDungeon:{self.rakunmalas1.health}:{self.rakunmalas2.health}:{self.rakunmalas3.health}"
        self.save_load_manager.save_data(player_pos,Config.SAVE_ICEDUNGEON)

    def load_player_location(self):#polimorfisme
        player_pos = self.save_load_manager.load_data(Config.SAVE_ICEDUNGEON)
        if player_pos:
            player_pos =( int(player_pos.split(":")[0]), int(player_pos.split(":")[1]))
            return player_pos
        return (4864,876)
    
    def load_rakunmalas_health(self, rakun):
        health = self.save_load_manager.load_data(Config.SAVE_ICEDUNGEON)
        if rakun == '1':
            if health:
                health = (int(health.split(":")[3]))
                return health
            return 1600
        elif rakun == '2':
            if health:
                health = (int(health.split(":")[4]))
                return health
            return 1600
        elif rakun == '3':
            if health:
                health = (int(health.split(":")[5]))
                return health
            return 1600

    def run(self): #polimorfisme
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)
        self.draw_koordinat()
        self.visible_sprites.update()
        self.player_atk_logic()
        

class SortingCamera2(SortingCamera): #inheritance
    def __init__(self):
        super().__init__()

        self.__display_surface = pygame.display.get_surface()
        self.__half_width = self.__display_surface.get_size()[0] // 2
        self.__half_height = self.__display_surface.get_size()[1] // 2
        self.__offset = pygame.math.Vector2()
        
        self.__floor_surf = pygame.image.load('../assets/map/ground/ground2.png').convert()
        self.__floor_rect = self.__floor_surf.get_rect(topleft = (0,0))
    
    def custom_draw(self,player): #polimorfisme
        
        self.__offset.x = player.rect.centerx - self.__half_width
        self.__offset.y = player.rect.centery - self.__half_height

        self.__display_surface.fill('#bbbbbb')

        floor_offset_pos = self.__floor_rect.topleft - self.__offset
        self.__display_surface.blit(self.__floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image,offset_pos)