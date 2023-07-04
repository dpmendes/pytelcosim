from src.basestation import BaseStation
from src.basestationcreator import BaseStationCreator


class BaseStationManager:
    def __init__(self, slot_duration_in_seconds, resource_blocks_per_slot):
        """Initializes BaseStationManager with provided slot duration and resource blocks."""
        self._base_stations = []
        self._slot_duration_in_seconds = slot_duration_in_seconds
        self._resource_blocks_per_slot = resource_blocks_per_slot
        self._base_station_creator = BaseStationCreator(0, 0)

    @staticmethod
    def add_outgoing_links(base_station, outgoing_links):
        for link in outgoing_links:
            base_station.outgoing_link = link

    @staticmethod
    def add_incoming_links(base_station, incoming_links):
        for link in incoming_links:
            base_station.incoming_link = link

    def add_base_station(self, base_station: BaseStation):
        if not self.find_base_station(base_station):
            self._base_stations.append(base_station)

    def find_base_station(self, base_station: BaseStation) -> bool:
        return base_station in self._base_stations

    def inform_base_stations_links(self, outgoing_links, incoming_links):
        for base_station in self._base_stations:
            self.inform_downlink_links(base_station, outgoing_links)
            self.inform_uplink_links(base_station, incoming_links)

    def inform_downlink_links(self, base_station: BaseStation, outgoing_links):
        for link in outgoing_links:
            base_station.outgoing_link = link

    def inform_uplink_links(self, base_station: BaseStation, incoming_links):
        for link in incoming_links:
            base_station.incoming_link = link

    def initialize_base_station_associated_user_equipment_scheduled_counters(self):
        for base_station in self._base_stations:
            base_station.initialize_user_equipment_times_scheduled_counters()

    def initialize_base_station_round_robin_schedulers(self):
        for base_station in self._base_stations:
            base_station.number_of_resource_blocks_per_slot = self._resource_blocks_per_slot
            base_station.initialize_round_robin_scheduler()
            base_station.inform_connected_user_equipment_to_scheduler()

    def create_base_station(self, upper_x_bound, upper_y_bound, default_frequency=None, unique_id=None):
        new_base_station = self._base_station_creator.create_fixed_base_station(
        upper_x_bound, upper_y_bound, default_frequency, unique_id)
        self._base_stations.append(new_base_station)
        return new_base_station


    def set_all_base_stations_transmit_power_in_watts(self, transmit_power: float):
        for base_station in self._base_stations:
            base_station.transmisson_power = transmit_power

    @property
    def base_stations(self):
        return self._base_stations

    def clear_base_stations(self):
        self._base_stations = []
