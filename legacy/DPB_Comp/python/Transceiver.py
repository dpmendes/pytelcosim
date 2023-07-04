import numpy as np


class Transceiver:
    """A class that represents a transceiver for wireless communication."""
    BOLTZMANN_CONSTANT = 1.38064852e-23

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.number_of_resource_blocks_received = 0
        self.transmit_power_in_watts = 0
        self.current_signal_to_interference_plus_noise_ratio = 0
        self.current_capacity_in_bits_per_second = 0
        self.bandwidth_in_hertz = 180e3
        self.receiver_temperature_in_kelvins = 290
        self.total_bits_received = 0
        self.total_bits_transmitted = 0
        self.slot_duration_in_seconds = 0.5e-3

    def set_position(self, x, y):
        """Set the position of the transceiver."""
        self.x = x
        self.y = y

    def get_position(self):
        """Return the position of the transceiver as a tuple."""
        return self.x, self.y

    def get_transmit_power_in_watts(self):
        """Return the current transmit power in watts."""
        return self.transmit_power_in_watts

    def set_transmit_power_in_watts(self, transmit_power):
        """Set the transmit power in watts."""
        self.transmit_power_in_watts = transmit_power

    def receive_resource_block(self):
        """Increment the number of received resource blocks and update the total bits received."""
        C = self.current_capacity_in_bits_per_second
        Tslot = self.slot_duration_in_seconds
        self.total_bits_received += (C * Tslot)
        self.number_of_resource_blocks_received += 1

    def transmit_resource_block(self, capacity):
        """Update the total bits transmitted."""
        self.total_bits_transmitted += capacity * self.slot_duration_in_seconds

    def update_signal_to_interference_plus_noise_ratio(self, intended_signal_power, interfering_signal_power):
        """Update the current signal-to-interference-plus-noise ratio (SINR)."""
        noise_power = self.calculate_noise_power()
        SINR = intended_signal_power / (interfering_signal_power + noise_power)
        self.current_signal_to_interference_plus_noise_ratio = SINR

    def calculate_reception_capacity(self):
        """Calculate and update the reception capacity based on the current SINR."""
        SINR = self.current_signal_to_interference_plus_noise_ratio
        BW = self.bandwidth_in_hertz
        capacity = BW * np.log2(1 + SINR)
        self.current_capacity_in_bits_per_second = capacity

    def get_current_capacity_in_bits_per_second(self):
        """Return the current capacity in bits per second."""
        return self.current_capacity_in_bits_per_second

    def calculate_noise_power(self):
        """Calculate the noise power based on the Boltzmann constant, temperature, and bandwidth."""
        k = self.BOLTZMANN_CONSTANT
        T = self.receiver_temperature_in_kelvins
        BW = self.bandwidth_in_hertz
        noise_power = k * T * BW
        return noise_power
