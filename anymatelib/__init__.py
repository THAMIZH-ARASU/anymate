"""Anymate - A powerful animation engine."""

__version__ = "0.1.0"

# Core imports
from anymatelib.constants import *
from anymatelib.config import get_config, reset_config

# Mobjects
from anymatelib.mobject import (
    Mobject, VMobject,
    Circle, Square, Rectangle, Triangle,
    Line, Arrow, Dot, NumberPlane,
    Text, TexText, MathTex
)

# Animations
from anymatelib.animation import (
    Animation, Wait,
    Create, Write, DrawBorderThenFill,
    FadeIn, FadeOut, GrowFromCenter, Uncreate, ShowCreation,
    Transform, ReplacementTransform, MoveToTarget, ApplyMethod,
    Rotate, Shift, Scale,
    smooth, linear, rush_into, rush_from, there_and_back, wiggle
)

# Scene
from anymatelib.scene import Scene, ThreeDScene, SpecialThreeDScene

# Camera
from anymatelib.camera import Camera, CameraFrame

__all__ = [
    # Version
    "__version__",
    
    # Config
    "get_config",
    "reset_config",
    
    # Constants (all exported from constants.py)
    "PI", "TAU", "DEGREES",
    "ORIGIN", "UP", "DOWN", "LEFT", "RIGHT", "IN", "OUT",
    "UL", "UR", "DL", "DR",
    "WHITE", "BLACK", "GREY", "GRAY", "DARK_GREY", "DARK_GRAY",
    "LIGHT_GREY", "LIGHT_GRAY",
    "RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "PURPLE", "PINK",
    "MAROON", "TEAL",
    "BLUE_A", "BLUE_B", "BLUE_C", "BLUE_D", "BLUE_E",
    "RED_A", "RED_B", "RED_C", "RED_D", "RED_E",
    "GREEN_A", "GREEN_B", "GREEN_C", "GREEN_D", "GREEN_E",
    "YELLOW_A", "YELLOW_B", "YELLOW_C", "YELLOW_D", "YELLOW_E",
    "PURPLE_A", "PURPLE_B", "PURPLE_C", "PURPLE_D", "PURPLE_E",
    
    # Mobjects
    "Mobject",
    "VMobject",
    "Circle",
    "Square",
    "Rectangle",
    "Triangle",
    "Line",
    "Arrow",
    "Dot",
    "NumberPlane",
    "Text",
    "TexText",
    "MathTex",
    
    # Animations
    "Animation",
    "Wait",
    "Create",
    "Write",
    "DrawBorderThenFill",
    "FadeIn",
    "FadeOut",
    "GrowFromCenter",
    "Uncreate",
    "ShowCreation",
    "Transform",
    "ReplacementTransform",
    "MoveToTarget",
    "ApplyMethod",
    "Rotate",
    "Shift",
    "Scale",
    "smooth",
    "linear",
    "rush_into",
    "rush_from",
    "there_and_back",
    "wiggle",
    
    # Scene
    "Scene",
    "ThreeDScene",
    "SpecialThreeDScene",
    
    # Camera
    "Camera",
    "CameraFrame",
]
