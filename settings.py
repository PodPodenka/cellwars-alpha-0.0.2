import math

# game settings
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100
MTP = (WIDTH - 155, 3)
FPS_POS = (WIDTH - 80, 35)
FPS_POS2 = (WIDTH - 80, 70)
SHOW_FPS = True
FPS_POS_I = (WIDTH - 50, 750)

# minimap settings
MAP_SCALE = 5
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)
MINIMAP_SCALE = 5
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = DIST * TILE
SCALE = WIDTH // NUM_RAYS

# player settings
player_pos = (HALF_WIDTH, HALF_HEIGHT)
player_angle = 0
player_speed = 4
player_money = 100

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (120, 120, 120)