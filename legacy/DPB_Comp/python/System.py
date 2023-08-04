from BaseStation import BaseStation
from BaseStationToUserEquipmentLink import BaseStationToUserEquipmentLink
from Cluster import Cluster
from FreeSpaceChannel import FreeSpaceChannel
from UserEquipment import UserEquipment
from UserEquipmentToBaseStationLink import UserEquipmentToBaseStationLink

# System for Test Script 01;


class System:

    def __init__(self):
        self.base_stations_list = []
        self.base_station_to_user_equipment_links_list = []
        self.clusters_list = []
        self.user_equipment_list = []
        self.user_equipment_to_base_station_links_list = []
        self.transceivers_list = []
        self.channel = None
        self.slot_duration_in_seconds = 0.5e-3
        self.resource_blocks_per_slot = 3
        self.results_file_handle = None

    @staticmethod
    def add_links_from_base_station_list(base_station, links_from_base_station_list):
        for link in links_from_base_station_list:
            base_station.add_link_from_base_station(link)

    @staticmethod
    def add_links_to_base_station_list(base_station, links_to_base_station_list):
        for link in links_to_base_station_list:
            base_station.add_link_to_base_station(link)

    @staticmethod
    def find_greatest_gain_link(links_list):
        greatest_gain_link = max(links_list, key=lambda link: link.gain)
        return greatest_gain_link

    @staticmethod
    def calculate_intended_signal_to_user_equipment(user_equipment, links_to_user_equipment):
        intended_signal = 0
        for current_link in links_to_user_equipment:
            if current_link.base_station == user_equipment.serving_base_station:
                base_station = current_link.base_station
                intended_signal += base_station.get_transmit_power_in_watts() * current_link.gain
        return intended_signal

    @staticmethod
    def calculate_interfering_signal_at_user_equipment(user_equipment, links_to_user_equipment):
        interfering_signal = 0
        for current_link in links_to_user_equipment:
            if current_link.base_station != user_equipment.serving_base_station:
                base_station = current_link.base_station
                interfering_signal += base_station.get_transmit_power_in_watts() * \
                    current_link.gain
        return interfering_signal

    @staticmethod
    def get_scheduled_users_from_all_schedules(all_base_stations_schedule, resource_block):
        scheduled_users = []
        for base_station_schedule in all_base_stations_schedule:
            user_equipment = base_station_schedule.get_user_in_resource_block(
                resource_block)
            scheduled_users.append(user_equipment)
        return scheduled_users

# //============================================================================
    def log_user_equipment(self):
        log_string = '\nUSER EQUIPMENT LIST\n'
        self.results_file_handle.write(log_string)
        for user_equipment in self.user_equipment_list:
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

    def open_results_file(self, filename):
        results_file = open(filename, 'w')
        self.results_file_handle = results_file
        return results_file

    def close_results_file(self, results_file):
        results_file.close()
        self.results_file_handle = None

# //============================================================================

    def add_base_station(self, base_station):
        index_of_base_station_in_list = self.find_base_station(base_station)

        if index_of_base_station_in_list == -1:
            self.base_stations_list.append(base_station)

    def find_base_station(self, base_station):
        try:
            index_in_list = self.base_stations_list.index(base_station)
        except ValueError:
            index_in_list = -1
        return index_in_list

    def find_user_equipment(self, user_equipment):
        try:
            index_in_list = self.user_equipment_list.index(user_equipment)
        except ValueError:
            index_in_list = -1
        return index_in_list

    def add_user_equipment(self, user_equipment):
        index_of_user_equipment_in_list = self.find_user_equipment(
            user_equipment)

        if index_of_user_equipment_in_list == -1:
            self.user_equipment_list.append(user_equipment)

    def set_all_base_stations_transmit_power_in_watts(self, transmit_power):
        for base_station in self.base_stations_list:
            base_station.set_transmit_power_in_watts(transmit_power)

    def update_downlink_links_list(self):
        self.base_station_to_user_equipment_links_list = []
        for base_station in self.base_stations_list:
            for user_equipment in self.user_equipment_list:
                link_channel = self.channel
                link = BaseStationToUserEquipmentLink(link_channel)
                link.base_station = base_station
                link.user_equipment = user_equipment
                link.calculate_link_gain()
                self.base_station_to_user_equipment_links_list.append(link)

    def update_uplink_links_list(self):
        self.user_equipment_to_base_station_links_list = []
        for base_station in self.base_stations_list:
            for user_equipment in self.user_equipment_list:
                link_channel = self.channel
                link = UserEquipmentToBaseStationLink(link_channel)
                link.base_station = base_station
                link.user_equipment = user_equipment
                link.calculate_link_gain()
                self.user_equipment_to_base_station_links_list.append(link)

    def find_links_from_base_station(self, base_station):
        links_from_base_station = []
        for link in self.base_station_to_user_equipment_links_list:
            if link.base_station == base_station:
                links_from_base_station.append(link)
        return links_from_base_station

    def find_links_to_base_station(self, base_station):
        links_to_base_station = []
        for link in self.user_equipment_to_base_station_links_list:
            if link.active_in_the_current_slot and link.base_station == base_station:
                links_to_base_station.append(link)
        return links_to_base_station

    def find_links_to_user_equipment(self, user_equipment):
        return [link for link in self.base_station_to_user_equipment_links_list
                if link.active_in_the_current_slot and link.user_equipment == user_equipment]

    def associate_all_user_equipment(self):
        for user_equipment in self.user_equipment_list:
            links_to_user_equipment = self.find_links_to_user_equipment(
                user_equipment)
            greatest_gain_link = self.find_greatest_gain_link(
                links_to_user_equipment)
            user_equipment.associate_to_base_station(
                greatest_gain_link.base_station)
            base_station = greatest_gain_link.base_station
            base_station.associate_user_equipment(user_equipment)

    def initialize_base_station_associated_user_equipment_scheduled_counters(self):
        for base_station in self.base_stations_list:
            base_station.initialize_user_equipment_times_scheduled_counters()

    def initialize_base_station_round_robin_schedulers(self):
        for base_station in self.base_stations_list:
            base_station.set_number_of_resource_blocks_per_slot(
                self.resource_blocks_per_slot)
            base_station.initialize_round_robin_scheduler()
            base_station.inform_associated_user_equipment_to_scheduler()

    def schedule_resource_blocks_for_base_stations(self):
        all_base_stations_schedule = []
        for base_station in self.base_stations_list:
            slot_schedule = base_station.request_next_schedule_to_scheduler()
            all_base_stations_schedule.append(slot_schedule)
        return all_base_stations_schedule

    def inform_base_stations_links(self):
        for base_station in self.base_stations_list:
            self.inform_downlink_links(base_station)
            self.inform_uplink_links(base_station)

    def inform_downlink_links(self, base_station):
        links_from_base_station_list = self.find_links_from_base_station(
            base_station)
        self.add_links_from_base_station_list(
            base_station, links_from_base_station_list)

    def inform_uplink_links(self, base_station):
        links_to_base_station_list = self.find_links_to_base_station(
            base_station)
        self.add_links_to_base_station_list(
            base_station, links_to_base_station_list)

    def update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio(self):
        for user_equipment in self.user_equipment_list:
            links_to_user_equipment = self.find_links_to_user_equipment(
                user_equipment)
            intended_signal = self.calculate_intended_signal_to_user_equipment(
                user_equipment, links_to_user_equipment)
            interfering_signal = self.calculate_interfering_signal_at_user_equipment(
                user_equipment, links_to_user_equipment)
            user_equipment.update_signal_to_interference_plus_noise_ratio(
                intended_signal, interfering_signal)

    def update_all_user_equipment_reception_capacity(self):
        for user_equipment in self.user_equipment_list:
            user_equipment.calculate_reception_capacity()

    def update_all_user_equipment_slot_duration(self):
        for user_equipment in self.user_equipment_list:
            user_equipment.slot_duration_in_seconds = self.slot_duration_in_seconds

    def calculate_downlink_round_robin_aggregate_throughput_over_number_of_slots(self, number_of_slots):
        current_slot = 1
        total_bits_transmitted = 0
        results_file = self.open_results_file('round_robin_scheduling.dat')
        self.log_user_equipment()
        self.log_associated_user_equipment()
        self.log_all_downlink_links()

        while current_slot <= number_of_slots:
            bits_transmitted_this_slot = self.calculate_downlink_round_robin_scheduling_slot_transmitted_bits()
            total_bits_transmitted += bits_transmitted_this_slot
            self.log_slots_bits_transmitted(
                current_slot, bits_transmitted_this_slot)
            current_slot += 1

            if current_slot % 10 == 0:
                print(f'Current Slot = {current_slot}')

        slot_duration = self.slot_duration_in_seconds
        self.close_results_file(results_file)
        aggregate_throughput = total_bits_transmitted / \
            (number_of_slots * slot_duration)
        return aggregate_throughput

    def calculate_bits_transmitted_in_downlink_resource_block(self, scheduled_users):
        bits_transmitted_in_resource_block = 0

        for user_equipment in scheduled_users:
            user_equipment.receive_resource_block()
            bits_transmitted_per_user_equipment = (
                user_equipment.current_capacity_in_bits_per_second
                * self.slot_duration_in_seconds
            )

            self.log_user_equipment_capacity(user_equipment)

            bits_transmitted_in_resource_block += bits_transmitted_per_user_equipment

        return bits_transmitted_in_resource_block

    def calculate_downlink_round_robin_scheduling_slot_transmitted_bits(self):
        bits_transmitted_this_slot = 0
        all_base_stations_schedule = self.schedule_resource_blocks_for_base_stations()

        for resource_block in range(self.resource_blocks_per_slot):
            scheduled_users = self.get_scheduled_users_from_all_schedules(
                all_base_stations_schedule, resource_block)
            self.update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
            self.update_all_user_equipment_reception_capacity()
            bits_transmitted_in_resource_block = self.calculate_bits_transmitted_in_downlink_resource_block(
                scheduled_users)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        return bits_transmitted_this_slot

    def configure_basics(self):
        self.channel = FreeSpaceChannel(2600e6)
        self.update_all_user_equipment_slot_duration()
        self.update_downlink_links_list()
        self.update_uplink_links_list()
        self.inform_base_stations_links()
        self.associate_all_user_equipment()
        self.initialize_base_station_associated_user_equipment_scheduled_counters()
        self.initialize_base_station_round_robin_schedulers()

    def configure_downlink_test(self):
        self.set_all_base_stations_transmit_power_in_watts(40)
        self.configure_basics()

    def load_test_scenario_1(self):
        self.add_base_station(BaseStation(10, 20))
        self.add_base_station(BaseStation(50, 20))
        self.add_user_equipment(UserEquipment(0, 0))
        self.add_user_equipment(UserEquipment(20, 0))
        self.add_user_equipment(UserEquipment(40, 0))
        self.add_user_equipment(UserEquipment(60, 0))
        self.configure_downlink_test()
