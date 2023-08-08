import random
from element import Element


class ElementCreator():
    """A class for creating Element objects with random or fixed positions."""

    def __init__(self, upper_x_bound=0, upper_y_bound=0):
        """Initialize the ElementCreator with the given upper bounds for x and y coordinates."""
        if upper_x_bound < 0 or upper_y_bound < 0:
            raise ValueError("Upper bounds must be positive numbers.")
        self._upper_x_bound = upper_x_bound
        self._upper_y_bound = upper_y_bound

    def _draw_position(self, _coordinate):
        """Return a random position within the range of [0, _coordinate]."""
        return random.uniform(0, _coordinate)

    def create_random_element(self,upper_x_bound, upper_y_bound, frequency=None):
        """Create an Element object with random x and y coordinates within the specified bounds and an optional frequency."""
        if upper_x_bound < 0 or upper_y_bound < 0:
            raise ValueError("Upper bounds must be positive numbers.")
        return Element(self._draw_position(self._upper_x_bound), self._draw_position(self._upper_y_bound), frequency)

    def create_fixed_element(self, x, y, frequency=None):

        """Create an Element object with fixed x and y coordinates and an optional frequency.
        Parameters:
        x (float): The x-coordinate of the Element.
        y (float): The y-coordinate of the Element.
        frequency (Optional[float]): The frequency of the Element. Defaults to None.

        Returns:
        Element: An Element object with the specified coordinates and frequency.
        """
        if x < 0 or y < 0:
            raise ValueError("Upper bounds must be positive numbers.")
        return Element(x, y, frequency)
