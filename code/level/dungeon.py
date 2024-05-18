import pygame
from settings.config_settings import Config
from interfaces.tile import Tile
from entity.player import Player
from interfaces.weapon import Weapon
from settings.extfunction import *
from entity.enemy import Enemy
from interfaces.ui import UI
from interfaces.particles import AnimationPlayer
from random import randint
from extmodul.game_light import Light
from service.save_load_manager import SaveLoadManager

class Dungeon:
    def __init__(self, gameStateManager):
        pygame.init()
        #init
        self.save_load_manager = SaveLoadManager(".save","save_data")
        
        self.font = pygame.font.Font(None,30)
        # Tampilan layar
        self.gameStateManager = gameStateManager
        self.display_surface = pygame.display.get_surface()
        
        # Camera
        self.visible_sprites = SortingCamera()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # Setup attack 
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group() #sprite senjata dan logic
        self.attackable_sprites = pygame.sprite.Group() #sprite musuh. mengecek 2 collision  atk dan atkable
        
        #Setup Map dan Enemy
        self.create_map()
        
        # user interface
        self.ui = UI()

        #particles
        self.animation_player = AnimationPlayer()
        #other
        
    
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('../assets/map/csvFile/map_blocks.csv'),
            'topwall' : import_csv_layout('../assets/map/csvFile/map_topwall.csv'),
            'entities': import_csv_layout('../assets/map/csvFile/map_entity.csv') 
        }
        collide_surf = {
            'topwall' : import_folder('../assets/map/topwall')
        }
        
        self.initial_spawn = self.load_player_location()
        self.rakun1_health = self.load_raccoon_health('1')
        self.rakun2_health = self.load_raccoon_health('2')
        self.rakun3_health = self.load_raccoon_health('3')

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
                                
                                self.player = Player(self.initial_spawn,[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack)#Player
                            else:
                                if col == '1':
                                    self.raccoon1 = Enemy('raccoon',(4600,2700),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, self.rakun1_health)
                                    self.raccoon2 = Enemy('raccoon',(300,270),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, self.rakun2_health)
                                    self.raccoon3 = Enemy('raccoon',(4250,453),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, self.rakun3_health)
                                elif col == '2':
                                    nama_monster = 'spirit'
                                elif col == '3':
                                    nama_monster = 'bamboo' 
                                else:
                                    nama_monster = 'spirit'

                                self.enemy = Enemy(nama_monster,(x,y),[self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_to_player, self.trigger_death_particles, 300)
        
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites]) 

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_atk_logic(self): # Baru 30/04/2024
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':#???
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):#???
                                self.animation_player.create_grass_particles(pos-offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player)
                        
    def damage_to_player(self, damage, attack_type):
        if not self.player.health <= 0:
            if self.player.eneble_get_atk:
                self.player.health = self.player.health - damage
                self.player.eneble_get_atk = False
                self.player.hurt_time = pygame.time.get_ticks()
                self.animation_player.create_particles(attack_type, self.player.rect.center, self.visible_sprites)
        else:
            self.gameStateManager.set_state('menu_kematian')
            self.player.kill()
            self.player.destroy_attack()
            self.player = Player((4000,2632),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack)
                    
    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)
    
    def draw_koordinat(self):
        Player.koordinat(self.player.rect.x,1120,10,'x',self.font)
        Player.koordinat(self.player.rect.y,1200,10,'y',self.font)

    def save_player_location(self):
        player_pos = f"{self.player.rect.x}:{self.player.rect.y}:Dungeon:{self.raccoon1.health}:{self.raccoon2.health}:{self.raccoon3.health}"
        self.save_load_manager.save_data(player_pos,Config.SAVE_DUNGEON)

    def load_player_location(self):
        player_pos = self.save_load_manager.load_data(Config.SAVE_DUNGEON)
        if player_pos:
            player_pos =( int(player_pos.split(":")[0]), int(player_pos.split(":")[1]))
            return player_pos
        return (197,2788)
    
    def load_raccoon_health(self, rakun):
        health = self.save_load_manager.load_data(Config.SAVE_DUNGEON)
        if rakun == '1':
            if health:
                health = (int(health.split(":")[3]))
                return health
            return 800
        elif rakun == '2':
            if health:
                health = (int(health.split(":")[4]))
                return health
            return 800
        elif rakun == '3':
            if health:
                health = (int(health.split(":")[5]))
                return health
            return 800
    
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.update()
        self.player_atk_logic()
        Light(self.display_surface).render()
        self.ui.display(self.player)
        self.draw_koordinat()

#penerapan enkapsulasi untuk cameranya
class SortingCamera(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__half_width = self.__display_surface.get_size()[0] // 2
        self.__half_height = self.__display_surface.get_size()[1] // 2
        self.__offset = pygame.math.Vector2()
        
        self.__floor_surf = pygame.image.load('../assets/map/ground/ground.png').convert()
        self.__floor_rect = self.__floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self,player):
        
        self.__offset.x = player.rect.centerx - self.__half_width
        self.__offset.y = player.rect.centery - self.__half_height

        self.__display_surface.fill('#222222')
        
        floor_offset_pos = self.__floor_rect.topleft - self.__offset
        self.__display_surface.blit(self.__floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.__offset
            self.__display_surface.blit(sprite.image,offset_pos)
            
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)