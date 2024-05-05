import pygame, sys
from config import *
from level import Level
from level2 import Level2
from game_state_manager import GameState
from MenuSetting import *
from messages import *
from lastmap import Island

class Main:
    try:
        def __init__(self):
            pygame.init() 
            self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
            pygame.display.set_caption('unenlightened')
            self.clock = pygame.time.Clock()
            self.gameState = GameState('menu')
            self.level = Level(self.gameState)
            self.level2 = Level2(self.gameState)
            self.menu = Menu('menu')
            self.menu_kematian = Menu_kematian('menu_kematian')
            self.pesan = Pesan()
            self.island = Island(self.gameState)
            self.tamat = Menu_tamatan('menu_tamatan')

            self.states = {
                'level':self.level,
                'level2':self.level2,
                'menu': self.menu,
                'menu_kematian': self.menu_kematian,
                'island': self.island,
                'menu_tamatan' :self.tamat
            }

            #main sound
            main_sound = pygame.mixer.Sound('../audio/main.ogg')
            main_sound.play(loops = -1)

        def run(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                self.states[self.gameState.get_state()].run()
                if self.gameState.get_state() == 'menu':
                    if self.menu.start_button.draw(self.screen): # Mengubah status ketika tombol start ditekan wwww
                        self.gameState.set_state('level')
                    if self.menu.exit_button.draw(self.screen): # Keluar dari program saat tombol exit ditekan
                        pygame.quit()
                        sys.exit()
                        
                if self.gameState.get_state() == 'menu_kematian':
                    self.states[self.gameState.get_state()].run()
                    if self.menu_kematian.retry_button.draw(self.screen):
                        self.gameState.set_state('level')
                    if self.menu_kematian.exit_button.draw(self.screen):
                        pygame.quit()
                        sys.exit()

                if self.gameState.get_state() == 'menu_tamatan':
                    self.states[self.gameState.get_state()].run()
                    if self.tamat.exit_button.draw(self.screen):
                        pygame.quit()
                        sys.exit()
                    
                if self.gameState.get_state() == 'level':
                    if self.level.player.rect.x == 704 and self.level.player.rect.y == 2670:
                        self.pesan.draw(self.screen, image_0)
                    if self.level.player.rect.x == 4864 and self.level.player.rect.y == 2962:
                        self.pesan.draw(self.screen, image_1)
                    if self.level.player.rect.x == 4160 and self.level.player.rect.y == 302:
                        self.pesan.draw(self.screen, image_2)
                    if self.level.player.rect.x == 192 and self.level.player.rect.y == 2670:
                        self.pesan.draw(self.screen, image_tutorial)
                    if (750 <= self.level.player.rect.x <= 800) and self.level.player.rect.y == 2798:
                        self.pesan.draw(self.screen, image_coordinate)
                    if (3812 <= self.level.player.rect.x <= 3863) and self.level.player.rect.y == 2734:
                        self.pesan.draw(self.screen, image_info)
                    if self.level.player.rect.x == 640 and self.level.player.rect.y == 174:
                        self.pesan.draw(self.screen, image_tolong)
                    if self.level.player.rect.x == 1024 and self.level.player.rect.y == 238:
                        self.pesan.draw(self.screen, image_close)
                    if self.level.player.rect.x == 4864 and self.level.player.rect.y == 2194:
                        self.pesan.draw(self.screen, image_suffer)
                    if self.level.raccoon1.healt <= 0 and  self.level.raccoon2.healt <= 0 and  self.level.raccoon3.healt <= 0:
                        if self.level.player.rect.x == 192 and self.level.player.rect.y == 174:
                            self.gameState.set_state('level2')
                        
                if self.gameState.get_state() == 'level2':
                    if self.level2.player.rect.x == 4672 and self.level2.player.rect.y == 366:
                        self.pesan.draw(self.screen, image_lastclue)
                    if self.level2.player.rect.x == 1134 and self.level2.player.rect.y == 283:
                        self.pesan.draw(self.screen, image_keepgoing)
                    if self.level2.player.rect.x == 4864 and self.level2.player.rect.y == 174:
                        self.pesan.draw(self.screen, image_diedie)
                    if self.level2.player.rect.x == 4160 and self.level2.player.rect.y == 2962:
                        self.pesan.draw(self.screen, image_cute)
                    if self.level2.player.rect.x == 3904 and self.level2.player.rect.y == 1134:
                        self.pesan.draw(self.screen, image_cold)
                    if self.level2.player.rect.x == 1856 and self.level2.player.rect.y == 2286:
                        self.pesan.draw(self.screen, image_path)
                    if self.level2.rakunmalas1.healt <= 0 and  self.level2.rakunmalas2.healt <= 0 and  self.level2.rakunmalas3.healt <= 0:
                        if (3968 <= self.level2.player.rect.x <= 4032) and (2676 <= self.level2.player.rect.y <= 2602):
                            self.gameState.set_state('island')
                            
                if self.gameState.get_state() == 'island':
                    if (2091 <= self.island.player.rect.x <= 2164) and self.island.player.rect.y == 1298:
                        self.gameState.set_state('menu_tamatan')  
                pygame.display.update()
                self.clock.tick(FPS)

    except pygame.error as e:
        print('pygame error:', e)
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    loop = Main()
    loop.run()