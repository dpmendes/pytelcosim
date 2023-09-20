from transceiver.base_station.base_station_creator import BaseStationCreator


class BaseStationManager:

    def __init__(self, slot_duration_in_seconds, resource_blocks_per_slot):
        """Initializes BaseStationManager with provided slot duration and resource blocks."""
        self._base_stations = []
        self._slot_duration_in_seconds = slot_duration_in_seconds
        self._resource_blocks_per_slot = resource_blocks_per_slot
        self._base_station_creator = BaseStationCreator(0, 0)

    def add_base_station(self, base_station):
        if not self.find_base_station(base_station):
            self._base_stations.append(base_station)

    def create_base_station(self, mode='FIXED', x=None, y=None, frequency=None, bandwidth=None, transmisson_power=None, unique_id=None):
        if mode == 'FIXED':
            if x is None or y is None:
                raise ValueError("x and y coordinates must be provided for 'FIXED' mode.")
            new_base_station = self._base_station_creator.create_fixed_base_station(x, y, frequency, bandwidth, transmisson_power, unique_id)
        elif mode == 'RANDOM':
            if x is None or y is None:
                raise ValueError("Upper x and y bounds must be provided for 'RANDOM' mode.")
            new_base_station = self._base_station_creator.create_random_base_station(x, y, frequency, bandwidth, transmisson_power, unique_id)
        else:
            raise ValueError(f"Invalid mode '{mode}'. Must be 'FIXED' or 'RANDOM'.")

        if not self.find_base_station(new_base_station):
            self.add_base_station(new_base_station)

    def find_base_station(self, base_station):
        return base_station in self._base_stations

    def initialize_base_station_associated_user_equipment_scheduled_counters(self):
        for base_station in self._base_stations:
            base_station.initialize_user_equipment_times_scheduled_counters()

    def initialize_base_station_round_robin_schedulers(self):
        for base_station in self._base_stations:
            base_station.number_of_resource_blocks_per_slot = self._resource_blocks_per_slot
            base_station.initialize_round_robin_scheduler()
            base_station.inform_connected_user_equipment_to_scheduler()

    def initialize_base_station_proportional_fair_schedulers(self, ewma_time_constant, starvation_threshold, starvation_flag=False):
        for base_station in self._base_stations:
            base_station.number_of_resource_blocks_per_slot = self._resource_blocks_per_slot
            base_station.initialize_proportional_fair_scheduler(ewma_time_constant, starvation_threshold,starvation_flag)
            base_station.inform_connected_user_equipment_to_scheduler()

    def set_all_base_stations_transmit_power_in_watts(self, transmit_power: float):
        for base_station in self._base_stations:
            base_station.transmisson_power = transmit_power

    @property
    def base_stations(self):
        return self._base_stations

    def clear_base_stations(self):
        self._base_stations = []