import pygame as pg
from classes import *
from functions import *

pg.init()

clock = pg.time.Clock()
fps = 60
font = pg.font.Font(size = 50)

#a screen that fits the screen of my phone 
mobile_sz = (1080, 2408) 
mobile_screen =  pg.display.set_mode(mobile_sz)

#the screen which must replace mobile_screen
main_scr_sz = (128, 284) 
main_screen = pg.Surface(main_scr_sz)
resized = None


menu = Menu(main_scr_sz)

level = Level(0, 2, main_scr_sz)
player = level.player
button = Button(20, 20, "start")

scene = menu



run = True
while run:
	time = clock.tick(fps)
	finger_pos = pg.math.Vector2(0, 0)

	for event in pg.event.get():
		if event.type == pg.QUIT: run = False
		if event.type == pg.FINGERMOTION: pass
		if event.type == pg.FINGERDOWN:
			finger_pos.x = event.x * main_scr_sz[0]
			finger_pos.y = event.y * main_scr_sz[1]
	
	text = font.render(f"{button.clicked}", True, (255, 255, 0))
	
	if input_detection()[0]: pass #fps = 1
	#else: fps = 60		
	level.update()
	if level.state == "done": run = False
	
	button.check_press(finger_pos)
	
	#main_screen.fill((0, 200, 230))
	level.display()
	
	main_screen.blit(level.background, (0, 0))
	main_screen.blit(level.panorama, level.pos)
	main_screen.blit(button.sprite, button.pos)
	
	resized  = pg.transform.scale(main_screen, mobile_sz)
	mobile_screen.blit(resized, (0, 0))
	
	mobile_screen.blit(text, (0, 0))
	
	#pg.image.save(level0.panorama, f"screenshots/frame.png");
	
	pg.display.update()
	

pg.quit()