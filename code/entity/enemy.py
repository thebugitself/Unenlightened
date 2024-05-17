from typing import Any
import pygame 
from settings.config_settings import *
from settings.extfunction import import_folder
from math import sin 
from settings.abstract import Entity

class Enemy(Entity): #inheritance
    def __init__(self,nama_monster,pos,groups,obstacle_sprites,damage_player,trigger_death_particles, health):
        super().__init__(groups,obstacle_sprites)
        self.sprite_type = 'enemy'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2(0, 0)
        
        self.import_graphics(nama_monster)
        self.status = 'idle'
        self.image = self.animation[self.status][self.frame_index]
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        
        self.nama_monster = nama_monster
        monster_info = Config.Enemy_Data[self.nama_monster]
        self.health = health
        self.attack_damage = monster_info['damage']
        self.deffend = monster_info['deffend']
        self.speed = monster_info['speed']
        self.atk_radius = monster_info['atk_radius']
        self.ntc_radius = monster_info['ntc_radius']
        self.atk_type = monster_info['attack_type']

        self.eneble_atk = True
        self.atk_cooldown = 1500
        self.attack_time = None
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        
        self.hit_time = None
        self.get_dmg_duration = 350
        self.eneble_get_atk = True

        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.05)
        self.attack_sound.set_volume(0.3)
    
    def import_graphics(self, nama):
        self.animation = {'idle':[], 'move':[],'attack':[]}
        main_path = f'../assets/actor/Enemy/monsters/{nama}/'
        
        for animation in self.animation.keys():
            self.animation[animation] = import_folder(main_path + animation)

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self,direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        
    def get_position_player(self, player): # mendapatkan nilai jarak enemy player dan arah enemy
        enemy_position = pygame.math.Vector2(self.rect.center) # nilai koordinat (x,y) enemy
        player_position = pygame.math.Vector2(player.rect.center) # nilai koordinat (x,y) player
        distance = (player_position - enemy_position).magnitude() # Menghitung jarak enemy - player. #Fungsi magnitude mengkonversi nilai vektor ke bilangan b 
        
        if distance > 0:
            direction = (player_position - enemy_position).normalize() 
        else:
            direction = pygame.math.Vector2()
        
        return (distance, direction)
                        
    def get_status(self, player):
        distance = self.get_position_player(player)[0]
        
        if distance <= self.atk_radius and self.eneble_atk == True: #Jarak jangkauan serangan enemy ke player
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.ntc_radius: #Jarak pandang enemy
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def actions(self, player): #tindakan enemy
        if self.status == 'attack' and self.eneble_atk == True:
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.atk_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_position_player(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
           
    def animate(self):
        animation = self.animation[self.status]
        self.frame_index = self.frame_index + self.animation_speed
        
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.eneble_atk = False
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.eneble_get_atk:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def cooldown_enemy_attack(self):
        current_time = pygame.time.get_ticks()
        if not self.eneble_atk:
            if current_time - self.attack_time >= self.atk_cooldown:
                self.eneble_atk = True
                
        if not self.eneble_get_atk:
            if current_time - self.hit_time >= self.get_dmg_duration:
                self.eneble_get_atk = True
    
    def get_damage(self, player): #Mengurangi darah musuh
        if self.eneble_get_atk:
            self.hit_sound.play()
            self.direction = self.get_position_player(player)[1]
            self.health = self.health - player.get_weapon_damage()
            self.hit_time = pygame.time.get_ticks()
            self.eneble_get_atk = False
    
    def death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.nama_monster)
            self.death_sound.play()
        
    def hit_reaction(self):
        if not self.eneble_get_atk:
            self.direction *= -self.deffend
    
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown_enemy_attack()
        self.death()
        
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)