from transceiver.base.element import Element


class UserEquipment(Element):
    """Represents a user equipment in a network."""

    def __init__(self, x, y, frequency, bandwidth, transmisson_power, unique_id=None):
        super().__init__(x, y, frequency, bandwidth, transmisson_power, unique_id)
        self._connected_base_station = None
        self._distance_from_bs = 0
        self._transmission_slots = []
        self._avg_delay = 0

    @property
    def connected_base_station(self):
        """The base station to which the user equipment is connected."""
        return self._connected_base_station

    @connected_base_station.setter
    def connected_base_station(self, base_station):
        self._connected_base_station = base_station

    def disconnect_from_base_stations(self):
        """Disconnects the user equipment from its connected base station."""
        self._connected_base_station = None

    @property
    def distance_from_bs(self):
        """The distance from the user equipment to the connected base station."""
        return self._distance_from_bs

    @distance_from_bs.setter
    def distance_from_bs(self, distance: float):
        self._distance_from_bs = distance

    @property
    def transmission_delay(self):
        return self._avg_delay

    @transmission_delay.setter
    def transmission_delay(self, delay):
        self._avg_delay = delay

    def record_transmission_slot(self, slot_number):
        """Records the slot number in which the user equipment transmitted something.

        Args:
        slot_number (int): The number of the slot to record.
        """
        self._transmission_slots.append(slot_number)

    def get_transmission_slots(self):
        """Returns a list of slots in which the user equipment transmitted.

        Returns:
        list[int]: List of slots.
        """
        return self._transmission_slots

    def __str__(self) -> str:
        return f"UserEquipment: ID={self._unique_id}, Location=({self._x:.2f},{self._y:.2f})"
