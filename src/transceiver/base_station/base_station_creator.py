from transceiver.base.element_creator import ElementCreator
from transceiver.base_station.base_station import BaseStation

class BaseStationCreator(ElementCreator):
    """A class to create instances of Base Stations."""

    def create_random_base_station(self, upper_x_bound, upper_y_bound, frequency, bandwidth, transmisson_power, unique_id=None):
        element = super().create_random_element(upper_x_bound, upper_y_bound, frequency, bandwidth, transmisson_power, unique_id)
        return BaseStation(element.x, element.y, element.frequency, element.bandwidth, element.transmisson_power, element.unique_id)

    def create_fixed_base_station(self, x, y, frequency, bandwidth, transmisson_power, unique_id=None):
        element = super().create_fixed_element(x, y, frequency, bandwidth, transmisson_power, unique_id)
        return BaseStation(element.x, element.y, element.frequency, element.bandwidth, element.transmisson_power, element.unique_id)
