"""Base animation class."""

import numpy as np
from typing import Optional, Callable
from anymatelib.mobject.mobject import Mobject
from anymatelib.constants import DEFAULT_ANIMATION_RUN_TIME


class Animation:
    """
    Base class for all animations.
    
    An animation transforms a mobject over time.
    """
    
    def __init__(self, mobject: Mobject, run_time: float = DEFAULT_ANIMATION_RUN_TIME,
                 rate_func: Optional[Callable] = None, **kwargs):
        self.mobject = mobject
        self.run_time = run_time
        self.rate_func = rate_func or smooth
        self.starting_mobject = None
        
        # Animation state
        self.is_finished = False
        self.suspend_mobject_updating = False
    
    def begin(self):
        """Called when the animation begins."""
        self.starting_mobject = self.mobject.copy()
        self.is_finished = False
    
    def finish(self):
        """Called when the animation finishes."""
        self.interpolate(1)
        self.is_finished = True
    
    def interpolate(self, alpha: float):
        """
        Interpolate the animation at time alpha (0 to 1).
        
        Args:
            alpha: Progress through the animation (0 = start, 1 = end)
        """
        alpha = np.clip(alpha, 0, 1)
        alpha = self.rate_func(alpha)
        self.interpolate_mobject(alpha)
    
    def interpolate_mobject(self, alpha: float):
        """Override this to define animation behavior."""
        pass
    
    def update_mobjects(self, dt: float):
        """Update mobjects during animation."""
        pass
    
    def get_all_mobjects(self):
        """Return all mobjects involved in the animation."""
        return [self.mobject]
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.mobject})"


# Rate functions (easing functions)
def smooth(t: float) -> float:
    """Smooth (ease in-out) rate function."""
    return t * t * (3 - 2 * t)


def linear(t: float) -> float:
    """Linear rate function."""
    return t


def rush_into(t: float) -> float:
    """Ease in rate function."""
    return t * t


def rush_from(t: float) -> float:
    """Ease out rate function."""
    return 1 - (1 - t) * (1 - t)


def there_and_back(t: float) -> float:
    """Go there and back."""
    return 1 - abs(2 * t - 1)


def wiggle(t: float, wiggles: float = 2) -> float:
    """Wiggle back and forth."""
    return smooth(t) * np.sin(wiggles * np.pi * t)


class Wait(Animation):
    """An animation that just waits."""
    
    def __init__(self, run_time: float = 1.0, **kwargs):
        # Create a dummy mobject
        from anymatelib.mobject.mobject import Mobject
        super().__init__(Mobject(), run_time=run_time, **kwargs)
    
    def interpolate_mobject(self, alpha: float):
        pass  # Do nothing
