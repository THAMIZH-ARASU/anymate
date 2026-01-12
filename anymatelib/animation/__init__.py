"""Animation package initialization."""

from anymatelib.animation.animation import (
    Animation, Wait,
    smooth, linear, rush_into, rush_from, there_and_back, wiggle
)
from anymatelib.animation.creation import (
    Create, Write, DrawBorderThenFill,
    FadeIn, FadeOut, GrowFromCenter, Uncreate, ShowCreation
)
from anymatelib.animation.transform import (
    Transform, ReplacementTransform, MoveToTarget, ApplyMethod,
    Rotate, Shift, Scale
)

__all__ = [
    # Base
    "Animation",
    "Wait",
    # Rate functions
    "smooth",
    "linear",
    "rush_into",
    "rush_from",
    "there_and_back",
    "wiggle",
    # Creation
    "Create",
    "Write",
    "DrawBorderThenFill",
    "FadeIn",
    "FadeOut",
    "GrowFromCenter",
    "Uncreate",
    "ShowCreation",
    # Transform
    "Transform",
    "ReplacementTransform",
    "MoveToTarget",
    "ApplyMethod",
    "Rotate",
    "Shift",
    "Scale",
]
