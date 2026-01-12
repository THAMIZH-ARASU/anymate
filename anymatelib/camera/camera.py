"""Camera system for Anymate."""

import numpy as np
from anymatelib.constants import *
from anymatelib.config import get_config


class Camera:
    """
    Camera for rendering scenes.
    
    The camera defines the view into the scene and handles projection.
    """
    
    def __init__(self, **kwargs):
        config = get_config()
        
        self.frame_width = kwargs.get('frame_width', config.get('frame_width', DEFAULT_FRAME_WIDTH))
        self.frame_height = kwargs.get('frame_height', config.get('frame_height', DEFAULT_FRAME_HEIGHT))
        self.pixel_width = kwargs.get('pixel_width', config.get('pixel_width', DEFAULT_PIXEL_WIDTH))
        self.pixel_height = kwargs.get('pixel_height', config.get('pixel_height', DEFAULT_PIXEL_HEIGHT))
        
        self.background_color = kwargs.get('background_color', config.get('background_color', BLACK))
        
        # Camera position and orientation
        self.position = np.array([0.0, 0.0, 0.0])
        self.rotation = np.array([0.0, 0.0, 0.0])
        
        # Camera frame (what the camera sees)
        self.frame_center = np.array([0.0, 0.0, 0.0])
    
    def capture_mobjects(self, mobjects):
        """
        Capture mobjects and prepare them for rendering.
        
        Returns a list of drawable primitives.
        """
        primitives = []
        for mobject in mobjects:
            primitives.extend(self._mobject_to_primitives(mobject))
        return primitives
    
    def _mobject_to_primitives(self, mobject):
        """Convert a mobject to rendering primitives."""
        primitives = []
        
        if len(mobject.points) > 0:
            # Convert points to screen coordinates
            screen_points = self._world_to_screen(mobject.points)
            
            primitive = {
                'type': 'line_strip',
                'points': screen_points,
                'color': mobject.color,
                'stroke_width': mobject.stroke_width,
                'opacity': mobject.opacity,
                'fill_opacity': mobject.fill_opacity,
            }
            primitives.append(primitive)
        
        # Process submobjects
        for submob in mobject.submobjects:
            primitives.extend(self._mobject_to_primitives(submob))
        
        return primitives
    
    def _world_to_screen(self, points):
        """Convert world coordinates to screen coordinates."""
        # Scale to pixel coordinates
        x_scale = self.pixel_width / self.frame_width
        y_scale = self.pixel_height / self.frame_height
        
        screen_points = points.copy()
        screen_points[:, 0] *= x_scale
        screen_points[:, 1] *= y_scale
        
        # Center on screen
        screen_points[:, 0] += self.pixel_width / 2
        screen_points[:, 1] += self.pixel_height / 2
        
        return screen_points
    
    def set_frame_center(self, point):
        """Set the center point of the camera frame."""
        self.frame_center = np.array(point)
    
    def get_frame_center(self):
        """Get the center point of the camera frame."""
        return self.frame_center.copy()


class CameraFrame:
    """
    The frame that the camera looks through.
    
    This can be animated to create camera movements.
    """
    
    def __init__(self, camera: Camera):
        self.camera = camera
        self.width = camera.frame_width
        self.height = camera.frame_height
        self.center = np.array([0.0, 0.0, 0.0])
    
    def move_to(self, point):
        """Move the camera frame to a point."""
        self.center = np.array(point)
        self.camera.set_frame_center(self.center)
    
    def shift(self, vector):
        """Shift the camera frame by a vector."""
        self.center += np.array(vector)
        self.camera.set_frame_center(self.center)
    
    def scale(self, factor):
        """Scale the camera frame."""
        self.width *= factor
        self.height *= factor
