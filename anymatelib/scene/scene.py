"""Base Scene class."""

import numpy as np
from typing import List, Optional
from anymatelib.mobject.mobject import Mobject
from anymatelib.animation.animation import Animation, Wait
from anymatelib.camera.camera import Camera
from anymatelib.config import get_config
from anymatelib.constants import *


class Scene:
    """
    Base class for all scenes.
    
    A scene is a container for mobjects and animations.
    Override the construct() method to define your scene.
    """
    
    def __init__(self, **kwargs):
        self.config = get_config()
        
        # Camera setup
        self.camera = Camera(**kwargs)
        
        # Scene state
        self.mobjects = []
        self.time = 0
        self.animations = []
        
        # Rendering
        self.renderer = None
        self.file_writer = None
        
        # Skip animations flag
        self.skip_animations = False
    
    def construct(self):
        """
        Override this method to define your scene.
        
        Example:
            def construct(self):
                circle = Circle()
                self.play(Create(circle))
                self.wait()
        """
        pass
    
    def setup(self):
        """Called before construct(). Override to set up the scene."""
        pass
    
    def tear_down(self):
        """Called after construct(). Override to clean up."""
        pass
    
    # Mobject management
    def add(self, *mobjects: Mobject):
        """Add mobjects to the scene."""
        for mobject in mobjects:
            if mobject not in self.mobjects:
                self.mobjects.append(mobject)
        return self
    
    def remove(self, *mobjects: Mobject):
        """Remove mobjects from the scene."""
        for mobject in mobjects:
            if mobject in self.mobjects:
                self.mobjects.remove(mobject)
        return self
    
    def clear(self):
        """Remove all mobjects from the scene."""
        self.mobjects = []
        return self
    
    def get_mobjects(self) -> List[Mobject]:
        """Get all mobjects in the scene."""
        return self.mobjects.copy()
    
    # Animation methods
    def play(self, *animations: Animation, **kwargs):
        """
        Play one or more animations.
        
        Args:
            *animations: Animations to play simultaneously
            **kwargs: Additional options (run_time, etc.)
        """
        if len(animations) == 0:
            return
        
        # Convert single animation to list
        if not isinstance(animations[0], Animation):
            # Handle case where user passes mobject instead of animation
            raise TypeError("play() requires Animation objects")
        
        # Get run time
        run_time = kwargs.get('run_time', animations[0].run_time)
        
        # Add mobjects if not already in scene
        for anim in animations:
            for mob in anim.get_all_mobjects():
                if mob not in self.mobjects:
                    self.add(mob)
        
        # Begin all animations
        for anim in animations:
            anim.begin()
        
        if self.skip_animations:
            # Skip to end
            for anim in animations:
                anim.finish()
            
            # Write final frame
            if self.file_writer:
                self.file_writer.write_frame()
        else:
            # Animate
            frame_rate = self.config.get('frame_rate', DEFAULT_FRAME_RATE)
            num_frames = int(run_time * frame_rate)
            
            for frame in range(num_frames + 1):
                alpha = frame / num_frames if num_frames > 0 else 1
                
                for anim in animations:
                    anim.interpolate(alpha)
                
                # Render frame
                if self.renderer:
                    self.renderer.render(self.mobjects)
                
                # Write frame to file if file writer is active
                if self.file_writer:
                    self.file_writer.write_frame()
                
                self.time += 1 / frame_rate
            
            # Finish animations
            for anim in animations:
                anim.finish()
        
        return self
    
    def wait(self, duration: float = DEFAULT_WAIT_TIME):
        """Wait for a duration."""
        self.play(Wait(run_time=duration))
        return self
    
    def render(self):
        """Render the entire scene."""
        # Setup
        self.setup()
        
        # Write initial frame if file writer is active
        if self.file_writer:
            self.file_writer.write_frame()
        
        # Run construct
        self.construct()
        
        # Write final frame
        if self.file_writer:
            self.file_writer.write_frame()
        
        # Tear down
        self.tear_down()
    
    def __repr__(self):
        return f"{self.__class__.__name__}()"
