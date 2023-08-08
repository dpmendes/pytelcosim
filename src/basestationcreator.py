from basestation import BaseStation
from elementcreator import ElementCreator


class BaseStationCreator(ElementCreator):
    """A class to create instances of Base Stations."""

    def create_base_station(self, frequency, unique_id):
        element = self.create_random_element(frequency)
        return BaseStation(element.x, element.y, element.frequency, unique_id)

    def create_fixed_base_station(self, x, y, frequency=None, unique_id=None):
        element = self.create_fixed_element(x, y, frequency)
        return BaseStation(element.x, element.y, element.frequency, unique_id)
