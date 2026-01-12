"""Scene file writer - handles video output."""

import os
import numpy as np
from pathlib import Path
from typing import Optional
from PIL import Image
from anymatelib.config import get_config


class SceneFileWriter:
    """
    Handles writing scene output to files (video, images, etc.).
    """
    
    def __init__(self, scene, **kwargs):
        self.scene = scene
        self.config = get_config()
        
        # Output settings
        self.write_to_movie = kwargs.get('write_to_movie', 
                                        self.config.get('write_to_movie', False))
        self.save_last_frame = kwargs.get('save_last_frame',
                                          self.config.get('save_last_frame', False))
        self.save_pngs = kwargs.get('save_pngs',
                                    self.config.get('save_pngs', False))
        
        # Output paths
        self.output_dir = self._get_output_dir()
        self.movie_file_path = None
        self.image_file_path = None
        
        # Frame buffer
        self.frame_count = 0
        self.frames = []  # Store frames for video creation
        
        # Get pixel dimensions
        self.pixel_width = self.config.get('pixel_width', 1920)
        self.pixel_height = self.config.get('pixel_height', 1080)
    
    def _get_output_dir(self) -> Path:
        """Get the output directory for this scene."""
        video_dir = self.config.get('video_dir', './media/videos')
        scene_name = self.scene.__class__.__name__
        
        output_dir = Path(video_dir) / scene_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return output_dir
    
    def begin(self):
        """Called at the start of rendering."""
        if self.write_to_movie:
            self._init_movie_writer()
    
    def end(self):
        """Called at the end of rendering."""
        if self.write_to_movie:
            self._finish_movie()
        
        if self.save_last_frame:
            self._save_last_frame()
    
    def _init_movie_writer(self):
        """Initialize the movie writer."""
        scene_name = self.scene.__class__.__name__
        self.movie_file_path = self.output_dir / f"{scene_name}.mp4"
        print(f"Writing to {self.movie_file_path}")
        self.frames = []
    
    def _finish_movie(self):
        """Finish writing the movie."""
        if self.movie_file_path:
            self.movie_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if self.frames:
                try:
                    # Try to create actual video using imageio
                    import imageio
                    
                    # Get frame rate from config
                    fps = self.config.get('frame_rate', 60)
                    
                    # Create video writer
                    writer = imageio.get_writer(
                        str(self.movie_file_path),
                        fps=fps,
                        codec='libx264',
                        pixelformat='yuv420p',
                        quality=8
                    )
                    
                    # Write all frames
                    for frame in self.frames:
                        writer.append_data(frame)
                    
                    writer.close()
                    
                except ImportError:
                    # Fallback: Save as animated GIF if imageio not available
                    print("Warning: imageio not installed. Saving as GIF instead.")
                    gif_path = self.movie_file_path.with_suffix('.gif')
                    
                    images = [Image.fromarray(frame) for frame in self.frames]
                    if images:
                        images[0].save(
                            str(gif_path),
                            save_all=True,
                            append_images=images[1:],
                            duration=int(1000 / self.config.get('frame_rate', 60)),
                            loop=0
                        )
                    
                    # Also save last frame as PNG
                    last_frame = self.frames[-1]
                    self._save_frame_as_image(last_frame, self.movie_file_path.with_suffix('.png'))
                    print(f"Created GIF: {gif_path}")
                
                except Exception as e:
                    print(f"Warning: Could not create video: {e}")
                    # Save last frame as PNG fallback
                    last_frame = self.frames[-1]
                    self._save_frame_as_image(last_frame, self.movie_file_path.with_suffix('.png'))
            
            print(f"Finished writing to {self.movie_file_path}")
    
    def write_frame(self, frame_data=None):
        """Write a single frame."""
        self.frame_count += 1
        
        # Create a frame from scene data
        if frame_data is None:
            frame_data = self._render_current_frame()
        
        self.frames.append(frame_data)
    
    def _render_current_frame(self):
        """Render the current frame from the scene."""
        from PIL import ImageDraw
        
        # Get background color
        bg_color = self.config.get('background_color', '#000000')
        bg_rgb = self._hex_to_rgb(bg_color)
        
        # Create a blank frame with background color
        frame = np.full((self.pixel_height, self.pixel_width, 3), bg_rgb, dtype=np.uint8)
        
        # Convert to PIL Image for drawing
        img = Image.fromarray(frame, mode='RGB')
        draw = ImageDraw.Draw(img)
        
        # Render each mobject
        for mobject in self.scene.mobjects:
            self._draw_mobject(draw, mobject)
        
        # Convert back to numpy array
        frame = np.array(img)
        return frame
    
    def _draw_mobject(self, draw, mobject):
        """Draw a mobject onto the image."""
        # Handle text mobjects specially
        if mobject.__class__.__name__ in ['Text', 'TexText', 'MathTex']:
            self._draw_text_mobject(draw, mobject)
            return
        
        if len(mobject.points) == 0:
            return
        
        # Convert world coordinates to screen coordinates
        points = self._world_to_screen(mobject.points)
        
        # Apply opacity
        opacity = int(mobject.opacity * 255) if hasattr(mobject, 'opacity') else 255
        if opacity < 10:
            return  # Skip nearly invisible objects
        
        # Draw based on mobject type
        if hasattr(mobject, 'fill_opacity') and mobject.fill_opacity > 0:
            # Draw filled shape
            fill_opacity = int(mobject.fill_opacity * 255)
            
            # Get fill color - prefer fill_color attribute
            if hasattr(mobject, 'fill_color'):
                fill_color = self._hex_to_rgb(mobject.fill_color)
            elif hasattr(mobject, 'color'):
                fill_color = self._hex_to_rgb(mobject.color)
            else:
                fill_color = (255, 255, 255)
            
            # Convert points to tuple format for PIL
            point_list = [(int(p[0]), int(p[1])) for p in points if not np.isnan(p[0])]
            
            if len(point_list) > 2:
                try:
                    draw.polygon(point_list, fill=fill_color, outline=None)
                except:
                    pass
        
        # Draw stroke
        if hasattr(mobject, 'stroke_width') and mobject.stroke_width > 0:
            stroke_width = int(mobject.stroke_width)
            
            # Get stroke color - prefer stroke_color attribute
            if hasattr(mobject, 'stroke_color'):
                stroke_color = self._hex_to_rgb(mobject.stroke_color)
            elif hasattr(mobject, 'color'):
                stroke_color = self._hex_to_rgb(mobject.color)
            else:
                stroke_color = (255, 255, 255)
            
            # Draw lines between consecutive points
            prev_point = None
            for point in points:
                if np.isnan(point[0]) or np.isnan(point[1]):
                    prev_point = None
                    continue
                
                if prev_point is not None:
                    try:
                        draw.line(
                            [(int(prev_point[0]), int(prev_point[1])), 
                             (int(point[0]), int(point[1]))],
                            fill=stroke_color,
                            width=stroke_width
                        )
                    except:
                        pass
                
                prev_point = point
        
        # Draw submobjects
        for submob in mobject.submobjects:
            self._draw_mobject(draw, submob)
    
    def _draw_text_mobject(self, draw, text_mobject):
        """Draw a text mobject onto the image."""
        from PIL import ImageFont
        
        # Get text properties
        text = getattr(text_mobject, 'text', '')
        if not text:
            return
        
        font_size = int(getattr(text_mobject, 'font_size', 48))
        
        # Get text color
        if hasattr(text_mobject, 'fill_color'):
            text_color = self._hex_to_rgb(text_mobject.fill_color)
        elif hasattr(text_mobject, 'color'):
            text_color = self._hex_to_rgb(text_mobject.color)
        else:
            text_color = (255, 255, 255)
        
        # Apply opacity
        opacity = getattr(text_mobject, 'opacity', 1.0)
        if opacity < 0.1:
            return
        
        # Get center position in world coordinates
        center = text_mobject.get_center()
        
        # Convert to screen coordinates
        screen_points = self._world_to_screen(np.array([center]))
        screen_x, screen_y = int(screen_points[0][0]), int(screen_points[0][1])
        
        # Try to load a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        text_x = screen_x - text_width // 2
        text_y = screen_y - text_height // 2
        
        # Draw the text
        draw.text((text_x, text_y), text, fill=text_color, font=font)
    
    def _world_to_screen(self, points):
        """Convert world coordinates to screen coordinates."""
        # Get frame dimensions from config
        frame_width = self.config.get('frame_width', 14.0)
        frame_height = self.config.get('frame_height', 8.0)
        
        # Scale factors
        x_scale = self.pixel_width / frame_width
        y_scale = self.pixel_height / frame_height
        
        # Convert points
        screen_points = points.copy()
        screen_points[:, 0] = screen_points[:, 0] * x_scale + self.pixel_width / 2
        screen_points[:, 1] = -screen_points[:, 1] * y_scale + self.pixel_height / 2  # Flip Y axis
        
        return screen_points
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple."""
        if not isinstance(hex_color, str):
            return (255, 255, 255)
        
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (255, 255, 255)
    
    def _save_frame_as_image(self, frame_data, file_path):
        """Save a frame as an image file."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.fromarray(frame_data, mode='RGB')
        img.save(str(file_path))
    
    def _save_last_frame(self):
        """Save the last frame as an image."""
        scene_name = self.scene.__class__.__name__
        image_dir = Path(self.config.get('image_dir', './media/images'))
        image_dir.mkdir(parents=True, exist_ok=True)
        
        self.image_file_path = image_dir / f"{scene_name}.png"
        print(f"Saving last frame to {self.image_file_path}")
        
        # Create and save a sample image
        if self.frames:
            frame = self.frames[-1]
        else:
            frame = self._render_current_frame()
        
        self._save_frame_as_image(frame, self.image_file_path)
    
    def get_movie_file_path(self) -> Optional[Path]:
        """Get the path to the output movie file."""
        return self.movie_file_path
