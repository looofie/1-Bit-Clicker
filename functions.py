import pygame as pg
from PIL import Image
import numpy as np
from constants import *


def rotate(im, angle, pivot):
    image = pg.transform.rotate(im, angle)
    rect = image.get_rect()
    rect.center = pivot
    return image, rect
  
   

def coord_from_pixels(color, image, tile_size):
	pim = Image.open(image).convert('RGB')
	im  = np.array(pim)
	color = color #RBG
	Y, X = np.where(np.all(im==color,axis=2))
	
	if X.size > 0 and Y.size > 0:
		return X[0]*tile_size, Y[0]*tile_size
	else: return False
	

	
def find_pixel(color, num, dict):
	pim = Image.open(f"assets/levels/{num}.png").convert('RGB')
	im  = np.array(pim)
	color = color #RBG
	Y, X = np.where(np.all(im==color,axis=2))
	for i in range(len(X)): dict[X[i], Y[i]] = color
	
def find_pixels(colors, num, dict):
	for c in colors: find_pixel(c, num, dict)
	
def get_path_points(image, tile_size):
	a = coord_from_pixels(YELLOW, image, tile_size)
	b = coord_from_pixels(ORANGE, image, tile_size)
	c = coord_from_pixels(RED, image, tile_size)
	d = coord_from_pixels(DARK_MAGENTA, image, tile_size)
	e = coord_from_pixels(MAGENTA, image, tile_size)
	f = coord_from_pixels(VIOLET2, image, tile_size)

	points = [a, b, c , d, e, f]
	
	return tuple([p for p in points if p != False])
	
		
	
	
def check_dir(value):
	if value < 0: return -1
	if value >= 0: return 1
	
	
def draw_tiles(surface, coords, sprites):
	for i in coords:
		x = i[0]*8; y = i[1]*8
		if coords[i] == RED:
			surface.blit(sprites["brick"], (x ,y))
			
		if coords[i] == GOLD_A:
			surface.blit(sprites["portal_left_exit"], (x ,y))
	
		if coords[i] == GOLD_B:
			surface.blit(sprites["portal_corner"], (x ,y))	
					
		if coords[i] == GOLD_C:
			surface.blit(sprites["portal_vert"], (x ,y))	
					
		if coords[i] == GOLD_D:
			surface.blit(sprites["portal_horiz"], (x ,y))	
			
		if coords[i] == ORANGE:
			surface.blit(sprites["portal_right_exit"], (x ,y))


def slice_surface(surface):
	slices = []
	size = pg.math.Vector2(surface.get_size()) / 2
	for y in range(2):
		for x in range(2):
			frame = pg.Surface(size, pg.SRCALPHA)
			frame.blit(surface, (-(x * size.x), -(y * size.y)))
			slices.append(frame)
			
	return slices


def interpolate_points(points, inverse=False):
	curr_start_point_index = 0
	curr_end_point_index = 1
	
	pos = list(points[0])
	
	interpolated = []	
	
	def follow_straight_line(start_point, end_point,
	obj_coord, speed=0.1):
		#dist between start and end point
		distx = end_point[0] - start_point[0]
		disty = end_point[1] - start_point[1]
		line_size = (distx ** 2 + disty ** 2) ** 0.5
		
		#dist between obj pos a and end point
		obj_distx = end_point[0] - obj_coord[0]
		obj_disty = end_point[1] - obj_coord[1]
		obj_dist = (obj_distx ** 2 + obj_disty ** 2) ** 0.5
			
		new_coord = list(obj_coord)
		change_line = False
		
			
		if obj_dist > speed * (2/3):
			new_coord[0] += distx * speed / line_size
			new_coord[1] += disty * speed / line_size
		
		else:
			change_line = True
				
		return new_coord, change_line
	
	
	while True:
		curr_start_point = points[curr_start_point_index]
		curr_end_point = points[curr_end_point_index]
		
		change_line = False
		
		pos, change_line = follow_straight_line(
		curr_start_point,
		curr_end_point,
		pos,
		speed = 2
		)
		
		interpolated.append(tuple(pos))
		
		if change_line:
			if curr_end_point_index < len(points) - 1:
				curr_start_point_index += 1
				curr_end_point_index += 1
				
			else: break
		
	if inverse:
		interpolated.reverse()
		return tuple(interpolated)
		
	else: return tuple(interpolated)

		
		
def input_detection(): #returns a Vector
	clicking = False
	if True in pg.mouse.get_pressed(): clicking = True	
	return clicking
