import uuid

import numpy as np


class Element:
    """A class that represents an element for wireless communication."""

    BOLTZMANN_CONSTANT = 1.380649e-23

    def __init__(self, x, y, frequency=None, bandwidth=None, transmisson_power=None, unique_id=None):
        """
        Initialize an Element object.

        :param x: float, x-coordinate of the element.
        :param y: float, y-coordinate of the element.
        :param frequency: float, frequency of the element.
        :param bandwidth: float, bandwidth of the element.
        :param transmisson_power: float, transmission power of the element.
        :param unique_id: UUID, unique identifier for the element.
        """

        self._x = x
        self._y = y
        # self._bandwidth = bandwidth
        self._bandwidth = 180e3
        self._current_capacity_in_bits_per_second = 0
        self._current_signal_to_interference_plus_noise_ratio = 0
        self._frequency = frequency
        self._number_of_resource_blocks = 0
        self._number_of_resource_blocks_received = 0
        self._receiver_temperature_in_kelvins = 290
        self._total_bits_received = 0
        self._total_bits_transmitted = 0
        # self._transmisson_power = transmisson_power
        self._transmisson_power = 40
        self._slot_duration_in_seconds = 0.5e-3
        self._unique_id = unique_id if unique_id is not None else uuid.uuid4()

    @property
    def x(self):
        """The x-coordinate of the element."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """The y-coordinate of the element."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def coordinates(self):
        """A tuple containing the x and y coordinates of the element."""
        return (self._x, self._y)

    @property
    def frequency(self):
        """The frequency of the element."""
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    @property
    def bandwidth(self):
        """The bandwidth of the element."""
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
        self._bandwidth = value

    @property
    def transmisson_power(self):
        """The transmission power of the element."""
        return self._transmisson_power

    @transmisson_power.setter
    def transmisson_power(self, value):
        self._transmisson_power = value

    @property
    def number_of_resource_blocks(self):
        return self._number_of_resource_blocks

    @number_of_resource_blocks.setter
    def number_of_resource_blocks(self, value):
        self._number_of_resource_blocks = value

    @property
    def current_signal_to_interference_plus_noise_ratio(self):
        return self._current_signal_to_interference_plus_noise_ratio

    @current_signal_to_interference_plus_noise_ratio.setter
    def current_signal_to_interference_plus_noise_ratio(self, value):
        self._current_signal_to_interference_plus_noise_ratio = value

    @property
    def current_capacity_in_bits_per_second(self):
        return self._current_capacity_in_bits_per_second

    @current_capacity_in_bits_per_second.setter
    def current_capacity_in_bits_per_second(self, value):
        self._current_capacity_in_bits_per_second = value

    @property
    def receiver_temperature_in_kelvins(self):
        return self._receiver_temperature_in_kelvins

    @receiver_temperature_in_kelvins.setter
    def receiver_temperature_in_kelvins(self, value):
        self._receiver_temperature_in_kelvins = value

    @property
    def total_bits_received(self):
        return self._total_bits_received

    @total_bits_received.setter
    def total_bits_received(self, value):
        self._total_bits_received = value

    @property
    def total_bits_transmitted(self):
        return self._total_bits_transmitted

    @total_bits_transmitted.setter
    def total_bits_transmitted(self, value):
        self._total_bits_transmitted = value

    @property
    def slot_duration_in_seconds(self):
        return self._slot_duration_in_seconds

    @slot_duration_in_seconds.setter
    def slot_duration_in_seconds(self, value):
        self._slot_duration_in_seconds = value

    @property
    def unique_id(self):
        """The unique ID of the element."""
        return self._unique_id

    @unique_id.setter
    def unique_id(self, value):
        self._unique_id = value

    @property
    def number_of_resource_blocks_received(self):
        return self._number_of_resource_blocks_received

    @number_of_resource_blocks_received.setter
    def number_of_resource_blocks_received(self, value):
        self._number_of_resource_blocks_received = value

    def receive_resource_block(self):
        """Increment the number of received resource blocks and update the total bits received."""
        C = self._current_capacity_in_bits_per_second
        Tslot = self._slot_duration_in_seconds
        self.total_bits_received += (C * Tslot)
        self._number_of_resource_blocks_received += 1

    def transmit_resource_block(self, capacity):
        """Update the total bits transmitted."""
        if capacity < 0:
            raise ValueError("Capacity must be a positive number.")
        self._total_bits_transmitted += capacity * self._slot_duration_in_seconds

    def update_signal_to_interference_plus_noise_ratio(self, intended_signal_power, interfering_signal_power):
        """Update the current signal-to-interference-plus-noise ratio (SINR)."""
        try:
            noise_power = self.calculate_noise_power()
            SINR = intended_signal_power / (interfering_signal_power + noise_power)
            self._current_signal_to_interference_plus_noise_ratio = SINR
        except ZeroDivisionError:
            self._current_signal_to_interference_plus_noise_ratio = float('inf')

    def calculate_reception_capacity(self):
        """Calculate and update the reception capacity based on the current SINR."""
        SINR = self._current_signal_to_interference_plus_noise_ratio
        BW = self._bandwidth
        capacity = BW * np.log2(1 + SINR)
        self._current_capacity_in_bits_per_second = capacity

    def calculate_noise_power(self):
        """Calculate the noise power based on the Boltzmann constant, temperature, and bandwidth."""
        k = self.BOLTZMANN_CONSTANT
        T = self._receiver_temperature_in_kelvins
        BW = self._bandwidth
        noise_power = k * T * BW
        return noise_power

    def __eq__(self, other):
        if isinstance(other, Element):
            return self.unique_id == other.unique_id
        return False