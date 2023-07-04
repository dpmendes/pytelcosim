import numpy as np
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.freespacechannel import FreeSpaceChannel

class TestFreeSpaceChannel(unittest.TestCase):

    def test_wavelength_calculation(self):
        frequency = 3e9  # 3 GHz
        channel = FreeSpaceChannel(frequency)
        expected_wavelength = 0.1  # meters
        self.assertAlmostEqual(channel.wavelength_in_meters, expected_wavelength, places=2)

    def test_calculate_gain(self):
        frequency = 3e9  # 3 GHz
        channel = FreeSpaceChannel(frequency)
        distance = 100  # meters
        expected_gain = 3.388e-14
        calculated_gain = channel.calculate_gain(distance)
        self.assertAlmostEqual(calculated_gain, expected_gain, places=14)

    def test_calculate_gain_in_db(self):
        frequency = 3e9  # 3 GHz
        channel = FreeSpaceChannel(frequency)
        distance = 100  # meters
        expected_gain_db = -153.98  # dB
        calculated_gain_db = channel.calculate_gain_in_db(distance)
        self.assertAlmostEqual(calculated_gain_db, expected_gain_db, places=2)

if __name__ == '__main__':
    unittest.main()
