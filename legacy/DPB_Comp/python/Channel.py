from abc import ABC, abstractmethod


class Channel(ABC):

    speed_of_light_in_meters_per_second = 3e8

    def __init__(self, frequency_in_hertz):
        self.frequency_in_hertz = frequency_in_hertz
        self.transmit_antenna_gain = 1
        self.receive_antenna_gain = 1

    @property
    def wavelength_in_meters(self):
        c = self.speed_of_light_in_meters_per_second
        f = self.frequency_in_hertz

        lambda_ = c / f

        return lambda_

    @abstractmethod
    def calculate_gain(self, distance_in_meters):
        pass
