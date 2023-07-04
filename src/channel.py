from abc import ABC, abstractmethod


class Channel(ABC):

    SPEED_OF_LIGHT_IN_METERS_PER_SECOND = 3e8

    def __init__(self, frequency_in_hertz: float):
        """
        Initialize the Channel with a given frequency.

        :param frequency_in_hertz: The frequency of the channel in Hertz.
        """
        self.frequency_in_hertz = frequency_in_hertz
        self.transmit_antenna_gain = 1
        self.receive_antenna_gain = 1

    @property
    def wavelength_in_meters(self) -> float:
        """
        Calculate and return the wavelength of the channel in meters.

        :return: The wavelength of the channel in meters.
        """
        c = self.SPEED_OF_LIGHT_IN_METERS_PER_SECOND
        f = self.frequency_in_hertz
        lambda_ = c / f

        return lambda_

    @abstractmethod
    def calculate_gain(self, distance_in_meters: float) -> float:
        """
        Abstract method to calculate the channel gain for a given distance in meters.
        This method should be implemented in any subclass of Channel.

        :param distance_in_meters: The distance in meters for which to calculate the gain.
        :return: The calculated gain. The unit and interpretation of this value may vary depending on the specific subclass.
        """
        pass
