import numpy as np
from src.channel import Channel


class FreeSpaceChannel(Channel):
    def __init__(self, frequency_in_hertz):
        """Initialize the FreeSpaceChannel with a given frequency."""
        super().__init__(frequency_in_hertz)

    def calculate_gain_in_db(self, distance_in_meters):
        """Calculate and return the channel gain in decibels for a given distance in meters."""
        gain_in_db = 10 * np.log10(self.calculate_gain(distance_in_meters))
        return gain_in_db

    def calculate_gain(self, distance_in_meters):
        """Calculate and return the channel gain for a given distance in meters."""
        lambda_ = self.wavelength_in_meters
        Gt = self.transmit_antenna_gain
        Gr = self.receive_antenna_gain
        d = distance_in_meters

        if d == 0:
            gain = np.inf
        else:
            gain = (Gt * Gr * (lambda_ ** 2)) / \
                ((4 * np.pi * d) ** 2)
        return gain
