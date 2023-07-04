from src.elementplotter import ElementPlotter
from src.logger import Logger
from src.system import System

class Monitor(ElementPlotter):
    """
    This class is responsible for monitoring system entities including base stations and user equipment.
    """
    def __init__(self, system, log_name, log_file_name):
        super().__init__()
        assert isinstance(system, System)  # assuming System is the expected type
        assert isinstance(log_name, str)
        assert isinstance(log_file_name, str)

        self._base_stations = system.base_stations
        self._user_equipments = system.user_equipments
        self._log_name = log_name
        self._log_file_name = log_file_name
        self._system_logger = Logger(self._log_name, self._log_file_name)
        self._system_plot = ElementPlotter(self._base_stations, self._user_equipments)

        # To handle file operations
        self.results_file_handle = None

    def open_results_file(self, filename):
        self.results_file_handle = open(filename, 'w')
        return self.results_file_handle

    def close_results_file(self):
        if self.results_file_handle is not None:
            self.results_file_handle.close()
            self.results_file_handle = None

    def log_user_equipment(self):
        log_string = '\nUSER EQUIPMENT LIST\n'
        self.results_file_handle.write(log_string)
        for user_equipment in self._user_equipments:
            x, y = user_equipment.get_position()
            log_string = f'UE at ({x},{y})\n'
            self.results_file_handle.write(log_string)
        def log_associated_user_equipment(self):
            log_string = '\nBASE STATION AND ASSOCIATED USER EQUIPMENT LIST\n'
        self.results_file_handle.write(log_string)
        for base_station in self.base_stations_list:
            x, y = base_station.get_position()
            log_string = f'BS at ({x},{y})\n'
            self.results_file_handle.write(log_string)
            for user_equipment in base_station.get_associated_user_equipment():
                x, y = user_equipment.get_position()
                log_string = f'UE at ({x},{y})\n'
                self.results_file_handle.write(log_string)
            log_string = '\n'
            self.results_file_handle.write(log_string)

    def log_all_downlink_links(self):
        log_string = '\nLINKS\n'
        self.results_file_handle.write(log_string)
        for link in self.base_station_to_user_equipment_links_list:
            user_equipment = link.user_equipment
            base_station = link.base_station
            xu, yu = user_equipment.get_position()
            xb, yb = base_station.get_position()
            gain = link.gain
            log_string = f'From BS ({xb},{yb}) to UE ({xu},{yu})\nLink gain = {gain:e}\n'
            self.results_file_handle.write(log_string)

    def log_user_equipment_capacity(self, user_equipment):
        x, y = user_equipment.get_position()
        capacity = user_equipment.current_capacity_in_bits_per_second
        log_string = f"\nUE ({x},{y}) capacity = {capacity:.10e}"
        self.results_file_handle.write(log_string)

    def log_base_station_capacity(self, base_station):
        x, y = base_station.get_position()
        capacity = base_station.current_capacity_in_bits_per_second
        log_string = f"\nBS ({x},{y}) capacity = {capacity:.10e}"
        self.results_file_handle.write(log_string)

    def log_slots_bits_transmitted(self, current_slot, bits_transmitted_this_slot):
        log_string = f"\nEND OF SLOT {current_slot}\n"
        self.results_file_handle.write(log_string)
        log_string = f"Bits transmitted this slot = {bits_transmitted_this_slot:e}\n"
        self.results_file_handle.write(log_string)

    def log_base_stations(self):
        """
        Logs information about the base stations
        """
        if not self._base_stations:
            self._system_logger.log_message(
                "critical", "No base stations found in system")
            raise ValueError("No base stations found in system")

        for i, base_station in enumerate(self._base_stations):
            self._system_logger.log_message(
                "info", f"Base Station {i}: {base_station}")

    def log_connected_ues(self):
        for base_station in self._base_stations:
            if not base_station:
                self._system_logger.log_message(
                    "critical", "Base station object is None")
                raise ValueError("Base station object is None")

            connected_ues = base_station.connected_ues
            if not connected_ues:
                self._system_logger.log_message(
                    "error", f"No connected UEs found for Base Station with ID: {base_station.unique_id}")
                continue

            self._system_logger.log_message(
                "info", f"Connected UEs for Base Station with ID: {base_station.unique_id}")
            num_of_connected_ues = len(connected_ues)

            for user_equipment in connected_ues:
                ue_x = user_equipment.x
                ue_y = user_equipment.y
                ue_distance = user_equipment.distance_from_bs
                ue_link_capacity = user_equipment.link_capacity
                self._system_logger.log_message(
                    "info", f"UE ID: {user_equipment.unique_id}, Location: ({ue_x}, {ue_y}), Distance: {ue_distance}, Capacity: {ue_link_capacity}")

            self._system_logger.log_message(
                "info", f"Total of {num_of_connected_ues} Ue's are connected")

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