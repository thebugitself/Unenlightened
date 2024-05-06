import pygame
from settings.config_settings import * 

class UI:
	def __init__(self):
		
		# general
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(Config.UI_FONT,Config.UI_FONT_SIZE)

		# bar setup
		self.health_bar_rect = pygame.Rect(10,10,Config.HEALTH_BAR_WIDTH,Config.BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,Config.ENERGY_BAR_WIDTH,Config.BAR_HEIGHT)

		# convert weapon dictionary
		self.weapon_graphics = []
		for weapon in Config.weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

	def show_bar(self,current,max_amount,bg_rect,color):
		# draw bg
		pygame.draw.rect(self.display_surface,Config.UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# drawing the bar
		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,Config.UI_BORDER_COLOR,bg_rect,3)

	def selection_box(self,left,top,has_switched):
		bg_rect = pygame.Rect(left,top,Config.ITEM_BOX_SIZE,Config.ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface,Config.UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.display_surface,Config.UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.display_surface,Config.UI_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched) 
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf,weapon_rect)

	def display(self,player):
		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,Config.HEALTH_COLOR)
		self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,Config.ENERGY_COLOR)
		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)