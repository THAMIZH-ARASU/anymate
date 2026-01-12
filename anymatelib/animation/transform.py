"""Transform animations."""

import numpy as np
from anymatelib.animation.animation import Animation
from anymatelib.mobject.mobject import Mobject


class Transform(Animation):
    """Transform one mobject into another."""
    
    def __init__(self, mobject: Mobject, target_mobject: Mobject, **kwargs):
        super().__init__(mobject, **kwargs)
        self.target_mobject = target_mobject
    
    def begin(self):
        super().begin()
        self.target_copy = self.target_mobject.copy()
    
    def interpolate_mobject(self, alpha: float):
        """Interpolate between starting mobject and target."""
        if self.starting_mobject is None:
            return
        
        # Interpolate points
        start_points = self.starting_mobject.points
        target_points = self.target_copy.points
        
        # Handle different numbers of points by resampling
        if len(start_points) != len(target_points):
            # Use the target's point count
            target_count = len(target_points)
            if len(start_points) > 0:
                # Resample starting points to match target
                indices = np.linspace(0, len(start_points) - 1, target_count)
                resampled_start = np.array([
                    start_points[int(i)] if i == int(i) else start_points[int(i)]
                    for i in indices
                ])
                self.mobject.points = (1 - alpha) * resampled_start + alpha * target_points
            else:
                self.mobject.points = target_points
        else:
            self.mobject.points = (1 - alpha) * start_points + alpha * target_points
        
        # Interpolate colors
        try:
            start_color = self._hex_to_rgb(self.starting_mobject.color)
            target_color = self._hex_to_rgb(self.target_copy.color)
            interp_color = tuple(int((1 - alpha) * s + alpha * t) for s, t in zip(start_color, target_color))
            self.mobject.color = self._rgb_to_hex(interp_color)
        except:
            if alpha > 0.5:
                self.mobject.color = self.target_copy.color
        
        # Interpolate fill_color for VMobjects
        if hasattr(self.starting_mobject, 'fill_color') and hasattr(self.target_copy, 'fill_color'):
            try:
                start_fill = self._hex_to_rgb(self.starting_mobject.fill_color)
                target_fill = self._hex_to_rgb(self.target_copy.fill_color)
                interp_fill = tuple(int((1 - alpha) * s + alpha * t) for s, t in zip(start_fill, target_fill))
                self.mobject.fill_color = self._rgb_to_hex(interp_fill)
            except:
                pass
        
        # Interpolate stroke_color for VMobjects
        if hasattr(self.starting_mobject, 'stroke_color') and hasattr(self.target_copy, 'stroke_color'):
            try:
                start_stroke = self._hex_to_rgb(self.starting_mobject.stroke_color)
                target_stroke = self._hex_to_rgb(self.target_copy.stroke_color)
                interp_stroke = tuple(int((1 - alpha) * s + alpha * t) for s, t in zip(start_stroke, target_stroke))
                self.mobject.stroke_color = self._rgb_to_hex(interp_stroke)
            except:
                pass
        
        # Interpolate fill opacity
        if hasattr(self.starting_mobject, 'fill_opacity') and hasattr(self.target_copy, 'fill_opacity'):
            self.mobject.fill_opacity = (1 - alpha) * self.starting_mobject.fill_opacity + alpha * self.target_copy.fill_opacity
        
        # Interpolate stroke width
        if hasattr(self.starting_mobject, 'stroke_width') and hasattr(self.target_copy, 'stroke_width'):
            self.mobject.stroke_width = (1 - alpha) * self.starting_mobject.stroke_width + alpha * self.target_copy.stroke_width
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        if not isinstance(hex_color, str):
            return (255, 255, 255)
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (255, 255, 255)
    
    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color."""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


class ReplacementTransform(Transform):
    """Transform one mobject into another, replacing the original."""
    pass


class MoveToTarget(Animation):
    """Move a mobject to its target."""
    
    def __init__(self, mobject: Mobject, **kwargs):
        if not hasattr(mobject, 'target') or mobject.target is None:
            raise ValueError("Mobject must have a target attribute")
        super().__init__(mobject, **kwargs)
    
    def begin(self):
        super().begin()
        self.target = self.mobject.target.copy()
    
    def interpolate_mobject(self, alpha: float):
        """Move towards target."""
        if self.starting_mobject is None:
            return
        
        start_center = self.starting_mobject.get_center()
        target_center = self.target.get_center()
        
        # Interpolate position
        new_center = (1 - alpha) * start_center + alpha * target_center
        self.mobject.move_to(new_center)


class ApplyMethod(Animation):
    """Apply a method to a mobject over time."""
    
    def __init__(self, method, *args, **kwargs):
        self.method = method
        self.method_args = args
        mobject = method.__self__
        super().__init__(mobject, **kwargs)
    
    def begin(self):
        super().begin()
        # Create target by applying method
        self.mobject.target = self.starting_mobject.copy()
        self.method(*self.method_args)
        self.target = self.mobject.copy()
        # Restore to starting state
        self.mobject.points = self.starting_mobject.points.copy()
    
    def interpolate_mobject(self, alpha: float):
        """Interpolate to target state."""
        if self.starting_mobject is None:
            return
        
        # Interpolate points
        start_points = self.starting_mobject.points
        target_points = self.target.points
        
        if len(start_points) == len(target_points) and len(start_points) > 0:
            self.mobject.points = (1 - alpha) * start_points + alpha * target_points


class Rotate(Animation):
    """Rotate a mobject."""
    
    def __init__(self, mobject: Mobject, angle: float, **kwargs):
        self.angle = angle
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha: float):
        """Rotate progressively."""
        if self.starting_mobject is None:
            return
        
        self.mobject.points = self.starting_mobject.points.copy()
        self.mobject.rotate(alpha * self.angle)


class Shift(Animation):
    """Shift a mobject."""
    
    def __init__(self, mobject: Mobject, vector: np.ndarray, **kwargs):
        self.vector = vector
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha: float):
        """Shift progressively."""
        if self.starting_mobject is None:
            return
        
        self.mobject.points = self.starting_mobject.points.copy()
        self.mobject.shift(alpha * self.vector)


class Scale(Animation):
    """Scale a mobject."""
    
    def __init__(self, mobject: Mobject, scale_factor: float, **kwargs):
        self.scale_factor = scale_factor
        super().__init__(mobject, **kwargs)
    
    def interpolate_mobject(self, alpha: float):
        """Scale progressively."""
        if self.starting_mobject is None:
            return
        
        self.mobject.points = self.starting_mobject.points.copy()
        current_scale = 1 + alpha * (self.scale_factor - 1)
        self.mobject.scale(current_scale)
