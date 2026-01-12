"""Text mobjects."""

import numpy as np
from anymatelib.mobject.types.vectorized_mobject import VMobject
from anymatelib.constants import *


class Text(VMobject):
    """
    A text mobject.
    
    In a full implementation, this would use manimpango for text rendering.
    For now, this uses PIL to render basic text.
    """
    
    def __init__(self, text: str, font_size: float = 48, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = font_size
        # Set fill by default for text
        if 'fill_opacity' not in kwargs:
            self.fill_opacity = 1.0
        if 'stroke_width' not in kwargs:
            self.stroke_width = 0
        self._generate_points()
    
    def _generate_points(self):
        """Generate placeholder points for text - actual rendering happens in scene_file_writer."""
        # Create a bounding box for the text
        # Approximate width based on character count
        char_width = self.font_size * 0.6  # Rough approximation
        width = len(self.text) * char_width / 100  # Scale to scene coordinates
        height = self.font_size / 50  # Scale to scene coordinates
        
        w = width / 2
        h = height / 2
        points = np.array([
            [-w, -h, 0],
            [w, -h, 0],
            [w, h, 0],
            [-w, h, 0],
            [-w, -h, 0],
        ])
        self.set_points(points)
    
    def __repr__(self):
        return f"Text('{self.text}')"


class TexText(Text):
    """
    LaTeX text mobject.
    
    In a full implementation, this would compile LaTeX and convert to SVG.
    """
    
    def __init__(self, *tex_strings, **kwargs):
        text = " ".join(tex_strings)
        super().__init__(text, **kwargs)


class MathTex(TexText):
    """
    Mathematical LaTeX expression.
    """
    pass
