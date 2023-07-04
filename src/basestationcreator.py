from src.elementcreator import ElementCreator
from src.basestation import BaseStation


class BaseStationCreator(ElementCreator):

    def create_base_station(self, frequency, unique_id):
        return BaseStation(self._draw_position(self._upper_x_bound), self._draw_position(self._upper_y_bound), frequency, unique_id)

    def create_fixed_base_station(self, x, y, frequency=None, unique_id=None):
        return BaseStation(x, y, frequency, unique_id)
