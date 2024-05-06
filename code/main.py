import pygame, sys
from config import *
from dungeon import Dungeon
from icedungeon import IceDungeon
from game_state_manager import GameState
from MenuSetting import *
from messages import *
from outside import OutsideDungeon

class Main:
    try: #penanganan kesalahan
        def __init__(self):
            pygame.init() 
            self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
            pygame.display.set_caption('unenlightened')
            self.clock = pygame.time.Clock()
            self.gameState = GameState('menu')
            self.Dungeon = Dungeon(self.gameState)
            self.IceDungeon = IceDungeon(self.gameState)
            self.menu = Menu('menu')
            self.menu_kematian = Menu_kematian('menu_kematian')
            self.pesan = Pesan()
            self.outside = OutsideDungeon(self.gameState)
            self.tamat = Menu_tamatan('menu_tamatan')

            self.states = {
                'Dungeon':self.Dungeon,
                'IceDungeon':self.IceDungeon,
                'menu': self.menu,
                'menu_kematian': self.menu_kematian,
                'outside': self.outside,
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
                        self.gameState.set_state('Dungeon')
                    if self.menu.exit_button.draw(self.screen): # Keluar dari program saat tombol exit ditekan
                        pygame.quit()
                        sys.exit()
                        
                if self.gameState.get_state() == 'menu_kematian':
                    self.states[self.gameState.get_state()].run()
                    if self.menu_kematian.retry_button.draw(self.screen):
                        self.gameState.set_state('Dungeon')
                    if self.menu_kematian.exit_button.draw(self.screen):
                        pygame.quit()
                        sys.exit()

                if self.gameState.get_state() == 'menu_tamatan':
                    self.states[self.gameState.get_state()].run()
                    if self.tamat.exit_button.draw(self.screen):
                        pygame.quit()
                        sys.exit()
                    
                if self.gameState.get_state() == 'Dungeon':
                    if self.Dungeon.player.rect.x == 704 and self.Dungeon.player.rect.y == 2670:
                        self.pesan.draw(self.screen, image_0)
                    if self.Dungeon.player.rect.x == 4864 and self.Dungeon.player.rect.y == 2962:
                        self.pesan.draw(self.screen, image_1)
                    if self.Dungeon.player.rect.x == 4160 and self.Dungeon.player.rect.y == 302:
                        self.pesan.draw(self.screen, image_2)
                    if self.Dungeon.player.rect.x == 192 and self.Dungeon.player.rect.y == 2670:
                        self.pesan.draw(self.screen, image_tutorial)
                    if (750 <= self.Dungeon.player.rect.x <= 800) and self.Dungeon.player.rect.y == 2798:
                        self.pesan.draw(self.screen, image_coordinate)
                    if (3812 <= self.Dungeon.player.rect.x <= 3863) and self.Dungeon.player.rect.y == 2734:
                        self.pesan.draw(self.screen, image_info)
                    if self.Dungeon.player.rect.x == 640 and self.Dungeon.player.rect.y == 174:
                        self.pesan.draw(self.screen, image_tolong)
                    if self.Dungeon.player.rect.x == 1024 and self.Dungeon.player.rect.y == 238:
                        self.pesan.draw(self.screen, image_close)
                    if self.Dungeon.player.rect.x == 4864 and self.Dungeon.player.rect.y == 2194:
                        self.pesan.draw(self.screen, image_suffer)
                    if self.Dungeon.raccoon1.healt <= 0 and  self.Dungeon.raccoon2.healt <= 0 and  self.Dungeon.raccoon3.healt <= 0:
                        if self.Dungeon.player.rect.x == 192 and self.Dungeon.player.rect.y == 174:
                            self.gameState.set_state('IceDungeon')
                        
                if self.gameState.get_state() == 'IceDungeon':
                    if self.IceDungeon.player.rect.x == 4672 and self.IceDungeon.player.rect.y == 366:
                        self.pesan.draw(self.screen, image_lastclue)
                    if self.IceDungeon.player.rect.x == 1134 and self.IceDungeon.player.rect.y == 283:
                        self.pesan.draw(self.screen, image_keepgoing)
                    if self.IceDungeon.player.rect.x == 4864 and self.IceDungeon.player.rect.y == 174:
                        self.pesan.draw(self.screen, image_diedie)
                    if self.IceDungeon.player.rect.x == 4160 and self.IceDungeon.player.rect.y == 2962:
                        self.pesan.draw(self.screen, image_cute)
                    if self.IceDungeon.player.rect.x == 3904 and self.IceDungeon.player.rect.y == 1134:
                        self.pesan.draw(self.screen, image_cold)
                    if self.IceDungeon.player.rect.x == 1856 and self.IceDungeon.player.rect.y == 2286:
                        self.pesan.draw(self.screen, image_path)
                    if self.IceDungeon.rakunmalas1.healt <= 0 and  self.IceDungeon.rakunmalas2.healt <= 0 and  self.IceDungeon.rakunmalas3.healt <= 0:
                        if (3968 <= self.IceDungeon.player.rect.x <= 4032) and (2676 <= self.IceDungeon.player.rect.y <= 2602):
                            self.gameState.set_state('outside')
                            
                if self.gameState.get_state() == 'outside':
                    if (2091 <= self.outside.player.rect.x <= 2164) and self.outside.player.rect.y == 1298:
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