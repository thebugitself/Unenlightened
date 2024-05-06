import  extmodul.Pygame_Lights as Pygame_Lights
import pygame
from pygame.locals import *


class Light:
    def __init__(self,screen,x=640,y=360,radius = 300,size=None,center=(0,0),intensity = 10):
        self.x = x
        if size is None:
            self.size = screen.get_size()
        else:
            self.size = size
        self.y = y
        self.intensity = intensity
        self.light = Pygame_Lights.LIGHT(radius, Pygame_Lights.pixel_shader(radius, (255,255,255),1,False))
        self.screen = screen
        self.center = center

    def render(self):
        mx = self.x
        my = self.y
        lights_display = pygame.Surface(self.size)
        lights_display.blit(Pygame_Lights.global_light(self.size, self.intensity), (0,0))
        self.light.main([], lights_display, mx-self.center[0], my-self.center[1])
        self.screen.blit(lights_display,self.center, special_flags=BLEND_RGB_MULT)