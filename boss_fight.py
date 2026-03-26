import pygame as pg
from functions import *
from constants import *
from classes import *

class Piranha():
	def __init__(self, x, y):
		self.pos = pg.math.Vector2(x, y)
		self.DEFPOS = (x, y)
		self.sprites = [
		pg.image.load("assets/sprites/piranha0.png").convert_alpha(),
		pg.image.load("assets/sprites/piranha1.png").convert_alpha()]
		
		self.source_sprite = self.sprites[0]
		self.sprite = self.source_sprite
		
		self.shape = self.sprite.get_rect(center=self.pos)
		self.shape.w *= 0.9; self.shape.h *= 0.9; 
		self.angle = 0
		self.gravity = 0.1
		self.jump_vel = 5
		self.state = "surf"
		
		self.rot_rect = None
		
		self.dive_vel = 0
		
		self.time = 50
		
	def jump(self):
		self.pos.y -= self.jump_vel
		self.jump_vel -= self.gravity
		self.shape.center = self.pos
		
	def dive(self):
		if self.pos.y < 242:
			self.dive_vel += 0.05
			self.pos.y += self.dive_vel
			
		else:
			self.state = "wait"
		
	def emerge(self):
		if self.dive_vel <= 0:
			self.state = "surf"
		
		else:
			self.dive_vel -= 0.05
			self.pos.y -= self.dive_vel
		
			
	def countdown(self):
		self.time -= 1
		if self.time <= 0:
			self.time = 50
			return True
		
		
	def update(self):
		self.sprite, self.rot_rect = rotate(self.source_sprite, self.angle, self.pos)
		
		if self.state == "surf":
			self.pos.x, self.pos.y = self.DEFPOS
			if input_detection() != VECTOR_ZERO:
				self.state = "dive"
		
		if self.state == "dive": self.dive()
		
		if self.state == "wait":
			if self.countdown(): #returns True if done
				self.state = "emerge"
		
		if self.state == "emerge": self.emerge()
	
		#if input_detection() != VECTOR_ZERO: self.state = "jumping"
		
		if self.state == "jumping": self.jump()
		
		self.shape.center = self.rot_rect.center
		
		
		

class PiranhaFight():
	def __init__(self, main_scr_sz = (128, 284)):
		self.background = pg.image.load("assets/sprites/background.png").convert()
		self.foreground = pg.image.load("assets/sprites/foreground.png").convert_alpha()
		self.water = pg.image.load("assets/sprites/water.png").convert_alpha()
		self.foregroundx = 0
		self.piranha = Piranha(0, 200)
		
		self.player = Player(104, 191)
		
		self.outputscreen = pg.Surface(main_scr_sz)
		
		self.monogram = pg.font.Font(f"assets/fonts/monogram.ttf", size=16)
		self.level_text = self.monogram.render("BOSS", False,  (31,54,12))
		
	def draw(self):
		self.outputscreen.blit(self.background, (0,-35))
		
		
		self.outputscreen.blit(self.foreground, (self.foregroundx, 122))
		self.outputscreen.blit(self.foreground, (self.foregroundx + 128, 122))
		
		
		self.outputscreen.blit(self.player.sprite, self.player.shape.topleft)
		
		
		#pg.draw.rect(self.outputscreen, (255,0,0), self.piranha.rot_rect)
		#pg.draw.rect(self.outputscreen, (0,0,0), self.piranha.shape)
		
		self.outputscreen.blit(self.piranha.sprite, self.piranha.rot_rect)
		
		self.outputscreen.blit(self.water, (self.foregroundx, 212))
		self.outputscreen.blit(self.water, (self.foregroundx+128, 212))
		
		self.outputscreen.blit(self.level_text, (100, 0))
		
	def update(self):
		self.foregroundx -= 1
		if self.foregroundx <= -128: self.foregroundx = 0
		
		self.piranha.update()
		
		
		self.draw()
		
		
		
		
			
		