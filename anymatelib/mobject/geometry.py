"""Geometric shapes."""

import numpy as np
from anymatelib.mobject.types.vectorized_mobject import VMobject
from anymatelib.constants import *


class Circle(VMobject):
    """A circle."""
    
    def __init__(self, radius: float = 1.0, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self._generate_points()
    
    def _generate_points(self, num_points: int = 64):
        """Generate points for the circle."""
        angles = np.linspace(0, TAU, num_points)
        points = np.array([
            [self.radius * np.cos(a), self.radius * np.sin(a), 0]
            for a in angles
        ])
        self.set_points(points)


class Square(VMobject):
    """A square."""
    
    def __init__(self, side_length: float = 2.0, **kwargs):
        super().__init__(**kwargs)
        self.side_length = side_length
        self._generate_points()
    
    def _generate_points(self):
        """Generate points for the square."""
        s = self.side_length / 2
        points = np.array([
            [-s, -s, 0],
            [s, -s, 0],
            [s, s, 0],
            [-s, s, 0],
            [-s, -s, 0],  # Close the shape
        ])
        self.set_points(points)


class Rectangle(VMobject):
    """A rectangle."""
    
    def __init__(self, width: float = 4.0, height: float = 2.0, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self._generate_points()
    
    def _generate_points(self):
        """Generate points for the rectangle."""
        w = self.width / 2
        h = self.height / 2
        points = np.array([
            [-w, -h, 0],
            [w, -h, 0],
            [w, h, 0],
            [-w, h, 0],
            [-w, -h, 0],  # Close the shape
        ])
        self.set_points(points)


class Triangle(VMobject):
    """An equilateral triangle."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generate_points()
    
    def _generate_points(self):
        """Generate points for the triangle."""
        height = np.sqrt(3)
        points = np.array([
            [0, height / 2, 0],
            [-1, -height / 2, 0],
            [1, -height / 2, 0],
            [0, height / 2, 0],  # Close the shape
        ])
        self.set_points(points)


class Line(VMobject):
    """A line segment."""
    
    def __init__(self, start: np.ndarray = LEFT, end: np.ndarray = RIGHT, **kwargs):
        super().__init__(**kwargs)
        self.set_points([start, end])
    
    def put_start_and_end_on(self, start: np.ndarray, end: np.ndarray):
        """Set the start and end points."""
        self.set_points([start, end])
        return self


class Arrow(Line):
    """An arrow (line with arrowhead)."""
    
    def __init__(self, start: np.ndarray = LEFT, end: np.ndarray = RIGHT, **kwargs):
        super().__init__(start, end, **kwargs)
        # Simplified - in full implementation would add arrowhead


class Dot(Circle):
    """A dot (small filled circle)."""
    
    def __init__(self, point: np.ndarray = ORIGIN, radius: float = 0.08, **kwargs):
        kwargs.setdefault('fill_opacity', 1.0)
        super().__init__(radius=radius, **kwargs)
        self.move_to(point)


class NumberPlane(VMobject):
    """A 2D coordinate plane with grid lines."""
    
    def __init__(self, x_range: tuple = (-10, 10), y_range: tuple = (-5, 5), **kwargs):
        super().__init__(**kwargs)
        self.x_range = x_range
        self.y_range = y_range
        self._generate_points()
    
    def _generate_points(self):
        """Generate grid lines."""
        points = []
        
        # Vertical lines
        for x in range(int(self.x_range[0]), int(self.x_range[1]) + 1):
            points.extend([
                [x, self.y_range[0], 0],
                [x, self.y_range[1], 0],
                [np.nan, np.nan, np.nan]  # Break in line
            ])
        
        # Horizontal lines
        for y in range(int(self.y_range[0]), int(self.y_range[1]) + 1):
            points.extend([
                [self.x_range[0], y, 0],
                [self.x_range[1], y, 0],
                [np.nan, np.nan, np.nan]  # Break in line
            ])
        
        self.set_points(np.array(points[:-1]))  # Remove last break
