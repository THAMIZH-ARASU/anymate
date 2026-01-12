"""Example scenes demonstrating Anymate features."""

from anymatelib import *


class SquareToCircle(Scene):
    """Basic example: transform a square into a circle."""
    
    def construct(self):
        # Create a square
        square = Square()
        square.set_fill(BLUE, opacity=0.5)
        square.set_stroke(BLUE_E, width=4)
        
        # Add it to the scene
        self.add(square)
        self.wait(1)
        
        # Transform to circle
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        circle.set_stroke(PINK, width=4)
        
        self.play(Transform(square, circle))
        self.wait(1)


class OpeningExample(Scene):
    """Opening example with text and transformations."""
    
    def construct(self):
        # Introduction text
        intro_words = Text("""
            Anymate is a powerful animation engine
            for creating explanatory videos and
            interactive visualizations programmatically.
        """)
        intro_words.to_edge(UP)
        
        self.play(Write(intro_words))
        self.wait(2)
        
        # Create a grid
        grid = NumberPlane((-10, 10), (-5, 5))
        grid.set_stroke(BLUE_E, width=1, opacity=0.3)
        
        self.play(Create(grid))
        self.wait(1)
        
        # Create some shapes
        circle = Circle(radius=1.5)
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        
        self.play(GrowFromCenter(circle))
        self.wait(1)
        
        # Transform the grid (simplified)
        self.play(FadeOut(intro_words))
        self.wait(1)


class GeometryShapes(Scene):
    """Demonstrate various geometric shapes."""
    
    def construct(self):
        # Create shapes
        shapes = [
            Circle(radius=0.8),
            Square(side_length=1.6),
            Triangle(),
            Rectangle(width=2, height=1),
        ]
        
        # Position shapes
        for i, shape in enumerate(shapes):
            shape.shift(LEFT * 4 + RIGHT * (i * 2.5))
            shape.set_fill(BLUE, opacity=0.5)
            shape.set_stroke(BLUE_E, width=4)
        
        # Animate creation
        self.play(*[GrowFromCenter(shape) for shape in shapes])
        self.wait(2)
        
        # Change colors
        colors = [RED, GREEN, YELLOW, PURPLE]
        for shape, color in zip(shapes, colors):
            shape.set_fill(color, opacity=0.7)
        
        self.wait(1)


class AnimationShowcase(Scene):
    """Showcase different animation types."""
    
    def construct(self):
        # Title
        title = Text("Animation Showcase")
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # FadeIn
        square = Square()
        square.shift(LEFT * 3)
        square.set_fill(RED, opacity=0.5)
        self.play(FadeIn(square))
        self.wait(0.5)
        
        # GrowFromCenter
        circle = Circle()
        circle.shift(LEFT * 1)
        circle.set_fill(GREEN, opacity=0.5)
        self.play(GrowFromCenter(circle))
        self.wait(0.5)
        
        # Create
        triangle = Triangle()
        triangle.shift(RIGHT * 1)
        triangle.set_fill(BLUE, opacity=0.5)
        self.play(Create(triangle))
        self.wait(0.5)
        
        # DrawBorderThenFill
        rect = Rectangle(width=1.5, height=1.5)
        rect.shift(RIGHT * 3)
        self.play(DrawBorderThenFill(rect))
        self.wait(0.5)
        
        # Fade everything out
        self.play(
            *[FadeOut(mob) for mob in [title, square, circle, triangle, rect]]
        )
        self.wait(0.5)


class MovingShapes(Scene):
    """Demonstrate movement animations."""
    
    def construct(self):
        # Create a circle
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        
        self.add(circle)
        self.wait(0.5)
        
        # Move right
        self.play(Shift(circle, RIGHT * 3))
        self.wait(0.5)
        
        # Move up
        self.play(Shift(circle, UP * 2))
        self.wait(0.5)
        
        # Move to origin
        circle_copy = circle.copy()
        circle_copy.move_to(ORIGIN)
        self.play(Transform(circle, circle_copy))
        self.wait(0.5)
        
        # Rotate
        self.play(Rotate(circle, PI / 2))
        self.wait(0.5)
        
        # Scale
        self.play(Scale(circle, 2))
        self.wait(0.5)


class TextExample(Scene):
    """Demonstrate text rendering."""
    
    def construct(self):
        # Simple text
        text1 = Text("Hello, Anymate!")
        text1.to_edge(UP)
        
        self.play(Write(text1))
        self.wait(1)
        
        # More text
        text2 = Text("Create beautiful animations")
        text2.next_to(text1, DOWN)
        
        self.play(FadeIn(text2))
        self.wait(1)
        
        # Final text
        text3 = Text("with Python!")
        text3.next_to(text2, DOWN)
        
        self.play(Write(text3))
        self.wait(2)


class GridAndShapes(Scene):
    """Shapes on a grid."""
    
    def construct(self):
        # Create grid
        grid = NumberPlane((-7, 7), (-4, 4))
        grid.set_stroke(GREY, width=1, opacity=0.5)
        
        self.add(grid)
        self.wait(0.5)
        
        # Add dots at key points
        points = [
            ORIGIN,
            UP * 2,
            RIGHT * 3,
            DOWN * 2 + LEFT * 3,
        ]
        
        dots = [Dot(point) for point in points]
        for dot in dots:
            dot.set_fill(YELLOW, opacity=1)
        
        self.play(*[GrowFromCenter(dot) for dot in dots])
        self.wait(1)
        
        # Connect with lines
        lines = []
        for i in range(len(points)):
            line = Line(points[i], points[(i + 1) % len(points)])
            line.set_stroke(BLUE, width=4)
            lines.append(line)
        
        self.play(*[Create(line) for line in lines])
        self.wait(2)
