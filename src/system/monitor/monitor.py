import os

from system.monitor.element_plotter import ElementPlotter
from system.monitor.logger import Logger
from system.system import System


class Monitor(ElementPlotter):
    """
    This class is responsible for monitoring system entities including base stations and user equipment.
    """

    def __init__(self, system: System, log_name: str, print_to_console: bool = False):
        self._base_stations = system.base_stations
        self._user_equipments = system.user_equipments
        self._base_station_to_user_equipment_links = system.base_station_to_user_equipment_links
        self._user_equipment_to_base_station_links = system.user_equipment_to_base_station_links
        self._capacity = system.capacity
        self._print_to_console_flag = print_to_console
        self._log_name = log_name
        self._log_file_name = self.create_log_directory(log_name)
        self._system_logger = Logger(self._log_name, self._log_file_name)

        super().__init__(self._base_stations, self._user_equipments)

    def create_log_directory(self, log_name, log_directory='.'):
        """Function to create a log directory if it doesn't exist and return the log file path."""
        log_directory = os.path.join(log_directory, 'execution logs')
        os.makedirs(log_directory, exist_ok=True)
        return os.path.join(log_directory, f'{log_name}.txt')

    def _print_to_console(self, string):
        if self._print_to_console_flag:
            print(string)

    def _log_separator(self):
        separator = "-" * 50
        self._system_logger.info(separator)
        if self._print_to_console_flag:
            print("")

    def log_base_stations(self):
        bs_counter = 1
        for base_station in self._base_stations:
            if not base_station:
                self._system_logger.critical("Base station object is None")
                raise ValueError("Base station object is None")

            bs_x = base_station.x
            bs_y = base_station.y
            bs_tx_power = base_station.transmisson_power
            bs_bandwidth = base_station.bandwidth
            bs_frequency = base_station.frequency
            log_string = f"Base Station Number: {bs_counter}, Location: ({bs_x}, {bs_y}), TX Power: {bs_tx_power}, Frequency: {bs_frequency}, Bandwidth: {bs_bandwidth}"
            self._system_logger.info(log_string)
            self._print_to_console(log_string)
            bs_counter += 1
        self._log_separator()

    def log_user_equipments(self):
        ue_counter = 1

        for user_equipment in self._user_equipments:
            ue_x = user_equipment.x
            ue_y = user_equipment.y
            log_string = f"UE Number: {ue_counter}, Location: ({ue_x}, {ue_y})"
            self._system_logger.info(log_string)
            self._print_to_console(log_string)
            ue_counter += 1
        self._log_separator()

    def log_connected_ues(self):
        bs_counter = 1
        for base_station in self._base_stations:
            if not base_station:
                self._system_logger.critical("Base station object is None")
                raise ValueError("Base station object is None")

            connected_ues = base_station.connected_user_equipment
            if not connected_ues:
                self._system_logger.error(f"No connected UEs found for Base Station: {bs_counter}")
                continue

            log_string = f"Connected UEs for Base Station: {bs_counter}"
            self._system_logger.info(log_string)
            self._print_to_console(log_string)
            num_of_connected_ues = len(connected_ues)

            ue_counter = 1
            for user_equipment in connected_ues:
                ue_x = user_equipment.x
                ue_y = user_equipment.y
                ue_distance = user_equipment.distance_from_bs
                ue_link_capacity = user_equipment.current_capacity_in_bits_per_second
                log_string = f"UE Number: {ue_counter}, Location: ({ue_x}, {ue_y}), Distance: {ue_distance:.3f}, Capacity: {ue_link_capacity}"
                self._system_logger.info(log_string)
                self._print_to_console(log_string)
                ue_counter += 1

            log_string = f"Total of {num_of_connected_ues} Ue's are connected"
            self._system_logger.info(log_string)
            self._print_to_console(log_string)
            bs_counter += 1
        self._log_separator()

    def log_all_downlink_links(self):
        link_counter = 1
        for link in self._base_station_to_user_equipment_links:
            if not link:
                self._system_logger.critical("Link object is None")
                raise ValueError("Link object is None")

            user_equipment = link.destination_node
            base_station = link.source_node
            xu, yu = user_equipment.x, user_equipment.y
            xb, yb = base_station.x, base_station.y
            gain = link.gain
            log_string = f"Link Number {link_counter}: From BS ({xb},{yb}) to UE ({xu},{yu}), Gain = {gain:e}"
            self._system_logger.info(log_string)
            self._print_to_console(log_string)
            link_counter += 1
        self._log_separator()

    def log_capacity(self):
        for slot, transmission_details in self._capacity.bits_transmitted_in_resource_block.items():
            log_string = "\n".join(transmission_details)
            self._system_logger.info(log_string)
            self._print_to_console(log_string)
            log_string = f"End of Slot {slot}"
            self._system_logger.info(log_string)
            self._print_to_console(log_string)
        self._log_separator()

    @property
    def base_stations(self):
        return self._base_stations

    @property
    def user_equipments(self):
        return self._user_equipments

    @property
    def log_name(self):
        return self._log_name

    @property
    def log_file_name(self):
        return self._log_file_name
