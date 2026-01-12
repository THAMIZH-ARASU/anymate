"""Scene extraction and execution."""

import sys
import importlib.util
from pathlib import Path
from typing import Optional, Type
from anymatelib.scene.scene import Scene


def get_scene_classes_from_file(file_path: str):
    """
    Extract all Scene classes from a Python file.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Dictionary of scene name -> scene class
    """
    # Load the module
    file_path = Path(file_path).resolve()
    spec = importlib.util.spec_from_file_location("scene_module", file_path)
    
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules["scene_module"] = module
    spec.loader.exec_module(module)
    
    # Find all Scene subclasses
    scene_classes = {}
    for name in dir(module):
        obj = getattr(module, name)
        if (isinstance(obj, type) and 
            issubclass(obj, Scene) and 
            obj is not Scene):
            scene_classes[name] = obj
    
    return scene_classes


def get_scene_class(file_path: str, scene_name: Optional[str] = None) -> Type[Scene]:
    """
    Get a specific scene class from a file.
    
    Args:
        file_path: Path to the Python file
        scene_name: Name of the scene class (optional)
        
    Returns:
        The scene class
    """
    scene_classes = get_scene_classes_from_file(file_path)
    
    if not scene_classes:
        raise ValueError(f"No Scene classes found in {file_path}")
    
    if scene_name is None:
        # Return the first scene found
        return list(scene_classes.values())[0]
    
    if scene_name not in scene_classes:
        available = ", ".join(scene_classes.keys())
        raise ValueError(
            f"Scene '{scene_name}' not found in {file_path}. "
            f"Available scenes: {available}"
        )
    
    return scene_classes[scene_name]


def list_scenes(file_path: str):
    """
    List all scenes in a file.
    
    Args:
        file_path: Path to the Python file
    """
    scene_classes = get_scene_classes_from_file(file_path)
    
    if not scene_classes:
        print(f"No Scene classes found in {file_path}")
        return
    
    print(f"Scenes in {file_path}:")
    for name in scene_classes:
        print(f"  - {name}")


def render_scene(scene_class: Type[Scene], **kwargs):
    """
    Render a scene.
    
    Args:
        scene_class: The scene class to render
        **kwargs: Additional rendering options
    """
    # Create scene instance
    scene = scene_class(**kwargs)
    
    # Set up file writer if needed
    if kwargs.get('write_to_movie', False):
        from anymatelib.scene.scene_file_writer import SceneFileWriter
        scene.file_writer = SceneFileWriter(scene, **kwargs)
        scene.file_writer.begin()
    
    # Set skip animations flag
    scene.skip_animations = kwargs.get('skip_animations', False)
    
    # Render
    try:
        scene.render()
    finally:
        if scene.file_writer:
            scene.file_writer.end()
    
    return scene
