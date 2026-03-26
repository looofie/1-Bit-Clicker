import pygame as pg
from classes import *
from functions import *
from boss_fight import *

pg.init()

clock = pg.time.Clock()
fps = 60
font = pg.font.Font(size = 50)

#final upspcaled res
mobile_sz = (1080/3, 2408/3) 
mobile_screen =  pg.display.set_mode(mobile_sz)

#internal res
main_scr_sz = (128, 284) 
main_screen = pg.Surface(main_scr_sz)
resized = None


main_menu = MainMenu(main_scr_sz)
levels = [
Level(0, 0), Level(1, 0), Level(2, 0), Level(3, 0), Level(4, 0), PiranhaFight(), Level(5, 2)
]

piranha = levels[5].piranha

level_index = 0
transition = Transition()
state = "menu"

ball_container = BallContainer(1, 11)
heart_container = HeartContainer(2, 3)

run = True
while run:
	
	
	time = clock.tick(fps)
	finger_pos = pg.math.Vector2(0, 0)

	for event in pg.event.get():
		if event.type == pg.QUIT: run = False
		if event.type == pg.MOUSEMOTION:
			finger_pos.x = event.pos[0]
			finger_pos.y = event.pos[1]
			
		if event.type == pg.MOUSEBUTTONDOWN:
			finger_pos.x = event.pos[0]
			finger_pos.y = event.pos[1]
	
	text = font.render(f"{piranha.state}", False, (255, 255, 255))
	
	#else: fps = 60		
	#if levels[level_index].state == "done": run = False
	
	if state == "menu":
		main_menu.update(finger_pos)
		main_screen.blit(main_menu.outputscreen, (0, 0))
		if main_menu.state == "done":
			main_menu.state = "main"; state = "transition"
			
	
	if state == "transition":
		if not transition.cover:
			levels[level_index].update()
			main_screen.blit(levels[level_index].outputscreen, (0, 0))
			
			heart_container.update(levels[level_index].player.health)
			main_screen.blit(heart_container.sprite, heart_container.pos)
			
			ball_container.update(levels[level_index].player.balls)
			main_screen.blit(ball_container.sprite, ball_container.pos)
		
		transition.update()
		main_screen.blit(transition.outputscreen, (0, 0))
		if transition.iterations == 2:
			state = "level";
			levels[level_index].state = "starting"
			transition.reset()
	
	if state == "level":
		levels[level_index].update()
		main_screen.blit(levels[level_index].outputscreen, (0, 0))
		
		heart_container.update(levels[level_index].player.health)
		main_screen.blit(heart_container.sprite, heart_container.pos)
		
		ball_container.update(levels[level_index].player.balls)
		main_screen.blit(ball_container.sprite, ball_container.pos)
		
		if levels[level_index].state == "done":
			balls = levels[level_index].player.balls
			level_index += 1
			levels[level_index].player.balls = balls
			state = "transition"
		
	
	
	resized  = pg.transform.scale(main_screen, mobile_sz)
	mobile_screen.blit(resized, (0, 0))
	
	mobile_screen.blit(text, (0, 0))
	pg.draw.rect(mobile_screen, BLUE, (finger_pos.x, finger_pos.y, 10, 10))
	print(finger_pos.x, finger_pos.y)
	
	
	
	pg.display.update()

	

pg.quit()