# Anymate Quick Start Guide

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd anymate
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\Activate.ps1
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Anymate:**
   ```bash
   pip install -e .
   ```

## Basic Usage

### List Available Scenes
```bash
python -m anymatelib example_scenes.py -l
```

### Render a Scene (Preview Only)
```bash
python -m anymatelib example_scenes.py SquareToCircle
```

### Render to Video
```bash
python -m anymatelib example_scenes.py SquareToCircle -w
```

### Skip Animations (Show Final Frame)
```bash
python -m anymatelib example_scenes.py SquareToCircle -s
```

### Save Last Frame as Image
```bash
python -m anymatelib example_scenes.py SquareToCircle --save_last_frame
```

## Creating Your First Scene

Create a new file `my_scene.py`:

```python
from anymatelib import *

class MyFirstScene(Scene):
    def construct(self):
        # Create a circle
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        
        # Add and animate
        self.play(Create(circle))
        self.wait()
        
        # Transform to square
        square = Square()
        square.set_fill(RED, opacity=0.5)
        self.play(Transform(circle, square))
        self.wait()
```

Render it:
```bash
python -m anymatelib my_scene.py MyFirstScene -w
```

## Command-Line Options

### Quality Presets
- `-ql` or `--quality_low`: 480p15
- `-qm` or `--quality_medium`: 720p30
- `-qh` or `--quality_high`: 1080p60 (default)
- `-qk` or `--quality_ultra`: 4K60

### Output Options
- `-w` or `--write_file`: Render to video file
- `-o` or `--open`: Write and open the result
- `-s` or `--skip_animations`: Skip to final frame
- `--save_last_frame`: Save last frame as PNG
- `--save_pngs`: Save all frames as PNGs
- `--save_as_gif`: Save as GIF
- `--transparent`: Render with transparent background

### Window Options
- `-f` or `--full_screen`: Show in fullscreen
- `-p` or `--presenter_mode`: Interactive presentation mode
- `--no_preview`: Disable preview window

### Custom Resolution
```bash
python -m anymatelib example_scenes.py SquareToCircle -r 1280x720
```

### Custom Frame Rate
```bash
python -m anymatelib example_scenes.py SquareToCircle --fps 30
```

## Available Example Scenes

1. **SquareToCircle** - Basic shape transformation
2. **OpeningExample** - Introduction with text and grid
3. **GeometryShapes** - Various geometric shapes
4. **AnimationShowcase** - Different animation types
5. **MovingShapes** - Movement and transformation
6. **TextExample** - Text rendering
7. **GridAndShapes** - Grid with connected shapes

## Key Concepts

### Mobjects (Mathematical Objects)
- `Circle()`, `Square()`, `Rectangle()`, `Triangle()`
- `Line()`, `Arrow()`, `Dot()`
- `Text()`, `TexText()`, `MathTex()`
- `NumberPlane()` - coordinate grid

### Animations
- **Creation**: `Create()`, `Write()`, `FadeIn()`, `GrowFromCenter()`
- **Transform**: `Transform()`, `ReplacementTransform()`
- **Movement**: `Shift()`, `Rotate()`, `Scale()`
- **Fade**: `FadeIn()`, `FadeOut()`

### Scene Methods
- `self.add(mobject)` - Add mobject to scene
- `self.remove(mobject)` - Remove mobject from scene
- `self.play(animation)` - Play an animation
- `self.wait(duration)` - Wait for duration

### Positioning
- `mobject.move_to(point)` - Move to specific point
- `mobject.shift(vector)` - Shift by vector
- `mobject.to_edge(direction)` - Move to edge (UP, DOWN, LEFT, RIGHT)
- `mobject.next_to(other, direction)` - Position next to another object

### Styling
- `mobject.set_color(color)` - Set color
- `mobject.set_fill(color, opacity)` - Set fill
- `mobject.set_stroke(color, width, opacity)` - Set stroke

### Constants
- **Directions**: `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`
- **Colors**: `RED`, `GREEN`, `BLUE`, `YELLOW`, `ORANGE`, `PURPLE`, `PINK`, `WHITE`, `BLACK`
- **Math**: `PI`, `TAU`, `DEGREES`

## Output Structure

```
anymate/
├── media/
│   ├── videos/
│   │   └── SceneName/
│   │       └── SceneName.mp4
│   ├── images/
│   │   └── SceneName.png
│   └── Tex/
```

## Tips

1. **Start Simple**: Begin with basic shapes and animations
2. **Use Skip Animations**: Test quickly with `-s` flag
3. **Chain Animations**: Use multiple arguments in `self.play()`
4. **Save Iterations**: Use `--save_last_frame` to save progress
5. **Explore Examples**: Study the example_scenes.py file

## Troubleshooting

### Import Errors
Make sure the virtual environment is activated:
```bash
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux
```

### Scene Not Found
List available scenes first:
```bash
python -m anymatelib your_file.py -l
```

### Performance Issues
- Use lower quality preset: `-ql` or `-qm`
- Skip animations during development: `-s`
- Reduce frame rate: `--fps 15`

## Next Steps

1. Explore all example scenes
2. Read through the mobject and animation classes
3. Create your own custom scenes
4. Experiment with different animations and transformations
5. Try 3D scenes with `ThreeDScene`

For more information, explore the source code in the `anymatelib/` directory.
