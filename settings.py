import pygame
class Settings:

	def __init__(self):
		#Arena Settings
		self.window_width = 800
		self.window_height = 600
		self.bg_color = (246, 153, 66)
		self.bg_color = pygame.image.load("img/wolf.png")
		self.screen = pygame.display.set_mode([self.window_width, self.window_height])
		self.my_screen = self.screen.get_rect()

		#Ship Settings
		self.ship_speed = 2.5
		self.ship_life = 2

		#Bullets Settings
		self.bullet_speed = 2.5
		self.bullet_width = 4
		self.bullet_height = 12
		self.bullet_color = (0, 17, 174)

		#Ufo Settings
		self.ufo_speed = 1.0
		self.ufo_drop_speed = 30
		self.ufo_direction = 1 #1 ke kanan -1 ke kiri

	def blit_back(self):
		self.screen.blit(self.bg_color, [0,0])