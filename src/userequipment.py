from src.element import Element
from src.basestation import BaseStation


class UserEquipment(Element):
    """Represents a user equipment in a network."""

    def __init__(self, x: float, y: float, frequency: float, unique_id: str):
        super().__init__(x, y, frequency, unique_id)

    @property
    def connected_bs(self):
        """The base station to which the user equipment is connected."""
        return self._connected_bs

    @connected_bs.setter
    def connected_bs(self, base_station: BaseStation):
        self._connected_bs = base_station

    def disconnect_from_base_stations(self):
        """Disconnects the user equipment from its connected base station."""
        self._connected_bs = None

    @property
    def distance_from_bs(self):
        """The distance from the user equipment to the connected base station."""
        return self._distance_from_bs

    @distance_from_bs.setter
    def distance_from_bs(self, distance: float):
        self._distance_from_bs = distance

    @property
    def link_capacity(self):
        """The link capacity of the user equipment."""
        return self._link_capacity

    @link_capacity.setter
    def link_capacity(self, capacity: float):
        self._link_capacity = capacity

    def is_dummy(self):
        """Checks if the user equipment is a dummy equipment, i.e., whether its x and y coordinates are both less than 0."""
        return self.x < 0 and self.y < 0

    def __str__(self) -> str:
        return f"UserEquipment: ID={self._unique_id}, Location=({self._x:.2f},{self._y:.2f}), Connected to Base Station={self._connected_bs}, Distance from Base Station={self._distance_from_bs:.2f}, Link Capacity={self._link_capacity:.2f}"
