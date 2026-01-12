"""Interactive window for scene preview."""

from typing import Optional
from anymatelib.config import get_config


class Window:
    """
    Interactive window for previewing scenes.
    
    In a full implementation, this would use moderngl_window or pyglet.
    """
    
    def __init__(self, scene, **kwargs):
        self.scene = scene
        self.config = get_config()
        
        # Window settings
        self.width = kwargs.get('width', self.config.get('window_size', [1280, 720])[0])
        self.height = kwargs.get('height', self.config.get('window_size', [1280, 720])[1])
        self.title = kwargs.get('title', f"Anymate - {scene.__class__.__name__}")
        self.fullscreen = kwargs.get('fullscreen', self.config.get('fullscreen', False))
        
        # State
        self.is_running = False
        self.is_paused = False
    
    def open(self):
        """Open the window."""
        print(f"Opening window: {self.title} ({self.width}x{self.height})")
        self.is_running = True
    
    def close(self):
        """Close the window."""
        self.is_running = False
    
    def run(self):
        """Run the main window loop."""
        self.open()
        
        # In full implementation, would have event loop here
        # For now, just render the scene
        self.scene.render()
        
        print("Scene rendering complete")
    
    def handle_input(self, key: str, action: str):
        """
        Handle keyboard/mouse input.
        
        Args:
            key: Key pressed
            action: Action (press, release, etc.)
        """
        if key == 'space' and action == 'press':
            self.is_paused = not self.is_paused
        elif key == 'q' and action == 'press':
            self.close()
    
    def update(self, dt: float):
        """Update the window state."""
        if not self.is_paused:
            # Update scene
            pass
    
    def render(self):
        """Render the current frame."""
        # In full implementation, would render with OpenGL
        pass


class InteractiveWindow(Window):
    """
    Enhanced window with interactive controls.
    
    Supports camera control, timeline scrubbing, etc.
    """
    
    def __init__(self, scene, **kwargs):
        super().__init__(scene, **kwargs)
        
        # Interactive features
        self.camera_control_enabled = True
        self.show_timeline = True
        self.current_time = 0.0
    
    def handle_input(self, key: str, action: str):
        """Handle interactive controls."""
        super().handle_input(key, action)
        
        if key == 'left' and action == 'press':
            # Scrub backward
            self.current_time = max(0, self.current_time - 0.1)
        elif key == 'right' and action == 'press':
            # Scrub forward
            self.current_time += 0.1
