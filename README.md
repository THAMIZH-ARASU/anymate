# Anymate Animation Engine

A powerful Python-based animation engine for creating explanatory videos and interactive visualizations programmatically.

## Features

- GPU-accelerated rendering with OpenGL
- Comprehensive animation framework
- Interactive development workflow
- Support for 2D and 3D graphics
- Mathematical visualization tools
- Text and LaTeX rendering
- Export to video or image sequences

## Installation

```bash
cd anymate
pip install -e .
```

## Quick Start

```python
from anymatelib import *

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        self.add(circle)
```

Run the scene:

```bash
anymate example_scenes.py SquareToCircle
```

## License

MIT License
