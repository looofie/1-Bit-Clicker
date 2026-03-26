import pygame as pg
from functions import *
from constants import *
from random import randint 

class Player():
	def __init__(self, x, y):
		self.INITIAL_JUMP_STR = 19 * (8/64)
		self.jump_strength = -self.INITIAL_JUMP_STR
		self.vely = 0
		self.state = None
		self.velx = 1
		
		self.health = 3
		self.invincible = None
		self.INIVINC_TIME = 100
		self.invinc_timer = 0
		
		self.balls = 0
		
		self.shape = pg.Rect(x, y, 8, 8)
		self.up_rect = pg.Rect(x, y, 8, 1)
		self.down_rect = pg.Rect(x, y, 8, 1)
		self.middle_rect = pg.Rect(x, y, 10, 2)
		
		self.pos_reg = [self.shape.topleft, self.shape.topleft]
		self.dir = pg.math.Vector2(0, 0)
		self.pos = pg.math.Vector2(x, y)
		
		self.sprite = pg.image.load("assets/sprites/slime.png").convert_alpha()
		self.normal = self.sprite
		self.flipped = pg.transform.flip(self.sprite, True, False)			
		
		
	def get_ball(self, objects):
		for i, b in enumerate(objects):
			if type(b) == Ball and self.shape.colliderect(b.shape):
				self.balls += 1; del objects[i]
				
	def check_dir(self):
		del self.pos_reg[0]
		self.pos_reg.append(self.shape.topleft)
		a = self.pos_reg[0]; b = self.pos_reg[1]
		
		dir = pg.math.Vector2(b[0]-a[0], b[1]-a[1])
		
		if dir != VECTOR_ZERO: self.dir = dir.normalize()
		else: self.dir = VECTOR_ZERO
		
			
	def udsr(self):
		#stands for "update satelite rects"
		#must be called whenever self.shape position is changed
		self.down_rect.midtop = self.shape.midbottom
		self.up_rect.midbottom = self.shape.midtop
		self.middle_rect.center = self.shape.center
	
	def jump(self, rects, gravity):
		self.shape.y += self.vely; self.udsr()
		self.vely += gravity
	
		if self.vely >= 0:
			self.state = "falling"
			self.vely = 0
		
		if self.up_rect.collidelistall(rects):
			index = self.up_rect.collidelist(rects)
			self.shape.top = rects[index].bottom; self.udsr()
			self.state = "falling"
			self.vely = 0			
		
	
	def fall(self, rects, gravity):
			self.shape.y += self.vely; self.udsr()
			self.vely += gravity
			
			if self.down_rect.collidelistall(rects):
				index = self.down_rect.collidelist(rects)
				self.shape.bottom = rects[index].top; self.udsr()
				self.state = "on_ground"
				self.vely = 0
				
	def collide(self, rects):
		if self.middle_rect.collidelistall(rects):
			index = self.middle_rect.collidelist(rects)
			if self.velx > 0:
				self.shape.right = rects[index].left; self.udsr()
			if self.velx < 0:
				self.shape.left = rects[index].right; self.udsr()
						
			self.velx *= -1
	
	def damage(self, spikes, objects):
		if self.shape.collidelistall(spikes) and not self.invincible:
			self.health -= 1
			self.invincible = True
			
		for obj in objects:
			if type(obj) == Enemy and self.shape.colliderect(obj.shape):
				self.health -= 2
				self.invincible = True
		
		if self.invincible: self.invinc_timer += 1
		
		if self.invinc_timer >= self.INIVINC_TIME:
			self.invinc_timer = 0
			self.invincible = False
			
	def check_flip(self):
		if self.dir.x >= 0: self.sprite = self.normal
		else: self.sprite = self.flipped
										
	def update(self, input, rects, spikes, objects, gravity):
		self.shape.x += self.velx; self.udsr()
		
		if input and self.state == "on_ground":
			self.vely = self.jump_strength
			self.state = "jumping"
			
		if not self.down_rect.collidelistall(rects) and self.vely == 0:
			self.state = "falling"
			
		if self.state == "jumping": self.jump(rects, gravity)	
		if self.state == "falling": self.fall(rects, gravity)
		
		self.collide(rects)
		self.damage(spikes, objects)
		self.get_ball(objects)
		
		
class Enemy():
	def __init__(self, x, y):
		self.vely = 0
		self.velx = 0.2
		self.pos = pg.math.Vector2(x, y)
		#if abs(self.velx) < 1: self.velx = 1
		self.shape = pg.Rect(x, y, 8, 8)
		self.down_rect = pg.Rect(x, y, 8, 1)
		self.middle_rect = pg.Rect(x, y, 10, 2)
		self.on_ground = None
		self.wait = None
		self.wait_time = 5
		
		self.sprite = pg.image.load(
		f"assets/sprites/enemy.png").convert_alpha()
		self.unflipp_sprite = self.sprite
		self.flipped_sprite = pg.transform.flip(self.sprite, True, False)
		self.sprite_offset = pg.math.Vector2(-4, 0)

	def udsr(self):
		#stands for "update satellite rects"
		#must be called every time self.shape position is changed
		self.down_rect.topleft = self.shape.bottomleft
		self.middle_rect.center = self.shape.center
											
	def fall(self, rects, gravity):
			self.pos.y += self.vely;
			self.vely += gravity
			self.shape.y = int(self.pos.y); self.udsr()
			
			if self.down_rect.collidelistall(rects):
				index = self.down_rect.collidelist(rects)
				self.shape.bottom = rects[index].top; self.udsr()
				self.on_ground = True
				self.vely = 0
				self.pos.y = self.shape.topleft[1]
				
	def update_timer(self):
		self.wait_time -= 1
		if self.wait_time <= 0:
			self.wait_time = 5; self.wait = False
		
				
	def collide(self, rects, bounds):
		all_rects = rects + bounds
		if self.middle_rect.collidelistall(all_rects):
			index = self.middle_rect.collidelist(all_rects)
			if self.velx > 0:
				self.shape.right = all_rects[index].left; self.udsr()
			if self.velx < 0:
				self.shape.left = all_rects[index].right; self.udsr()		
		
			self.velx *= -1; self.wait = True;
			self.pos.x = self.shape.topleft[0]
	
	# epinshape = end pipe inside shape
	def update(self, rects, bounds, gravity, epinshape):
		if self.shape.colliderect(epinshape):
			self.velx = -abs(self.velx)
			self.shape.right = epinshape.left; self.udsr()
			self.wait = True
			self.pos.x = self.shape.topleft[0]
			
		
		else:
			self.pos.x += self.velx
			self.shape.x = int(self.pos.x); self.udsr()
				
			if not self.down_rect.collidelistall(rects) and self.vely == 0:
				self.on_ground = False	
			if not self.on_ground: self.fall(rects, gravity)
			
			if self.wait: self.update_timer()
			else: self.collide(rects, bounds)
			
			
		if self.velx >=  0: self.sprite = self.flipped_sprite
		else: self.sprite = self.unflipp_sprite
		

		

class StartPipe():
	def __init__(self, x, y):
		self.shape = pg.Rect(x, y, 16, 16)
		self.sprite = pg.image.load(
		f"assets/sprites/start_pipe.png").convert_alpha()

class EndPipe():
	def __init__(self, x, y):
		self.shape = pg.Rect(x, y, 16, 16)
		
		#for checking if enemy is stuck inside 		
		w = self.shape.w; h = self.shape.h
		self.in_shape = pg.Rect(x, y, w, h*0.9)
		self.in_shape.bottomright = self.shape.bottomright
		
		self.on = pg.image.load(
		f"assets/sprites/end_pipe_on.png").convert_alpha()
		
		self.off = pg.image.load(
		f"assets/sprites/end_pipe_off.png").convert_alpha()

		self.sprites = [self.off, self.on]
		self.state = 0
		self.sprite = self.off
		
	
	def toggle(self):
		self.sprite = self.sprites[self.state]
		self.state += 1
		if self.state > 1: self.state = 0
		


class Lever():
	def __init__(self, x, y, state, type="ground"):
		self.type = type
		self.shape = pg.Rect(x, y, 8, 8)
		
		left = pg.image.load(
		f"assets/sprites/lever_left.png").convert_alpha()
		
		right = pg.image.load(
		f"assets/sprites/lever_right.png").convert_alpha()
		
		self.sprites = { "left" : left, "right" : right }
		
		offset = pg.math.Vector2(-4, 0)
		
		if type == "roof":
			for i in self.sprites:
				self.sprites[i] = pg.transform.flip(self.sprites[i], False, True)
		if type == "left_wall":
			for i in self.sprites:
				self.sprites[i] = pg.transform.rotate(self.sprites[i], -90)
				offset = pg.math.Vector2(0, -4)
		
		if type == "right_wall":
			for i in self.sprites:
				self.sprites[i] = pg.transform.rotate(self.sprites[i], 90)
				self.sprites[i] = pg.transform.flip(self.sprites[i], False, True)
				offset = pg.math.Vector2(0, -4)		
			
				
		self.sprite = self.sprites[state]
		self.sprite_pos = self.shape.topleft + offset
		self.state = state
		self.events = [None, None]
		
	def detect_change(self):
		del self.events[0]
		self.events.append(self.sprite)
		
		if self.events[0] != self.events[1]: return True
		else: return False
		
						
class Camera():
	def __init__(self, player, pos, output_scr_sz):
		self.shake_duration = 25
		self.SHAKE_STREN = 1
		self.player = player
		self.pos = pos
		self.output_scr_sz = output_scr_sz
		self.offset = pg.math.Vector2(0.5, 0.5)
		self.offset_speed = 0.01
		self.pause = False
		
		
	def update_offset(self):
		dir = self.player.dir
		self.offset.x -= dir.x * self.offset_speed
		self.offset.y -= dir.y * self.offset_speed / 8
				
		if self.offset.x <= 0.25: self.offset.x = 0.25
		if self.offset.x >= 0.75:self.offset.x = 0.75
		
		if self.offset.y <= 0.25: self.offset.y = 0.25
		if self.offset.y >= 0.75:self.offset.y = 0.75
		
		
			
		
	def update(self):
		p = pg.math.Vector2(self.player.shape.center)
	
		if self.pause: self.offset_speed = -0.004
		else: self.offset_speed = 0.008
			
		self.update_offset()
		
		self.pos.y = -p.y + (self.output_scr_sz[1] * self.offset.y)
		self.pos.x = -p.x + (self.output_scr_sz[0] * self.offset.x)		
			
			
	def shake(self): 
		if self.player.invinc_timer < self.shake_duration:
			s = self.SHAKE_STREN
			self.update()
			x = int(self.pos.x); y = int(self.pos.y)
			
			self.pos.x = randint(x - s, x + s)
			self.pos.y = randint(y - s, y + s)
			

class Spike():
	def __init__(self, x, y, rot):
		self.pos = [x, y]
		v = pg.Rect(x+4, y, 1, 8)
		h = pg.Rect(x, y+4, 8, 1)
		
		img = pg.image.load(f"assets/sprites/spike.png").convert_alpha()
		img = pg.transform.rotate(img, rot)
		self.sprite = img
		
		self.shape = None
		if rot in  [0, 180]: self.shape = v
		else: self.shape = h


class Ball():
	def __init__(self, x, y):
		self.sprite = pg.image.load(f"assets/sprites/ball.png").convert_alpha()
		s = self.sprite.get_size()
		self.shape = pg.Rect(x, y, s[0], s[1])
		
class Button():
	def __init__(self, x, y, name):
		self.name = name
		self.pos = pg.math.Vector2(x, y)		
		
		self.unclicked_spr = pg.image.load(f"assets/sprites/{name}.png").convert_alpha()
		
		self.clicked_spr = self.unclicked_spr
		
		try: self.clicked_spr = pg.image.load(f"assets/sprites/{name}_clicked.png").convert_alpha()
		except: pass
		
		self.shape = self.clicked_spr.get_rect()
		self.shape.topleft = (x, y)
		self.sprite = self.unclicked_spr
		self.timer = 10
		self.clicked = False
		
	def check_press(self, point):
		if self.clicked:
			self.timer -= 1
			if self.timer <= 0:
				self.timer = 10; self.clicked = False
		
		if self.shape.collidepoint(point):
			self.clicked = True
			
		if self.clicked: self.sprite = self.clicked_spr
		else: self.sprite = self.unclicked_spr


class Selector():
	def __init__(self, options, x, y):
		self.options = []
		
		if "yes" in options:
			self.options.append(Button(x, y, options[0]))
			button2 = Button(x, y, options[1])
			button2.shape.center = self.options[0].shape.center
			button2.pos = button2.shape.topleft
			self.options.append(button2)
		
		if "english" in options:
			self.options.append(Button(x, y, options[0]))
		
		self.shape = self.options[0].shape
			
	def check_press(self, finger_pos):
		if self.shape.collidepoint(finger_pos):
			a = self.options[0]; del self.options[0]
			self.options.append(a)
			
			
		
			
			
		
class MainMenu():
	def __init__(self, screen_sz):
		self.mainmenu_bg = pg.image.load("assets/sprites/mainmenu_bg.png").convert()
		self.config_bg = pg.image.load("assets/sprites/config_bg.png").convert()
		self.start_button = Button(30, 235, "start")
		self.config_button = Button(110, 2, "config")
		
		Button(23, 52, "english")
		
		self.lang_selector = Selector(["english"], 23, 52)
		
		self.yes_no_selec = Selector(["yes", "no"], 43, 156)
		self.no_yes_selec = Selector(["no", "yes"], 48, 104)
		
		self.confirm_button = Button(7, 218, "confirm")
		
		self.language = "english"
		self.delete_save = False
		self.camera_shake = True
		
		self.mainscreen = pg.Surface(screen_sz)
		self.configscreen = pg.Surface(screen_sz)
		self.aboutscreen = pg.Surface(screen_sz)
		
		self.outputscreen = pg.Surface(screen_sz)
		
		self.state = "main" #main, config, done
			
	def display(self):
		if self.state == "main":
			self.mainscreen.blit(self.mainmenu_bg, (0, 0))
			self.mainscreen.blit(self.start_button.sprite, self.start_button.pos)
			self.mainscreen.blit(self.config_button.sprite, self.config_button.pos)
			self.outputscreen.blit(self.mainscreen, (0, 0))
			
		if self.state == "config":
			self.configscreen.blit(self.config_bg, (0, 0))
			
			button = self.lang_selector.options[0]
			self.configscreen.blit(button.sprite, button.pos)
			
			button = self.no_yes_selec.options[0]
			self.configscreen.blit(button.sprite, button.pos)
			
			button = self.yes_no_selec.options[0]
			self.configscreen.blit(button.sprite, button.pos)
			
			button = self.confirm_button
			self.configscreen.blit(button.sprite, button.pos)
			
			
			
			self.outputscreen.blit(self.configscreen, (0, 0))
			
		
	
	def update(self, fingerpos):
		if self.state == "main":
			self.start_button.check_press(fingerpos)
			self.config_button.check_press(fingerpos)
			
			if self.config_button.clicked:
				self.state = "config"; self.config_button.clicked = False
		
		if self.state == "config":
			self.confirm_button.check_press(fingerpos)
			self.yes_no_selec.check_press(fingerpos)
			self.no_yes_selec.check_press(fingerpos)
			
			if self.confirm_button.clicked:
				self.state = "main"; self.confirm_button.clicked = False
			
			
		if self.start_button.clicked:
			self.state = "done"; self.start_button.clicked = False
		
		
		
		self.display()
		
		
		
class Transition():
	def __init__(self, main_scr_sz=(128, 284)):
		self.main_scr_sz = main_scr_sz
		self.outputscreen = pg.Surface(main_scr_sz)
		self.outputscreen.set_colorkey((0, 0, 0))
		self.pen = pg.Rect(-16, 0, 16, 16)
		self.pen2 = pg.Rect(main_scr_sz[0], main_scr_sz[1]-16 , 16, 16)
		self.cover = True
		self.iterations = 0
	
	def update(self):
		for i in range(2):
			if self.cover:
				pg.draw.rect(self.outputscreen, (31,54,12), self.pen)
				pg.draw.rect(self.outputscreen, (31,54,12), self.pen2)
				
			else:
				pg.draw.rect(self.outputscreen, (0,0,0), self.pen)
				pg.draw.rect(self.outputscreen, (0,0,0), self.pen2)
					
				
			self.pen.x += 16; self.pen2.x -= 16
			
			if self.pen.x >= self.main_scr_sz[0]:
				self.pen.x = -16; self.pen.y += 16
			
			if self.pen.x <= -16:
				self.pen2.x = self.main_scr_sz[0]; self.pen2.y -= 16
			
		if self.pen.y >= self.main_scr_sz[1]/2:
			self.pen.topleft = [0, 0]
			self.pen2.x = self.main_scr_sz[0];
			self.pen2.y = self.main_scr_sz[1] - 16
			self.cover = False
			self.iterations += 1
			
	def reset(self):
		self.iterations = 0
		self.cover = True
		
class HeartContainer():
	def __init__(self, x, y):
		self.pos = pg.math.Vector2(x, y)
		self.sprite = pg.Surface((71, 7), pg.SRCALPHA)
		self.sprite.set_colorkey((0,0,0))
		self.heart = pg.image.load(f"assets/sprites/heart.png").convert_alpha()
	
	def update(self, player_health=8):
		self.sprite.fill((0,0,0))
		for i in range(player_health):
			self.sprite.blit(self.heart, (i*8, -1))

class BallContainer():
	def __init__(self, x, y):
		self.pos  = pg.math.Vector2(x, y)
		self.icon = pg.image.load(f"assets/sprites/ball.png").convert_alpha()
		self.container = pg.image.load(f"assets/sprites/ball_container.png").convert_alpha()
		self.container.set_colorkey((0,0,0))
		self.bar = pg.Rect(9, 2, 1, 4)
		self.sprite = pg.Surface((71, 8), pg.SRCALPHA)
		self.sprite.set_colorkey((0, 0, 0))
	
	def update(self, player_balls):
		self.bar.w = 62 * (player_balls / 100)
		self.bar.left = 9
		
		pg.draw.rect(self.sprite, (31,54,12), self.bar)
		self.sprite.blit(self.container, (7, 0))
		self.sprite.blit(self.icon, (-1, 0))


class Level():
	def __init__(self, num, num_pipe_portals, main_scr_sz=(128, 284)):
		self.GRAVITY = 0.8 * (8 / 64)

		self.sprites = {
		"brick" : pg.image.load(f"assets/sprites/brick.png").convert(),
		"portal_horiz" : pg.image.load(f"assets/sprites/horizontal.png").convert_alpha(),
		"portal_vert" : pg.image.load(f"assets/sprites/vertical.png").convert_alpha(),
		"portal_corner" : pg.image.load(f"assets/sprites/corner.png").convert_alpha(),
		"portal_left_exit" : pg.image.load(f"assets/sprites/left_exit.png").convert_alpha(),
		"portal_right_exit" : pg.image.load(f"assets/sprites/right_exit.png").convert_alpha()
		}

		
		self.tile_data = {}
		find_pixels(colors, num, self.tile_data)
		
		self.collision_rects = [] #walls for collisions
		self.bound_rects = [] #for the enemies not to fall from border
		self.rest_areas = [] # list of rects
		self.spikes = [] # list of Spikes objects
		self.spikeshapes = [shp.shape for shp in self.spikes]
		self.objects = []
		self.paths = []  # [associated_rect, pipe_direction(-1 or 1),  path ]
		
		self.path_index = 0
		self.curr_path = None
		self.portal_time = 50
		self.curr_exit_dir = None
		self.path_points = []
		for i in range(num_pipe_portals):
			file_path = f"assets/levels/{num}p{i}.png"
			self.path_points.append(get_path_points(file_path, 8))
		self.path_points = tuple(self.path_points)
		
		self.player = None
		self.tile_size = 8
		pixel_data = pg.image.load(f"assets/levels/{num}.png").convert()
		size = pixel_data.get_size()
		self.size = pg.math.Vector2((size[0]*8), (size[1]*8))
		self.panorama = pg.Surface(self.size).convert()
		self.panorama.set_colorkey((0, 0, 0))
		
		self.outputscreen = pg.Surface(main_scr_sz)
		
		self.pos = pg.math.Vector2(0, 0)
		
		self.start_pipe = None
		self.end_pipe = None
		self.end_pipe_rect = None
		self.state = "ready"
		
		self.monogram = pg.font.Font(f"assets/fonts/monogram.ttf", size=16)
		self.level_text = self.monogram.render(f"LEVEL {num+1}", False,  (31,54,12))
		
		self.background = pg.image.load(f"assets/sprites/background.png").convert()
		
		for i in self.tile_data:
			x = i[0]*8; y = i[1]*8; t = 8
			
			if self.tile_data[i] == RED: #bricks
				self.collision_rects.append(pg.Rect(x, y, t, t))
				
			if self.tile_data[i] == BLUE: #spikes
				right = self.tile_data.get((i[0] +1, i[1])) != None
				up = self.tile_data.get((i[0], i[1] - 1)) != None
				left = self.tile_data.get((i[0] - 1, i[1])) != None
				
				rot = 0
				if right:
					if self.tile_data[(i[0] + 1, i[1])] == RED: rot = 90
				if up:
					if self.tile_data[(i[0], i[1] - 1)] == RED: rot = 180
				if left:
					if self.tile_data[(i[0] - 1, i[1])] == RED: rot = -90
				
				spike = Spike(x, y, rot)
				self.spikes.append(spike)
				self.spikeshapes.append(spike.shape)
				
				
				
			if self.tile_data[i] == DARK_BLUE: #rest areas
				self.rest_areas.append(pg.Rect(x, y, t, t))
			
			if self.tile_data[i] == DARK_RED: #bounds
				self.bound_rects.append(pg.Rect(x, y, t, t))
				
			if self.tile_data[i] == GREEN: #player and start pipes
				self.player = Player(x, y+(t/2))
				self.objects.append(self.player)
				self.start_pipe = StartPipe(x, y)
				self.collision_rects.append(self.start_pipe.shape)
				
			if self.tile_data[i] == MAGENTA: #enemies
				self.objects.append(Enemy(x, y))
				
			if self.tile_data[i] == CYAN: #ground levers
				self.objects.append(Lever(x+(t/2), y, "left"))
			
			if self.tile_data[i] == DARK_CYAN: #ground levers
				self.objects.append(Lever(x+(t/2), y, "right"))
			
			
			if self.tile_data[i] == AQUA_GREEN: #roof levers
				self.objects.append(Lever(x+(t/2), y, "left", "roof"))
			
			if self.tile_data[i] == DARK_AQUA_GREEN: #roof levers
				self.objects.append(Lever(x+(t/2), y, "right", "roof"))
				
			if self.tile_data[i] == SEA_BLUE: #left wall levers up
				self.objects.append(Lever(x, y+(t/2), "left", "left_wall")) 
			
			if self.tile_data[i] == DARK_SEA_BLUE: #left wall levers down
				self.objects.append(Lever(x, y+(t/2), "right", "left_wall"))
			
			if self.tile_data[i] == VIOLET: #right wall levers down
				self.objects.append(Lever(x, y+(t/2), "left", "right_wall")) 
			
			if self.tile_data[i] == DARK_VIOLET: #right wall levers up
				self.objects.append(Lever(x, y+(t/2), "right", "right_wall"))
			
			if self.tile_data[i] in [ GOLD_A, GOLD_B, GOLD_C, GOLD_D, ORANGE ]: #portal pipes
				self.collision_rects.append(pg.Rect(x, y, t*2, t*2))
			
			
			r = pg.Rect(x, y, t, t)
			if self.tile_data[i] == LEMON_GREEN: #portal left
				for pth in self.path_points:
					if pth[0] == (x, y):	
						self.paths.append([r, 1, interpolate_points(pth)])
					if pth[-1] == (x, y):
						self.paths.append([r, 1, interpolate_points(pth,True)])
			
			if self.tile_data[i] == DARK_LEMON_GREEN: #portal right
				for pth in self.path_points:
					if pth[0] == (x+t, y):	
						self.paths.append([r, -1 ,interpolate_points(pth)])
					if pth[-1] == (x+t, y):
						self.paths.append([r, -1, interpolate_points(pth, True)])
			
			if self.tile_data[i] == YELLOW: #end pipes
				self.end_pipe = EndPipe(x, y)
				self.collision_rects.append(self.end_pipe.shape)
				self.end_pipe_rect = pg.Rect(x-t, y+t, t, t)
				
			if self.tile_data[i] == BROWN: #balls
				ball = Ball(x, y)
				self.objects.append(ball)
				
				
				
		self.camera = Camera(self.player, self.pos, main_scr_sz)
		
	
	def display(self):
		self.outputscreen.blit(self.background, (0, 0))
		
		self.panorama.fill((0, 0, 0))
		p = pg.math.Vector2(self.player.shape.center)
		
		for obj in self.objects:
			if type(obj) == Enemy:
				self.panorama.blit(obj.sprite, obj.shape.topleft+obj.sprite_offset)
				
#				pg.draw.rect(self.panorama, (9,9,9), obj.shape)
#				pg.draw.rect(self.panorama, (127,255,0), obj.down_rect)
#				pg.draw.rect(self.panorama, (0,0,255), obj.middle_rect)	
			
			if type(obj) == Lever:
				self.panorama.blit(obj.sprite, obj.sprite_pos)
				
#				pg.draw.rect(self.panorama, (127,0,0), obj.shape)
			
			if type(obj) == Ball:
				self.panorama.blit(obj.sprite, obj.shape.topleft)
				
				
			
		if self.player.invincible:
			if self.player.invinc_timer % 5 != 0: self.player.sprite.set_alpha(0)
			else: self.player.sprite.set_alpha(255)
		else: self.player.sprite.set_alpha(255)
		
		self.panorama.blit(self.player.sprite, self.player.shape.topleft)
		
#		pg.draw.rect(self.panorama, (0, 0, 0), self.player.shape)
#		pg.draw.rect(self.panorama, (255, 0, 127), self.player.down_rect)
		
		self.panorama.blit(self.start_pipe.sprite, self.start_pipe.shape.topleft)
		self.panorama.blit(self.end_pipe.sprite, self.end_pipe.shape.topleft)
		
		
#		pg.draw.rect(self.panorama, (255, 255, 0), self.end_pipe_rect)
					
				
			

		#for b in self.bound_rects: pg.draw.rect(self.panorama, (240, 89, 190), b)
		for i, s in enumerate(self.spikeshapes):
			self.panorama.blit(self.spikes[i].sprite, self.spikes[i].pos)
#			pg.draw.rect(self.panorama, (255, 0, 255), s)
#		
#		for r in self.collision_rects: pg.draw.rect(self.panorama, (167, 89, 34), r)
#		pg.draw.rect(self.panorama, (127, 0, 127), self.end_pipe.in_shape)

		draw_tiles(self.panorama, self.tile_data, self.sprites)
		self.outputscreen.blit(self.level_text, (78, 0))
		self.outputscreen.blit(self.panorama, self.pos)
		
	def restart(self):
		pos = self.pos
		self.__init__(0, 0, self.output_scr_sz)
		self.pos = pos
	
	
	def move_point(self, dest, point, area = 2, speed = 1):
		p = pg.math.Vector2(point); c = pg.math.Vector2(dest)
		dx = pg.math.Vector2(c.x - p.x, 0)
		dy = pg.math.Vector2(0, c.y - p.y)
		dir = dx + dy
		if dir != VECTOR_ZERO: dir = dir.normalize()
			
		x = c.x - area     <    p.x   <    c.x + area
		y = c.y - area     <    p.y   <    c.y + area	
		
		if x and y: return VECTOR_ZERO
		else: return dir * speed		
		
		
	def update(self):
		shp = self.end_pipe.shape
		inshp = self.end_pipe.in_shape
		
		if self.end_pipe.state == 0:
			if shp not in self.collision_rects:
				self.collision_rects.append(shp)

			w = self.end_pipe.shape.w; h = self.end_pipe.shape.h
			x = self.end_pipe.shape.x; y = self.end_pipe.shape.y
			self.end_pipe.in_shape = pg.Rect(x, y, w, h*0.9)
			self.end_pipe.in_shape.bottomright = self.end_pipe.shape.bottomright
			
		else:
			if shp in self.collision_rects:
				self.collision_rects.remove(shp)

			self.end_pipe.in_shape.size = [8, 8]
			self.end_pipe.in_shape.left = self.end_pipe.shape.right
		
		
		
		lever_detection = []
		for obj in self.objects:
			if type(obj) == Enemy:
				obj.update(self.collision_rects, self.bound_rects, self.GRAVITY, self.end_pipe.in_shape)
				
			if type(obj) == Lever:
				if self.player.shape.colliderect(obj.shape):
					if obj.type in ["ground", "roof"]:
						if self.player.velx >= 0:
							obj.sprite = obj.sprites["right"]
						else:
							obj.sprite = obj.sprites["left"]
					
					else:
						if self.player.vely >= 0:
							obj.sprite = obj.sprites["right"] #down
						else:
							obj.sprite = obj.sprites["left"] #up
				
				lever_detection.append(obj.detect_change())
		
					
		if True in lever_detection: self.end_pipe.toggle()
		
		if self.state == "ready": pass
		
		if self.state == "starting":
			self.player.shape.x = int(self.player.pos.x)
			self.player.pos.x += 0.5
			if not self.player.shape.colliderect(self.start_pipe.shape):
				self.state = "in_progress"
		
		
		if self.state == "in_progress":			
			for path in self.paths:
				if self.player.shape.colliderect(path[0]):
					self.curr_path = path[2]
					self.curr_exit_dir = path[1]
					self.state = "into_portal"
				
				
		if self.state == "into_portal":
			p = self.player.shape.center; c = self.curr_path[0]
			self.player.shape.center += self.move_point(c, p)
			
			if self.move_point(c, p) == VECTOR_ZERO:
				self.state = "following_path"
		
		if self.state in ["into_portal", "following_path"]:
			self.player.damage(self.spikeshapes, self.objects)		
			
		
		if self.state == "following_path":
			i = self.path_index
						
			if i < len(self.curr_path) - 1:
				self.player.shape.center = self.curr_path[i]
				self.path_index += 1
			else:
				self.path_index = 0
				self.state = "out_portal"
			
				
		if self.state == "out_portal":
			t = pg.math.Vector2(8 * self.curr_exit_dir, 0)
			l = pg.math.Vector2(self.curr_path[-1]) + t
			p = self.player.shape.center
			
			self.player.shape.center += self.move_point(l, p)
				
			if self.move_point(l, p) == VECTOR_ZERO:
				self.player.velx = abs(self.player.velx) * self.curr_exit_dir
				self.state = "wait_portal"
				self.curr_path = None				
			
							
		if self.state == "wait_portal":
			self.portal_time -= 1
			if self.portal_time <= 0:
				self.portal_time = 50
				self.state = "in_progress"
				

		if self.state in ["in_progress", "wait_portal"]:		
			self.player.update(
			input_detection(),
			self.collision_rects,
			self.spikeshapes,
			self.objects,
			self.GRAVITY)
			
		
		on = self.end_pipe.state == 0
		collide = self.player.shape.colliderect(self.end_pipe_rect)
		if on and collide: self.state = "finishing"
			
		if self.state == "finishing":
			pi = self.end_pipe.shape.center
			pl = self.player.shape.center
			self.player.shape.center += self.move_point(pi, pl)
			if self.move_point(pi, pl) == VECTOR_ZERO:
				self.state = "done"
		
		self.player.check_dir()
		self.player.check_flip()
			
		if self.player.shape.collidelistall(self.rest_areas):
			self.camera.pause = True
		else: self.camera.pause = False
				
		self.camera.update()
			
		if self.player.invincible: self.camera.shake()
		
		self.display()
					
		
		
	