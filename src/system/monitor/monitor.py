import os
from system.monitor.element_plotter import ElementPlotter
from system.monitor.logger import Logger
from system.system import System

class Monitor(ElementPlotter):
    """
    This class is responsible for monitoring system entities including base stations and user equipment.
    """
    def __init__(self, system: System, log_name: str, print_to_console: bool = False):
        self._scenario_config = system.scenario_config
        self._scenario_name = system.scenario_name
        self._base_stations = system.base_stations
        self._user_equipments = system.user_equipments
        self._base_station_to_user_equipment_links = system.base_station_to_user_equipment_links
        self._user_equipment_to_base_station_links = system.user_equipment_to_base_station_links
        self._capacity = system.capacity
        self._aggregate_throughput = system.throughput
        self._delays = system.delays
        self._log_name = log_name
        self._log_file_name = self.create_log_directory_and_get_file_path(log_name)
        self._system_logger = Logger(self._log_name, self._log_file_name)
        self._print = print if print_to_console else lambda s: None

        super().__init__(self._base_stations, self._user_equipments)

    @staticmethod
    def create_log_directory_and_get_file_path(log_name, log_directory='.'):
        """Function to create a log directory if it doesn't exist and return the log file path."""
        os.makedirs(log_directory, exist_ok=True)
        return os.path.join(log_directory, f'{log_name}.txt')

    def _log_separator(self):
        separator = "-" * 50
        self._system_logger.info(separator)
        self._print("")

    def log_general_settings(self):
        scenario_config = self._scenario_config
        log_string = "General Settings:"
        self._system_logger.info(log_string)
        self._print(log_string)

        general_settings_keys = [
            'bandwidth', 'frequency', 'slot_duration_in_seconds',
            'number_of_slots', 'resource_blocks_per_slot', 'tx_power',
            'ewma_time_constant', 'starvation_threshold', 'capacity_calculator'
        ]

        for key in general_settings_keys:
            value = scenario_config.get(key, "Not available")
            log_string = f"{key}: {value}"
            self._system_logger.info(log_string)
            self._print(log_string)
        self._log_separator()

    def log_scenario_name(self):
        self._log_separator()
        scenario_name = self._scenario_name
        log_string = f"Scenario Name: {scenario_name}"
        self._system_logger.info(log_string)
        self._print(log_string)
        self._log_separator()

    def log_base_stations(self):
        for i, base_station in enumerate(self._base_stations, start=1):
            if not base_station:
                self._system_logger.critical("Base station object is None")
                raise ValueError("Base station object is None")

            log_string = (f"Base Station Number: {i}, Location: ({base_station.x}, {base_station.y}), "
                          f"TX Power: {base_station.transmisson_power}, Frequency: {base_station.frequency}, "
                          f"Bandwidth: {base_station.bandwidth}")
            self._system_logger.info(log_string)
            self._print(log_string)
        self._log_separator()

    def log_user_equipments(self):
        for i, user_equipment in enumerate(self._user_equipments, start=1):
            log_string = f"UE Number: {i},{user_equipment.unique_id}, Location: ({user_equipment.x:.2f}, {user_equipment.y:.2f})"
            self._system_logger.info(log_string)
            self._print(log_string)
        self._log_separator()

    def log_connected_ues(self):
        for i, base_station in enumerate(self._base_stations, start=1):
            if not base_station:
                self._system_logger.critical("Base station object is None")
                raise ValueError("Base station object is None")

            connected_ues = base_station.connected_user_equipments
            if not connected_ues:
                log_string = f"No connected UEs found for Base Station: {i}"
                self._system_logger.info(log_string)
                continue

            log_string = f"Connected UEs for Base Station: {i}"
            self._system_logger.info(log_string)
            self._print(log_string)

            for j, user_equipment in enumerate(connected_ues, start=1):
                log_string = (f"UE Number:{j}, {user_equipment.unique_id}, Location:({user_equipment.x:.2f}, {user_equipment.y:.2f}),"
                              f"Distance:{user_equipment.distance_from_bs:.3f},"
                              f"Capacity:{user_equipment.current_capacity_in_bits_per_second}")
                self._system_logger.info(log_string)
                self._print(log_string)

            log_string = f"Total of {len(connected_ues)} UEs are connected"
            self._system_logger.info(log_string)
            self._print(log_string)
        self._log_separator()

    def log_all_downlink_links(self):
        for i, link in enumerate(self._base_station_to_user_equipment_links, start=1):
            if not link:
                self._system_logger.critical("Link object is None")
                raise ValueError("Link object is None")

            user_equipment = link.destination_node
            base_station = link.source_node
            log_string = (f"Link Number {i}: From BS ({base_station.x},{base_station.y}) to "
                          f"{user_equipment.unique_id}, UE ({user_equipment.x:.2f},{user_equipment.y:.2f}), Gain = {link.gain:e}")
            self._system_logger.info(log_string)
            self._print(log_string)
        self._log_separator()

    def log_transmission_detail(self):
        for slot, transmission_details in self._capacity.bits_transmitted_in_resource_block.items():
            for detail in transmission_details:
                self._system_logger.info(detail)
                self._print(detail)
            log_string = f"End of Slot {slot}"
            self._system_logger.info(log_string)
            self._print(log_string)
        self._log_separator()

    def log_user_equipments_delays(self):
        for i, user_equipment in enumerate(self._user_equipments, start=1):
            # Validation for transmission_delay
            if self._delays [user_equipment.unique_id] is None or not isinstance(user_equipment.transmission_delay, (int, float)):
                delay_info = "Unavailable"
                warning_message = f"Warning: Transmission delay data for UE Number: {i}, {user_equipment.unique_id} is unavailable or invalid."
                self._system_logger.warning(warning_message)
                self._print(warning_message)
            else:
                delay_info = f"{self._delays [user_equipment.unique_id]:.5f}"
                # delay_info = f"{user_equipment.transmission_delay:.6f}"

            log_string = f"UE Number: {i}, {user_equipment.unique_id}, Avg Delay: {delay_info}"
            self._system_logger.info(log_string)
            self._print(log_string)
        self._log_separator()

    def log_aggregate_throughput(self):
        log_string = f"Aggregate Throughput: {self._aggregate_throughput}"
        self._system_logger.info(log_string)
        self._print(log_string)
        self._log_separator()

    def log_scenario_data(self):

        self.log_scenario_name()
        self.log_general_settings()
        self.log_base_stations()
        self.log_user_equipments()
        self.log_connected_ues()
        self.log_all_downlink_links()
        self.log_transmission_detail()
        self.log_user_equipments_delays()
        self.log_aggregate_throughput()