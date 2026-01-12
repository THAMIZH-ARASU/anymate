"""Vectorized Mobject - for smooth curves and shapes."""

import numpy as np
from anymatelib.mobject.mobject import Mobject
from anymatelib.constants import *


class VMobject(Mobject):
    """
    Vectorized Mobject - uses bezier curves for smooth rendering.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fill_color = kwargs.get('fill_color', self.color)
        self.stroke_color = kwargs.get('stroke_color', self.color)
    
    def start_new_path(self, point: np.ndarray):
        """Start a new path at the given point."""
        if len(self.points) > 0:
            self.points = np.vstack([self.points, point])
        else:
            self.points = np.array([point])
        return self
    
    def add_line_to(self, point: np.ndarray):
        """Add a line to the given point."""
        if len(self.points) == 0:
            self.start_new_path(point)
        else:
            self.points = np.vstack([self.points, point])
        return self
    
    def set_points(self, points: np.ndarray):
        """Set the points of the VMobject."""
        self.points = np.array(points)
        return self
    
    def set_fill(self, color: str = None, opacity: float = None):
        """Set fill properties."""
        if color is not None:
            self.fill_color = color
        if opacity is not None:
            self.fill_opacity = opacity
        return self
    
    def set_stroke(self, color: str = None, width: float = None, opacity: float = None):
        """Set stroke properties."""
        if color is not None:
            self.stroke_color = color
        if width is not None:
            self.stroke_width = width
        if opacity is not None:
            self.stroke_opacity = opacity
        return self
