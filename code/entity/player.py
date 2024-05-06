import pygame 
from settings.config_settings import *
from settings.extfunction import import_folder
from math import sin
from settings.game_state_manager import GameState
from entity.abstract import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups,obstacle_sprites)
        
        self.gameState = GameState('level')
        self.image = pygame.image.load('../assets/actor/MC/down_idle/idle_down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)

        # graphics setup
        self.import_graphics()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.14

        # movement sama dash
        self.direction = pygame.math.Vector2()
        self.dash_speed = 40
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.can_dash = True
        self.dash_cooldown = 1000
        self.dash_time = None
        self.dashing = False
        self.dash_duration = 40
        self.dash_timer_start = None
        self.dash_energy_consume = 10

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #stats
        self.stats = {'health': 100, 'energy': 100, 'attack': 10, 'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        
        #Durasi damage ke player
        self.eneble_get_atk = True
        self.hurt_time = None
        self.get_dmg_duration = 400

        #sound
        self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def import_graphics(self):
        character_path = '../assets/actor/MC/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
            'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def keybind(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack input 
            if keys[pygame.K_k] and not self.dashing and self.energy >=5:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
                if self.weapon_index == 0:
                    self.energy -= 5
                else:
                    self.energy -= 15

            #dash
            if keys[pygame.K_LSHIFT] and self.can_dash and 'idle' not in self.status and self.energy>=10:
                self.can_dash = False
                self.dashing = True
                self.dash_timer_start = pygame.time.get_ticks()
                self.dash_time = pygame.time.get_ticks()
                self.speed = self.dash_speed
                self.energy -= 10

            #switch weapon
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                    
                self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):

        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:       
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def koordinat(info,x,y,m,font):
        display_surface = pygame.display.get_surface()
        text_surf = font.render(str(f'{m}: {info}'),True,(255, 0, 0))
        text_rect = text_surf.get_rect(topleft = (x,y))
        pygame.draw.rect(display_surface,'Black',text_rect)
        display_surface.blit(text_surf,text_rect)

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if self.dashing:
            if current_time - self.dash_timer_start >= self.dash_duration:
                self.dashing = False
                self.speed = self.stats['speed']
        
        if not self.can_dash:
            if current_time - self.dash_time >= self.dash_cooldown:
                self.can_dash = True
                
        if not self.eneble_get_atk:
            if current_time - self.hurt_time >= self.get_dmg_duration:
                self.eneble_get_atk = True

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.eneble_get_atk:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_weapon_damage(self): # Mendapatkan total nilai damage dari weapon dan player #29/04/2024
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def energy_drop(self):
        if self.energy <= 100:
            self.energy += 0.08

    def update(self):
        self.keybind()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_drop()