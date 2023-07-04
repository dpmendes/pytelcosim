import unittest
from src.element import Element


class TestElement(unittest.TestCase):

    def setUp(self):
        self.element = Element(1, 2, 700e6, 180e3, 10)

    def test_element_creation(self):
        """Test if the Element object is created with correct initial values."""

        element = self.element

        self.assertEqual(element.x, 1)
        self.assertEqual(element.y, 2)
        self.assertEqual(element.frequency, 700e6)
        self.assertEqual(element.bandwidth, 180e3)
        self.assertEqual(element.transmisson_power, 10)

    def test_element_setters(self):
        """Test if the Element object's properties can be updated using setters."""
        element = Element(0, 0)

        element.x = 3
        element.y = 4
        element.frequency = 740e6
        element.bandwidth = 100e3
        element.transmisson_power = 20
        element.number_of_resource_blocks = 3
        element.current_signal_to_interference_plus_noise_ratio = -10
        element.current_capacity_in_bits_per_second = 100e3
        element.receiver_temperature_in_kelvins = 280
        element.total_bits_received = 1024
        element.total_bits_transmitted = 512
        element.slot_duration_in_seconds = 1e-3

        self.assertEqual(element.x, 3)
        self.assertEqual(element.y, 4)
        self.assertEqual(element.frequency, 740e6)
        self.assertEqual(element.bandwidth, 100e3)
        self.assertEqual(element.transmisson_power, 20)
        self.assertEqual(
            element.current_signal_to_interference_plus_noise_ratio, -10)
        self.assertEqual(element.current_capacity_in_bits_per_second, 100e3)
        self.assertEqual(element.receiver_temperature_in_kelvins, 280)
        self.assertEqual(element.total_bits_received, 1024)
        self.assertEqual(element.total_bits_transmitted, 512)
        self.assertEqual(element.slot_duration_in_seconds, 1e-3)

    def test_element_coordinates(self):
        """Test if the Element object's coordinates can be updated."""
        element = self.element
        element.coordinates = (3, 4)

        self.assertEqual(element.coordinates, (3, 4))
        self.assertEqual(element.x, 3)
        self.assertEqual(element.y, 4)


if __name__ == '__main__':
    unittest.main()


# import unittest
# import numpy as np
# from transceiver import Transceiver

# class TestTransceiver(unittest.TestCase):
#     def setUp(self):
#         self.transceiver = Transceiver(0, 0)

#     def test_set_position(self):
#         self.transceiver.set_position(1, 1)
#         self.assertEqual(self.transceiver.get_position(), (1, 1))

#     def test_get_position(self):
#         self.assertEqual(self.transceiver.get_position(), (0, 0))

#     def test_transmit_power(self):
#         self.transceiver.set_transmit_power_in_watts(10)
#         self.assertEqual(self.transceiver.get_transmit_power_in_watts(), 10)

#     def test_receive_resource_block(self):
#         self.transceiver.set_transmit_power_in_watts(10)
#         self.transceiver.update_signal_to_interference_plus_noise_ratio(10, 0)
#         self.transceiver.calculate_reception_capacity()
#         self.transceiver.receive_resource_block()
#         self.assertEqual(self.transceiver.number_of_resource_blocks_received, 1)

#     def test_transmit_resource_block(self):
#         self.transceiver.transmit_resource_block(100)
#         self.assertAlmostEqual(self.transceiver.total_bits_transmitted, 50)

#     def test_update_signal_to_interference_plus_noise_ratio(self):
#         self.transceiver.set_transmit_power_in_watts(10)
#         self.transceiver.update_signal_to_interference_plus_noise_ratio(10, 0)
#         SINR = 10 / self.transceiver.calculate_noise_power()
#         self.assertAlmostEqual(self.transceiver.current_signal_to_interference_plus_noise_ratio, SINR)

#     def test_calculate_reception_capacity(self):
#         self.transceiver.set_transmit_power_in_watts(10)
#         self.transceiver.update_signal_to_interference_plus_noise_ratio(10, 0)
#         self.transceiver.calculate_reception_capacity()
#         SINR = 10 / self.transceiver.calculate_noise_power()
#         capacity = self.transceiver.bandwidth_in_hertz * np.log2(1 + SINR)
#         self.assertAlmostEqual(self.transceiver.current_capacity_in_bits_per_second, capacity)

#     def test_get_current_capacity_in_bits_per_second(self):
#         self.transceiver.set_transmit_power_in_watts(10)
#         self.transceiver.update_signal_to_interference_plus_noise_ratio(10, 0)
#         self.transceiver.calculate_reception_capacity()
#         capacity = self.transceiver.get_current_capacity_in_bits_per_second()
#         self.assertAlmostEqual(self.transceiver.current_capacity_in_bits_per_second, capacity)

#     def test_calculate_noise_power(self):
#         noise_power = self.transceiver.calculate_noise_power()
#         expected_noise_power = Transceiver.BOLTZMANN_CONSTANT * self.transceiver.receiver_temperature_in_kelvins * self.transceiver.bandwidth_in_hertz
#         self.assertAlmostEqual(noise_power, expected_noise_power)

# if __name__ == '__main__':
#     unittest.main()
