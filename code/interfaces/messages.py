import pygame

image_0 = '../assets/map/messages/0.png'
image_1 = '../assets/map/messages/1.png'
image_2 = '../assets/map/messages/2.png'
image_coordinate = '../assets/map/messages/coordinate.png'
image_cute = '../assets/map/messages/cute.png'
image_path = '../assets/map/messages/path.png'
image_info = '../assets/map/messages/info.png'
image_suffer = '../assets/map/messages/suffer.png'
image_tolong = '../assets/map/messages/tolong.png'
image_tutorial = '../assets/map/messages/tutorial.png'
image_close = '../assets/map/messages/close.png'
image_diedie = '../assets/map/messages/diedie.png'
image_cold = '../assets/map/messages/cold.png'
image_lastclue = '../assets/map/messages/lastclue.png'
image_keepgoing = '../assets/map/messages/keepgoing.png'
image_goodbye = '../assets/map/messages/goodbye.png'

class Pesan: #enkapsulasi
    def draw(self, surface, path):
        self.__path = path
        self.__notes = pygame.image.load(self.__path).convert()
        surface.blit(self.__notes, (320, 180))