"""Constants used throughout Anymate."""

import numpy as np

# Geometry
PI = np.pi
TAU = 2 * PI
DEGREES = TAU / 360

# Directions
ORIGIN = np.array([0.0, 0.0, 0.0])
UP = np.array([0.0, 1.0, 0.0])
DOWN = np.array([0.0, -1.0, 0.0])
RIGHT = np.array([1.0, 0.0, 0.0])
LEFT = np.array([-1.0, 0.0, 0.0])
IN = np.array([0.0, 0.0, -1.0])
OUT = np.array([0.0, 0.0, 1.0])

# Useful diagonal directions
UL = UP + LEFT
UR = UP + RIGHT
DL = DOWN + LEFT
DR = DOWN + RIGHT

# Colors (RGB format)
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY = "#888888"
GRAY = GREY
DARK_GREY = "#444444"
DARK_GRAY = DARK_GREY
LIGHT_GREY = "#BBBBBB"
LIGHT_GRAY = LIGHT_GREY

# Basic colors
RED = "#FC6255"
GREEN = "#83C167"
BLUE = "#58C4DD"
YELLOW = "#FFD94A"
ORANGE = "#FC9758"
PURPLE = "#C59DF6"
PINK = "#F37FB1"
MAROON = "#EC4E56"
TEAL = "#65DCB0"

# Color variants
BLUE_A = "#C7E9F1"
BLUE_B = "#9CDBEA"
BLUE_C = "#58C4DD"
BLUE_D = "#29ABCA"
BLUE_E = "#1C758A"

RED_A = "#FFA8A0"
RED_B = "#FC8177"
RED_C = "#FC6255"
RED_D = "#E14B3D"
RED_E = "#A83B32"

GREEN_A = "#C9E2AE"
GREEN_B = "#A6CF8C"
GREEN_C = "#83C167"
GREEN_D = "#77B05D"
GREEN_E = "#699C52"

YELLOW_A = "#FFF1B6"
YELLOW_B = "#FFE79A"
YELLOW_C = "#FFD94A"
YELLOW_D = "#F4D345"
YELLOW_E = "#E8C42D"

PURPLE_A = "#E0CAFF"
PURPLE_B = "#D4B2FF"
PURPLE_C = "#C59DF6"
PURPLE_D = "#9A72CB"
PURPLE_E = "#715582"

# Sizes
DEFAULT_STROKE_WIDTH = 4
DEFAULT_FRAME_WIDTH = 14.0
DEFAULT_FRAME_HEIGHT = 8.0
DEFAULT_PIXEL_WIDTH = 1920
DEFAULT_PIXEL_HEIGHT = 1080

# Animation
DEFAULT_WAIT_TIME = 1.0
DEFAULT_ANIMATION_RUN_TIME = 1.0
DEFAULT_ANIMATION_LAG_RATIO = 0

# Frame rate
DEFAULT_FRAME_RATE = 60

# File extensions
VIDEO_DIR = "./media/videos"
IMAGE_DIR = "./media/images"
TEX_DIR = "./media/Tex"
