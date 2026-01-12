# Anymate Project Structure

## Overview
Anymate is a Python-based animation engine for creating explanatory videos and interactive visualizations programmatically.

## Directory Structure

```
anymate/
├── anymatelib/                     # Main library directory
│   ├── __init__.py                # Package exports
│   ├── __main__.py                # CLI entry point
│   ├── constants.py               # System constants (colors, directions, etc.)
│   ├── config.py                  # Configuration management
│   ├── default_config.yml         # Default configuration
│   ├── extract_scene.py           # Scene extraction and execution
│   ├── shader_wrapper.py          # OpenGL shader management
│   ├── window.py                  # Interactive playback window
│   │
│   ├── camera/                    # Camera system
│   │   ├── __init__.py
│   │   └── camera.py             # Camera and CameraFrame classes
│   │
│   ├── scene/                     # Scene management
│   │   ├── __init__.py
│   │   ├── scene.py              # Base Scene class
│   │   ├── scene_file_writer.py  # Video file output
│   │   └── three_d_scene.py      # 3D scene support
│   │
│   ├── animation/                 # Animation system
│   │   ├── __init__.py
│   │   ├── animation.py          # Base animation class & rate functions
│   │   ├── creation.py           # Creation animations (Create, Write, FadeIn, etc.)
│   │   └── transform.py          # Transform animations (Transform, Rotate, Scale, etc.)
│   │
│   ├── mobject/                   # Visual objects
│   │   ├── __init__.py
│   │   ├── mobject.py            # Base Mobject class
│   │   ├── geometry.py           # Geometric shapes (Circle, Square, etc.)
│   │   │
│   │   ├── types/                # Mobject types
│   │   │   ├── __init__.py
│   │   │   └── vectorized_mobject.py  # VMobject for smooth curves
│   │   │
│   │   └── svg/                  # SVG-based objects
│   │       ├── __init__.py
│   │       └── text_mobject.py   # Text, TexText, MathTex
│   │
│   ├── shaders/                   # GLSL shader programs
│   │   ├── simple_vert.glsl      # Basic vertex shader
│   │   └── simple_frag.glsl      # Basic fragment shader
│   │
│   └── tex_templates/             # LaTeX templates (empty for now)
│
├── example_scenes.py              # Example scenes demonstrating features
├── setup.py                       # Package setup script
├── setup.cfg                      # Package configuration
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview
├── QUICKSTART.md                  # Quick start guide
└── venv/                          # Virtual environment (not in git)
```

## Core Components

### 1. Constants (`constants.py`)
- Mathematical constants (PI, TAU, DEGREES)
- Direction vectors (UP, DOWN, LEFT, RIGHT, ORIGIN, etc.)
- Color definitions (RED, GREEN, BLUE, etc.)
- Default sizes and animation settings

### 2. Configuration System (`config.py`, `default_config.yml`)
- Layered configuration with defaults and overrides
- Frame settings (width, height, pixel dimensions)
- Quality presets (low, medium, high, ultra)
- Output settings (video dir, frame rate, etc.)

### 3. Mobject System (`mobject/`)
- **Mobject**: Base class for all visual objects
  - Position, rotation, scale
  - Color and opacity
  - Submobjects hierarchy
  - State saving/restoration

- **VMobject**: Vectorized objects with bezier curves
  - Stroke and fill properties
  - Point-based rendering

- **Geometry**: Built-in shapes
  - Circle, Square, Rectangle, Triangle
  - Line, Arrow, Dot
  - NumberPlane (coordinate grid)

- **Text**: Text rendering
  - Text, TexText, MathTex
  - (Simplified implementation - full version uses manimpango)

### 4. Animation System (`animation/`)
- **Animation**: Base class for all animations
  - Time interpolation (0 to 1)
  - Rate functions (easing)
  - Begin, update, finish lifecycle

- **Rate Functions**:
  - smooth (ease in-out)
  - linear
  - rush_into (ease in)
  - rush_from (ease out)
  - there_and_back
  - wiggle

- **Creation Animations**:
  - Create, Write: Draw/write objects
  - FadeIn, FadeOut: Opacity changes
  - GrowFromCenter: Scale from center
  - DrawBorderThenFill: Draw then fill
  - Uncreate: Reverse creation

- **Transform Animations**:
  - Transform: Morph one object to another
  - ReplacementTransform: Replace during transform
  - MoveToTarget: Move to target position
  - ApplyMethod: Apply method over time
  - Rotate, Shift, Scale: Basic transformations

### 5. Scene System (`scene/`)
- **Scene**: Base scene class
  - Mobject management (add, remove, clear)
  - Animation playback (play, wait)
  - Setup and teardown hooks
  - Rendering coordination

- **ThreeDScene**: 3D scene support
  - 3D camera positioning
  - Spherical coordinates
  - Ambient camera rotation

- **SceneFileWriter**: Output management
  - Video file writing
  - Image output
  - Frame buffer management
  - Directory structure creation

### 6. Camera System (`camera/`)
- **Camera**: View and projection
  - Frame dimensions
  - Pixel dimensions
  - Background color
  - World-to-screen coordinate conversion

- **CameraFrame**: Animatable camera frame
  - Position and movement
  - Scaling (zoom)

### 7. Rendering Pipeline (`shader_wrapper.py`, `window.py`)
- **ShaderWrapper**: OpenGL shader management
  - Program creation
  - Uniform variables
  - Primitive rendering
  - (Simplified - full version uses ModernGL)

- **Renderer**: Main rendering system
  - Shader initialization
  - Mobject rendering
  - Screen clearing
  - Buffer swapping

- **Window**: Interactive preview
  - Window creation and management
  - Input handling
  - Event loop
  - (Simplified - full version uses moderngl_window)

### 8. CLI System (`__main__.py`, `extract_scene.py`)
- **extract_scene**: Scene discovery and execution
  - Load Python files
  - Extract Scene classes
  - Scene instantiation
  - Rendering coordination

- **__main__**: Command-line interface
  - Argument parsing
  - Configuration application
  - Scene selection
  - Output handling

## Example Scenes

The `example_scenes.py` file contains 7 demonstration scenes:

1. **SquareToCircle**: Basic shape transformation
2. **OpeningExample**: Text, grid, and transformations
3. **GeometryShapes**: Multiple geometric shapes
4. **AnimationShowcase**: Various animation types
5. **MovingShapes**: Movement and transformations
6. **TextExample**: Text rendering
7. **GridAndShapes**: Grid with connected shapes

## Usage Workflow

1. **Import**: `from anymatelib import *`
2. **Create Scene Class**: Inherit from `Scene`
3. **Implement construct()**: Define animations
4. **Run**: `python -m anymatelib file.py SceneName`

## Key Features Implemented

✅ Mobject hierarchy system
✅ Animation framework with rate functions
✅ Scene management and rendering coordination
✅ Camera system with transformations
✅ Configuration management
✅ CLI with comprehensive options
✅ Example scenes demonstrating features
✅ Quality presets (low, medium, high, ultra)
✅ Multiple output formats (video, images)
✅ Geometric shapes (circles, squares, etc.)
✅ Text rendering (simplified)
✅ 3D scene support (basic)
✅ OpenGL shader infrastructure (simplified)

## Future Enhancements (Not Yet Implemented)

- Full OpenGL rendering with ModernGL
- Real-time preview window with moderngl_window
- LaTeX rendering with actual compilation
- Text rendering with manimpango
- SVG import and rendering
- Advanced 3D graphics
- Interactive controls
- Timeline scrubbing
- More animation types
- Graph plotting
- Vector field visualization
- Surface rendering

## Testing

The project has been tested with:
- Package installation: ✅
- Scene listing: ✅
- Basic rendering: ✅
- Video output: ✅
- Last frame saving: ✅
- Skip animations: ✅

## Dependencies

Core dependencies installed:
- moderngl (OpenGL rendering)
- moderngl-window (Window management)
- numpy (Numerical computations)
- Pillow (Image processing)
- manimpango (Text rendering)
- PyOpenGL (OpenGL bindings)
- matplotlib (Plotting)
- scipy (Scientific computing)
- pyyaml (Configuration)
- click (CLI framework)
- rich (Terminal formatting)

## Notes

This is a foundational implementation of the Anymate engine. The core architecture is in place:
- Object system (Mobjects)
- Animation system
- Scene management
- Configuration system
- CLI interface

The rendering pipeline is simplified. A full implementation would:
- Use ModernGL for actual GPU rendering
- Implement proper shader programs
- Use FFmpeg for video encoding
- Add interactive window with controls
- Implement full LaTeX compilation
- Add proper text rendering with Pango

The current implementation provides a solid foundation for educational purposes and can be extended with full rendering capabilities.
