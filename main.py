import pygame
import sys
import random
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from ufo import Ufo 
from star import Star
from game_stats import GameStats

class AlienWorld:

	def __init__(self):
		pygame.init()
		self.my_settings = Settings()

		self.error = False
		self.screen = pygame.display.set_mode([self.my_settings.window_width, self.my_settings.window_height])
		#self.screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
		self.title = pygame.display.set_caption("Game ALIEN")
		self.bg_color = self.my_settings.bg_color

		self.my_ship = Ship(self)
		self.bullets = pygame.sprite.Group() #container for bullet
		self.ufo_army = pygame.sprite.Group()
		self.my_stars = pygame.sprite.Group()
		self.my_stats = GameStats(self)


		self.create_ufo_army()
		self.create_my_stars()

	def run_game(self):
		while not self.error:
			self.check_events() #refactoring
			self.update_ship()
			self.bullets.update()
			self.update_ufo()
			self.update_frame() #refactoring
			self.update_bullet()

	def check_events(self):
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					#sys.exit()
					self.error = True

				elif event.type == pygame.KEYDOWN:
					self.check_keydown_event(event)

				elif event.type == pygame.KEYUP:
					self.check_keyup_event(event)

	def check_keydown_event(self, event):
		if event.key == pygame.K_w: #forward
			self.my_ship.moving_up = True
		elif event.key == pygame.K_s: #backward
			self.my_ship.moving_down = True
		elif event.key == pygame.K_d: #right
			self.my_ship.moving_right = True
		elif event.key == pygame.K_a: #left
			self.my_ship.moving_left = True
		elif event.key == pygame.K_q:
			self.error = True
		elif event.key == pygame.K_SPACE: #fire!
			self.fire_bullet()
		elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_RCTRL:
			self.screen = pygame.display.set_mode([0,0], pygame.FULLSCREEN)
		elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_SHIFT:
			self.screen = pygame.display.set_mode([self.my_settings.window_width, self.my_settings.window_height])

	def check_keyup_event(self, event):
		if event.key == pygame.K_w:
			self.my_ship.moving_up = False
		elif event.key == pygame.K_s:
			self.my_ship.moving_down = False
		elif event.key == pygame.K_d:
			self.my_ship.moving_right = False
		elif event.key == pygame.K_a:
			self.my_ship.moving_left = False

	def fire_bullet(self):
		if len(self.bullets) <= 10:#ini 					
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def update_ship(self):
		self.my_ship.update() #piloting ship

		if pygame.sprite.spritecollideany(self.my_ship, self.ufo_army):
			#print("Kapal Menabrak Ufo!")
			self.ship_hit()

	def ship_hit(self):
		self.my_stats.ship_life -= 1

		self.ufo_army.empty()
		self.bullets.empty()

		self.create_ufo_army()
		self.my_ship.re_position_ship() #set ulang posisi

		sleep(0.5)

	def update_bullet(self):
		self.bullets.update()
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
			#print(len(self.bullets))
		self.check_bullet_ufo_collision()
		
	def check_bullet_ufo_collision(self):
		collisions = pygame.sprite.groupcollide(self.bullets, self.ufo_army, True, True)
		'''
		for hitufo in collisions:
			hitufo.life -= 1
			if hitufo.life ==0:
				self.ufo_army.remove(hitufo) #klo mau kasih nyawa
				'''
		if len(self.ufo_army) == 0:
			self.bullets.empty()
			self.create_ufo_army()


	def create_ufo(self, each_ufo, every_row):
		ufo = Ufo(self)
		ufo_width, ufo_height = ufo.rect.size
		ufo.x = ufo_width + (2 * ufo_width * each_ufo)
		ufo.rect.x = ufo.x
		ufo.rect.y = ufo_height + (2 * ufo_height * every_row)
		self.ufo_army.add(ufo) #keranjang


	def create_ufo_army(self):
		ufo = Ufo(self)
		ufo_width, ufo_height = ufo.rect.size
		available_space_for_ufo = self.my_settings.window_width - (2*ufo_width)
		number_of_ufo = available_space_for_ufo // (2*ufo_width)

		ship_p1_height = self.my_ship.rect.height
		available_space_for_row = self.my_settings.window_height - (3*ufo_height) - ship_p1_height
		number_of_row = available_space_for_row // (2*ufo_height)

		for every_row in range(number_of_row):
			for each_ufo in range(number_of_ufo+1):
				self.create_ufo(each_ufo, every_row)

	def update_ufo(self):
		self.check_ufo_army()
		self.ufo_army.update()

	def check_ufo_army(self):
		for ufo in self.ufo_army.sprites():
			#if ufo.check_life():
				#self.ufo_army.delete(ufo)
			if ufo.check_edges():
				self.change_direction_ufo_army()
				break #biar ga terus2an

	def change_direction_ufo_army(self):
		for ufo in self.ufo_army.sprites():
			ufo.rect.y += self.my_settings.ufo_drop_speed
		self.my_settings.ufo_direction *= -1

	def create_star(self, pos_x, pos_y): #ini star
		star = Star(self)
		star.rect.x, star.rect.y = pos_x, pos_y
		self.my_stars.add(star)

	def create_my_stars(self):
		star = Star(self)
		star_width, star_height = star.rect.size
		number_of_stars = (self.my_settings.window_width * self.my_settings.window_height) // (star_width*star_height)

		for each_star in range(number_of_stars//5):
			pos_x = random.randint(0, self.my_settings.window_width)
			pos_y = random.randint(0, self.my_settings.window_height)
			self.create_star(pos_x, pos_y)

	def update_frame(self):
		self.my_settings.blit_back()
		self.my_stars.draw(self.screen)

		self.my_ship.blit_ship()

		for bullet in self.bullets.sprites():
			bullet.draw()
			
		self.ufo_army.draw(self.screen)

		pygame.display.flip()

Game_ALIEN = AlienWorld()
Game_ALIEN.run_game()