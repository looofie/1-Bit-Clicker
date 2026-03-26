import pygame as pg

VECTOR_ZERO = pg.math.Vector2(0, 0)

RED = (255, 0, 0) #bricks  / portal point 3
DARK_RED = (127, 0, 0) #bounds
BLUE = (0, 0, 255); #spike 
DARK_BLUE = (0, 0, 127)#rest area
YELLOW = (255, 255, 0) #goal pipe / portal point 1
GREEN = (0, 255, 0) #player
MAGENTA = (255, 0, 255) #enemy / portal point 5
CYAN = (0, 255, 255) #ground lever left
DARK_CYAN = (0, 127, 127) #lground ever right
AQUA_GREEN = (0, 255, 127) #roof lever left
DARK_AQUA_GREEN = (0, 127, 63) #roof lever right
SEA_BLUE = (0, 127, 255) #left wall lever up
DARK_SEA_BLUE = (0, 63, 127) # left wall lever down
VIOLET = (63, 63, 255) #right wall lever up
DARK_VIOLET = (31, 31, 127) #right wall lever down
GOLD_A = (255, 191, 0) #portal left exit
GOLD_B = (127, 95, 0) #portal corner
GOLD_C = (63, 47, 0) #portal vertical
GOLD_D = (15, 11, 0) #portal horizontal
ORANGE = (255, 127, 0) #portal right exit / portal point 2
LEMON_GREEN = (127, 255, 0) #portal entry left
DARK_LEMON_GREEN = (63, 127, 0) #portal entry right
DARK_MAGENTA = (255, 0, 127) #portal point 4
VIOLET2 = (127, 0 , 255)# portal point 6
BROWN = (127, 63, 0)# balls


colors = (RED, DARK_RED, BLUE, DARK_BLUE, YELLOW, GREEN, MAGENTA, CYAN, DARK_CYAN, AQUA_GREEN, DARK_AQUA_GREEN, SEA_BLUE, DARK_SEA_BLUE, VIOLET, DARK_VIOLET, GOLD_A, GOLD_B, GOLD_C, GOLD_D, ORANGE, LEMON_GREEN, DARK_LEMON_GREEN, BROWN)


