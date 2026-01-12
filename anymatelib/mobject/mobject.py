"""Base Mobject (Mathematical Object) class."""

import numpy as np
from typing import List, Optional, Tuple, Union
from anymatelib.constants import *


class Mobject:
    """
    Base class for all mathematical objects in Anymate.
    
    A Mobject is any object that can be displayed and animated.
    """
    
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.color = kwargs.get('color', WHITE)
        self.opacity = kwargs.get('opacity', 1.0)
        
        # Position, rotation, scale
        self.points = np.zeros((0, 3))
        self.submobjects = []
        
        # Transformation state
        self._position = np.array([0.0, 0.0, 0.0])
        self._rotation = 0.0
        self._scale = 1.0
        
        # Rendering properties
        self.stroke_width = kwargs.get('stroke_width', DEFAULT_STROKE_WIDTH)
        self.fill_opacity = kwargs.get('fill_opacity', 0.0)
        self.stroke_opacity = kwargs.get('stroke_opacity', 1.0)
        
        # Animation tracking
        self.target = None
        self.saved_state = None
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"
    
    # Position methods
    def get_center(self) -> np.ndarray:
        """Get the center point of the mobject."""
        if len(self.points) == 0:
            return np.array([0.0, 0.0, 0.0])
        return np.mean(self.points, axis=0)
    
    def move_to(self, point: np.ndarray):
        """Move the mobject to a specific point."""
        shift = point - self.get_center()
        self.shift(shift)
        return self
    
    def shift(self, vector: np.ndarray):
        """Shift the mobject by a vector."""
        self.points += vector
        for submob in self.submobjects:
            submob.shift(vector)
        return self
    
    def scale(self, scale_factor: float, **kwargs):
        """Scale the mobject."""
        for i, point in enumerate(self.points):
            self.points[i] = scale_factor * (point - self.get_center()) + self.get_center()
        for submob in self.submobjects:
            submob.scale(scale_factor, **kwargs)
        return self
    
    def rotate(self, angle: float, axis: np.ndarray = OUT, **kwargs):
        """Rotate the mobject around an axis."""
        # Simplified rotation around z-axis
        if np.allclose(axis, OUT):
            cos_a = np.cos(angle)
            sin_a = np.sin(angle)
            rotation_matrix = np.array([
                [cos_a, -sin_a, 0],
                [sin_a, cos_a, 0],
                [0, 0, 1]
            ])
            center = self.get_center()
            self.points = (self.points - center) @ rotation_matrix.T + center
            
        for submob in self.submobjects:
            submob.rotate(angle, axis, **kwargs)
        return self
    
    # Edge methods
    def to_edge(self, edge: np.ndarray, buff: float = 0.5):
        """Move the mobject to an edge of the frame."""
        from anymatelib.config import get_config
        config = get_config()
        frame_width = config.get('frame_width', DEFAULT_FRAME_WIDTH)
        frame_height = config.get('frame_height', DEFAULT_FRAME_HEIGHT)
        
        target = np.array([0.0, 0.0, 0.0])
        if np.allclose(edge, UP):
            target[1] = frame_height / 2 - buff
        elif np.allclose(edge, DOWN):
            target[1] = -frame_height / 2 + buff
        elif np.allclose(edge, LEFT):
            target[0] = -frame_width / 2 + buff
        elif np.allclose(edge, RIGHT):
            target[0] = frame_width / 2 - buff
        
        self.move_to(target)
        return self
    
    def next_to(self, mobject, direction: np.ndarray, buff: float = 0.25):
        """Position this mobject next to another."""
        # Get the edge of the reference mobject in the given direction
        ref_center = mobject.get_center()
        ref_points = mobject.get_all_points()
        
        if len(ref_points) > 0:
            # Find the extreme point in the direction
            if np.allclose(direction, DOWN):
                # Find bottom edge
                min_y = np.min(ref_points[:, 1])
                target_y = min_y - buff
                target = np.array([ref_center[0], target_y, 0])
            elif np.allclose(direction, UP):
                # Find top edge
                max_y = np.max(ref_points[:, 1])
                target_y = max_y + buff
                target = np.array([ref_center[0], target_y, 0])
            elif np.allclose(direction, LEFT):
                # Find left edge
                min_x = np.min(ref_points[:, 0])
                target_x = min_x - buff
                target = np.array([target_x, ref_center[1], 0])
            elif np.allclose(direction, RIGHT):
                # Find right edge
                max_x = np.max(ref_points[:, 0])
                target_x = max_x + buff
                target = np.array([target_x, ref_center[1], 0])
            else:
                # General direction
                target = ref_center + direction * buff
        else:
            target = ref_center + direction * buff
        
        self.move_to(target)
        return self
    
    # Color methods
    def set_color(self, color: str):
        """Set the color of the mobject."""
        self.color = color
        for submob in self.submobjects:
            submob.set_color(color)
        return self
    
    def set_opacity(self, opacity: float):
        """Set the opacity of the mobject."""
        self.opacity = opacity
        for submob in self.submobjects:
            submob.set_opacity(opacity)
        return self
    
    # Stroke and fill
    def set_stroke(self, color: Optional[str] = None, width: Optional[float] = None, 
                   opacity: Optional[float] = None):
        """Set stroke properties."""
        if color is not None:
            self.color = color
        if width is not None:
            self.stroke_width = width
        if opacity is not None:
            self.stroke_opacity = opacity
        return self
    
    def set_fill(self, color: Optional[str] = None, opacity: Optional[float] = None):
        """Set fill properties."""
        if color is not None:
            self.color = color
        if opacity is not None:
            self.fill_opacity = opacity
        return self
    
    # Submobject methods
    def add(self, *mobjects):
        """Add submobjects."""
        for mobject in mobjects:
            if mobject not in self.submobjects:
                self.submobjects.append(mobject)
        return self
    
    def remove(self, *mobjects):
        """Remove submobjects."""
        for mobject in mobjects:
            if mobject in self.submobjects:
                self.submobjects.remove(mobject)
        return self
    
    def get_all_points(self) -> np.ndarray:
        """Get all points including submobjects."""
        result = self.points.copy()
        for submob in self.submobjects:
            submob_points = submob.get_all_points()
            if len(submob_points) > 0:
                result = np.vstack([result, submob_points])
        return result
    
    # State saving
    def save_state(self):
        """Save the current state for later restoration."""
        self.saved_state = {
            'points': self.points.copy(),
            'color': self.color,
            'opacity': self.opacity,
            'stroke_width': self.stroke_width,
            'fill_opacity': self.fill_opacity,
            'stroke_opacity': self.stroke_opacity,
        }
        return self
    
    def restore(self):
        """Restore to saved state."""
        if self.saved_state is not None:
            self.points = self.saved_state['points'].copy()
            self.color = self.saved_state['color']
            self.opacity = self.saved_state['opacity']
            self.stroke_width = self.saved_state['stroke_width']
            self.fill_opacity = self.saved_state['fill_opacity']
            self.stroke_opacity = self.saved_state['stroke_opacity']
        return self
    
    # Copy
    def copy(self):
        """Create a copy of this mobject."""
        import copy
        return copy.deepcopy(self)
