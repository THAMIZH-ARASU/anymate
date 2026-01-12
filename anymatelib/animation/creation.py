"""Creation animations."""

import numpy as np
from anymatelib.animation.animation import Animation
from anymatelib.mobject.mobject import Mobject


class Create(Animation):
    """Animate the creation of a mobject by drawing it."""
    
    def __init__(self, mobject: Mobject, **kwargs):
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha: float):
        """Draw the mobject progressively."""
        if self.starting_mobject is None:
            return
        
        # Interpolate opacity
        self.mobject.set_opacity(alpha)


class Write(Create):
    """Animate writing text or drawing a mobject."""
    pass


class DrawBorderThenFill(Animation):
    """Draw the border of a mobject, then fill it."""
    
    def __init__(self, mobject: Mobject, **kwargs):
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha: float):
        """Draw border then fill."""
        if alpha < 0.5:
            # First half: draw border
            self.mobject.stroke_opacity = alpha * 2
            self.mobject.fill_opacity = 0
        else:
            # Second half: fill
            self.mobject.stroke_opacity = 1
            self.mobject.fill_opacity = (alpha - 0.5) * 2


class FadeIn(Animation):
    """Fade in a mobject."""
    
    def interpolate_mobject(self, alpha: float):
        """Fade in by increasing opacity."""
        self.mobject.set_opacity(alpha)


class FadeOut(Animation):
    """Fade out a mobject."""
    
    def interpolate_mobject(self, alpha: float):
        """Fade out by decreasing opacity."""
        self.mobject.set_opacity(1 - alpha)


class GrowFromCenter(Animation):
    """Grow a mobject from its center."""
    
    def begin(self):
        super().begin()
        self.center = self.mobject.get_center()
    
    def interpolate_mobject(self, alpha: float):
        """Scale up from zero."""
        if self.starting_mobject is None:
            return
        
        self.mobject.points = self.starting_mobject.points.copy()
        self.mobject.move_to(self.center)
        
        # Scale from 0 to 1
        scale_factor = alpha
        for i, point in enumerate(self.mobject.points):
            self.mobject.points[i] = scale_factor * (point - self.center) + self.center


class Uncreate(Animation):
    """Reverse of Create - erase a mobject."""
    
    def interpolate_mobject(self, alpha: float):
        """Erase the mobject progressively."""
        self.mobject.set_opacity(1 - alpha)


class ShowCreation(Create):
    """Alias for Create."""
    pass
