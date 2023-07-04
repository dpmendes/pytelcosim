from BaseStation import BaseStation
from BaseStationToUserEquipmentLink import BaseStationToUserEquipmentLink
from Cluster import Cluster
from FreeSpaceChannel import FreeSpaceChannel
from UserEquipment import UserEquipment
from UserEquipmentToBaseStationLink import UserEquipmentToBaseStationLink


class System:

    def __init__(self):
        self.base_stations = []
        self.base_station_to_user_equipment_links = []
        self.clusters = []
        self.user_equipment = []
        self.user_equipment_to_base_station_links = []
        self.transceivers = []
        self.channel = None
        self.slot_duration_in_seconds = 0.5e-3
        self.resource_blocks_per_slot = 3
        self.results_file_handle = None

    @staticmethod
    def get_scheduled_users_from_all_schedules(all_base_stations_schedule, resource_block):
        scheduled_users = []
        for base_station_schedule in all_base_stations_schedule:
            user_equipment = base_station_schedule.get_user_in_resource_block(
                resource_block)
            scheduled_users.append(user_equipment)
        return scheduled_users

    @staticmethod
    def find_greatest_gain_link(links):
        greatest_gain_link = None
        previous_greatest_gain = 0
        for current_link in links:
            current_link_gain = current_link.gain
            if current_link_gain > previous_greatest_gain:
                previous_greatest_gain = current_link_gain
                greatest_gain_link = current_link
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
    def calculate_interfering_signal_at_base_station(base_station, links_to_base_station):
        interfering_signal = 0
        for current_link in links_to_base_station:
            user_equipment = current_link.user_equipment
            if user_equipment.serving_base_station != base_station:
                interfering_signal += user_equipment.get_transmit_power_in_watts() * \
                    current_link.gain
        return interfering_signal

    @staticmethod
    def activate_scheduled_users_links(scheduled_users_links):
        for link in scheduled_users_links:
            link.activate_link()

    @staticmethod
    def add_links_from_base_station_list(base_station, links_from_base_station_list):
        for link in links_from_base_station_list:
            base_station.add_link_from_base_station(link)

    @staticmethod
    def add_links_to_base_station_list(base_station, links_to_base_station_list):
        for link in links_to_base_station_list:
            base_station.add_link_to_base_station(link)

    @staticmethod
    def deactivate_links(links):
        for link in links:
            link.deactivate_link()

    @staticmethod
    def activate_links(links):
        for link in links:
            link.activate_link()

    def calculate_dpb_aggregate_throughput_over_number_of_slots(self, number_of_slots, is_uplink):
        current_slot = 1
        total_bits_transmitted = 0
        if is_uplink:
            results_file = self.open_results_file(
                'dynamic_point_blanking_uplink.dat')
            self.log_all_uplink_links()
        else:
            results_file = self.open_results_file('dynamic_point_blanking.dat')
            self.log_all_downlink_links()

        self.log_user_equipment()
        self.log_associated_user_equipment()

        while current_slot <= number_of_slots:
            if is_uplink:
                bits_transmitted_this_slot = self.calculate_uplink_dpb_slot_transmitted_bits()
            else:
                bits_transmitted_this_slot = self.calculate_downlink_dpb_slot_transmitted_bits()

            total_bits_transmitted += bits_transmitted_this_slot
            self.log_slots_bits_transmitted(
                current_slot, bits_transmitted_this_slot)

            current_slot += 1
            if not current_slot % 10:
                print(f'Current Slot = {current_slot}')

        slot_duration = self.slot_duration_in_seconds
        aggregate_throughput = total_bits_transmitted / \
            (number_of_slots * slot_duration)
        self.close_results_file(results_file)

    def open_results_file(self, filename):
        results_file = open(filename, 'w')
        self.results_file_handle = results_file
        return results_file

    def log_user_equipment(self):
        log_string = '\nUSER EQUIPMENT LIST\n'
        self.results_file_handle.write(log_string)
        for user_equipment in self.user_equipment:
            x, y = user_equipment.get_position()
            log_string = f'UE at ({x},{y})\n'
            self.results_file_handle.write(log_string)

    def log_associated_user_equipment(self):
        log_string = '\nBASE STATION AND ASSOCIATED USER EQUIPMENT LIST\n'
        self.results_file_handle.write(log_string)
        for base_station in self.base_stations:
            x, y = base_station.get_position()
            log_string = f'BS at ({x},{y})\n'
            self.results_file_handle.write(log_string)
            for user_equipment in base_station.associateduser_equipment:
                x, y = user_equipment.get_position()
                log_string = f'UE at ({x},{y})\n'
                self.results_file_handle.write(log_string)
            log_string = '\n'
            self.results_file_handle.write(log_string)

    def log_all_downlink_links(self):
        log_string = '\nLINKS\n'
        self.results_file_handle.write(log_string)
        for link in self.base_station_to_user_equipment_links:
            user_equipment = link.userEquipment
            base_station = link.baseStation
            xu, yu = user_equipment.get_position()
            xb, yb = base_station.get_position()
            gain = link.gain
            log_string = f'From BS ({xb},{yb}) to UE ({xu},{yu})\nLink gain = {gain:e}\n'
            self.results_file_handle.write(log_string)

    def log_all_uplink_links(self):
        log_string = "\nLINKS\n"
        self.results_file_handle.write(log_string)
        for link in self.user_equipment_to_base_station_links:
            user_equipment = link.user_equipment
            base_station = link.base_station
            xu, yu = user_equipment.get_position()
            xb, yb = base_station.get_position()
            gain = link.gain
            log_string = f"From UE ({xu},{yu}) to BS ({xb},{yb})\nLink gain = {gain:e}\n"
            self.results_file_handle.write(log_string)

    def log_slots_bits_transmitted(self, current_slot, bits_transmitted_this_slot):
        log_string = f"\nEND OF SLOT {current_slot}\n"
        self.results_file_handle.write(log_string)
        log_string = f"Bits transmitted this slot = {bits_transmitted_this_slot:e}\n"
        self.results_file_handle.write(log_string)

    def close_results_file(self, results_file):
        results_file.close()
        self.results_file_handle = None

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

    def calculate_uplink_round_robin_aggregate_throughput_over_number_of_slots(self, number_of_slots):
        current_slot = 1
        total_bits_transmitted = 0
        results_file = self.open_results_file('round_robin_uplink.dat')
        self.log_user_equipment()
        self.log_associated_user_equipment()
        self.log_all_uplink_links()

        while current_slot <= number_of_slots:
            bits_transmitted_this_slot = self.calculate_uplink_round_robin_scheduling_slot_transmitted_bits()
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

    def calculate_coordinated_beamforming_slot_transmitted_bits(self):
        bits_transmitted_this_slot = 0
        all_base_stations_schedule = self.schedule_resource_blocks_for_base_stations()

        for resource_block in range(1, self.resource_blocks_per_slot + 1):
            scheduled_users = self.get_scheduled_users_from_all_schedules(
                all_base_stations_schedule, resource_block)
            self.activate_all_downlink_links()
            scheduled_users_links = self.find_scheduled_users_links(
                scheduled_users)
            self.deactivate_all_downlink_links()
            self.activate_scheduled_users_links(scheduled_users_links)
            self.update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
            self.update_all_user_equipment_reception_capacity()
            bits_transmitted_in_resource_block = self.calculate_bits_transmitted_in_downlink_resource_block(
                scheduled_users)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        return bits_transmitted_this_slot

    def calculate_downlink_round_robin_scheduling_slot_transmitted_bits(self):
        bits_transmitted_this_slot = 0
        all_base_stations_schedule = self.schedule_resource_blocks_for_base_stations()

        for resource_block in range(1, self.resource_blocks_per_slot + 1):
            scheduled_users = self.get_scheduled_users_from_all_schedules(
                all_base_stations_schedule, resource_block)
            self.update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
            self.update_all_user_equipment_reception_capacity()
            bits_transmitted_in_resource_block = self.calculate_bits_transmitted_in_downlink_resource_block(
                scheduled_users)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        return bits_transmitted_this_slot

    def calculate_uplink_round_robin_scheduling_slot_transmitted_bits(self):
        bits_transmitted_this_slot = 0
        all_base_stations_schedule = self.schedule_resource_blocks_for_base_stations()

        for resource_block in range(1, self.resource_blocks_per_slot + 1):
            scheduled_users = self.get_scheduled_users_from_all_schedules(
                all_base_stations_schedule, resource_block)
            self.activate_links_with_scheduled_users(scheduled_users)
            self.update_all_base_stations_rx_signal_to_interference_plus_noise_ratio()
            self.update_all_base_stations_reception_capacity()
            bits_transmitted_in_resource_block = self.calculate_bits_transmitted_in_uplink_resource_block(
                scheduled_users)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        return bits_transmitted_this_slot

    def activate_links_with_scheduled_users(self, scheduled_users):
        self.deactivate_all_uplink_links()
        self.activate_scheduled_user_equipment_uplink_links(scheduled_users)

    def calculate_downlink_dpb_slot_transmitted_bits(self):
        bits_transmitted_this_slot = 0
        clusters_schedule = self.request_schedule_to_clusters()

        for resource_block in range(1, self.resource_blocks_per_slot + 1):
            scheduled_users = self.get_scheduled_users_from_all_schedules(
                clusters_schedule, resource_block)
            self.log_scheduled_users_in_resource_block(
                scheduled_users, resource_block)
            active_base_stations = self.determine_active_base_stations(
                scheduled_users)
            self.deactivate_all_downlink_links()
            self.activate_active_base_stations_downlink_links(
                active_base_stations)
            self.update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
            self.update_all_user_equipment_reception_capacity()
            bits_transmitted_in_resource_block = self.calculate_bits_transmitted_in_downlink_resource_block(
                scheduled_users)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        return bits_transmitted_this_slot

    def calculate_uplink_dpb_slot_transmitted_bits(self):
        bits_transmitted_this_slot = 0
        clusters_schedule = self.request_schedule_to_clusters()

        for resource_block in range(1, self.resource_blocks_per_slot + 1):
            scheduled_users = self.get_scheduled_users_from_all_schedules(
                clusters_schedule, resource_block)
            self.log_scheduled_users_in_resource_block(
                scheduled_users, resource_block)
            self.activate_links_with_scheduled_users(scheduled_users)
            self.update_all_base_stations_rx_signal_to_interference_plus_noise_ratio()
            self.update_all_base_stations_reception_capacity()
            bits_transmitted_in_resource_block = self.calculate_bits_transmitted_in_uplink_resource_block(
                scheduled_users)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        return bits_transmitted_this_slot

    def log_scheduled_users_in_resource_block(self, scheduled_users, resource_block):
        log_string = f'\nRESOURCE BLOCK {resource_block}\n'
        self.results_file_handle.write(log_string)
        for user_equipment in scheduled_users:
            xu, yu = user_equipment.get_position()
            log_string = f'UE ({xu},{yu})\n'
            self.results_file_handle.write(log_string)

    def determine_active_base_stations(self, scheduled_users):
        active_base_stations = []
        for base_station in self.base_stations:
            associated_user_equipment = base_station.get_associated_user_equipment()
            is_base_station_active = any(
                ue in scheduled_users for ue in associated_user_equipment)
            if is_base_station_active:
                active_base_stations.append(base_station)
        return active_base_stations

    def activate_active_base_stations_downlink_links(self, active_base_stations):
        for link in self.base_station_to_user_equipment_links:
            link_base_station = link.base_station
            if link_base_station in active_base_stations:
                link.activate_link()

    def activate_scheduled_user_equipment_uplink_links(self, scheduled_users):
        for link in self.user_equipment_to_base_station_links:
            link_user_equipment = link.user_equipment
            if link_user_equipment in scheduled_users:
                link.activate_link()

    def request_schedule_to_clusters(self):
        clusters_schedule = []
        for cluster in self.clusters:
            clusters_schedule.extend(
                cluster.request_schedule_to_central_unit())
        return clusters_schedule

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

    def calculate_bits_transmitted_in_uplink_resource_block(self, scheduled_users):
        bits_transmitted_in_resource_block = 0

        for user_equipment in scheduled_users:
            if user_equipment.is_dummy:
                continue

            receiving_base_station = user_equipment.get_serving_base_station()
            receiving_base_station.receive_resource_block()
            capacity = receiving_base_station.get_current_capacity_in_bits_per_second()
            user_equipment.transmit_resource_block(capacity)
            bits_transmitted_per_base_station = (
                receiving_base_station.current_capacity_in_bits_per_second
                * self.slot_duration_in_seconds
            )

            self.log_base_station_capacity(receiving_base_station)

            bits_transmitted_in_resource_block += bits_transmitted_per_base_station

        return bits_transmitted_in_resource_block

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

    def deactivate_all_downlink_links(self):
        links = self.base_station_to_user_equipment_links
        self.deactivate_links(links)

    def deactivate_all_uplink_links(self):
        links = self.user_equipment_to_base_station_links
        self.deactivate_links(links)

    def activate_all_uplink_links(self):
        links = self.user_equipment_to_base_station_links
        self.activate_links(links)

    def schedule_resource_blocks_for_base_stations(self):
        all_base_stations_schedule = []
        for base_station in self.base_stations:
            slot_schedule = base_station.request_next_schedule_to_scheduler()
            all_base_stations_schedule.extend(slot_schedule)
        return all_base_stations_schedule

    def find_scheduled_users_links(self, scheduled_users):
        links_to_user_equipment = []
        for user_equipment in scheduled_users:
            new_links_to_user_equipment = self.find_links_to_user_equipment(
                user_equipment)
            links_to_user_equipment.extend(new_links_to_user_equipment)
        return links_to_user_equipment

    def calculate_aggregate_capacity(self):
        self.update_all_user_equipment_reception_capacity()
        aggregate_capacity = 0
        for user_equipment in self.user_equipment:
            aggregate_capacity += user_equipment.current_capacity_in_bits_per_second
        return aggregate_capacity

    def update_all_user_equipment_reception_capacity(self):
        for user_equipment in self.user_equipment:
            user_equipment.calculate_reception_capacity()

    def update_all_base_stations_reception_capacity(self):
        for base_station in self.base_stations:
            base_station.calculate_reception_capacity()

    def update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio(self):
        for user_equipment in self.user_equipment:
            links_to_user_equipment = self.find_links_to_user_equipment(
                user_equipment)
            intended_signal = self.calculate_intended_signal_to_user_equipment(
                user_equipment, links_to_user_equipment)
            interfering_signal = self.calculate_interfering_signal_at_user_equipment(
                user_equipment, links_to_user_equipment)
            user_equipment.update_signal_to_interference_plus_noise_ratio(
                intended_signal, interfering_signal)

    def update_all_base_stations_rx_signal_to_interference_plus_noise_ratio(self):
        for base_station in self.base_stations:
            links_to_base_station = self.find_links_to_base_station(
                base_station)
            intended_signal = self.calculate_intended_signal_to_base_station(
                base_station, links_to_base_station)
            interfering_signal = self.calculate_interfering_signal_at_base_station(
                base_station, links_to_base_station)
            base_station.update_signal_to_interference_plus_noise_ratio(
                intended_signal, interfering_signal)

    def add_base_station(self, base_station):
        index_of_base_station_in = self.find_base_station(base_station)

        if index_of_base_station_in == -1:
            self.base_stations.append(base_station)

    def remove_base_station(self, base_station):
        index_of_base_station_in = self.find_base_station(base_station)

        if index_of_base_station_in != -1:
            self.base_stations.pop(index_of_base_station_in)

    def find_base_station(self, base_station):
        try:
            index_in = self.base_stations.index(base_station)
        except ValueError:
            index_in = -1
        return index_in

    def add_user_equipment(self, user_equipment):
        index_of_user_equipment_in = self.find_user_equipment(user_equipment)

        if index_of_user_equipment_in == -1:
            self.user_equipment.append(user_equipment)

    def remove_user_equipment(self, user_equipment):
        index_of_user_equipment_in = self.find_user_equipment(user_equipment)

        if index_of_user_equipment_in != -1:
            self.user_equipment.pop(index_of_user_equipment_in)

    def find_user_equipment(self, user_equipment):
        try:
            index_in = self.user_equipment.index(user_equipment)
        except ValueError:
            index_in = -1
        return index_in

    def update_downlink_links(self):
        self.base_station_to_user_equipment_links = []
        for base_station in self.base_stations:
            for user_equipment in self.user_equipment:
                link_channel = self.channel
                link = BaseStationToUserEquipmentLink(link_channel)
                link.base_station = base_station
                link.user_equipment = user_equipment
                link.calculate_link_gain()
                self.base_station_to_user_equipment_links.append(link)

    def update_uplink_links(self):
        self.user_equipment_to_base_station_links = []

        for base_station in self.base_stations:
            for user_equipment in self.user_equipment:
                link_channel = self.channel
                link = UserEquipmentToBaseStationLink(link_channel)
                link.base_station = base_station
                link.user_equipment = user_equipment
                link.calculate_link_gain()
                self.user_equipment_to_base_station_links.append(link)

    def associate_all_user_equipment(self):
        for user_equipment in self.user_equipment:
            links_to_user_equipment = self.find_links_to_user_equipment(
                user_equipment)
            greatest_gain_link = self.find_greatest_gain_link(
                links_to_user_equipment)
            user_equipment.associate_to_base_station(
                greatest_gain_link.base_station)
            base_station = greatest_gain_link.base_station
            base_station.associate_user_equipment(user_equipment)

    def initialize_base_station_associated_user_equipment_scheduled_counters(self):
        for base_station in self.base_stations:
            base_station.initialize_user_equipment_times_scheduled_counters()

    def find_links_to_user_equipment(self, user_equipment):
        links_to_user_equipment = []
        for link in self.base_station_to_user_equipment_links:
            if link.active_in_the_current_slot and link.user_equipment == user_equipment:
                links_to_user_equipment.append(link)
        return links_to_user_equipment

    def find_links_to_base_station(self, base_station):
        links_to_base_station = []
        for link in self.user_equipment_to_base_station_links:
            if link.active_in_the_current_slot and link.base_station == base_station:
                links_to_base_station.append(link)
        return links_to_base_station

    def load_test_scenario_1(self):
        self.add_base_station(BaseStation(10, 20))
        self.add_base_station(BaseStation(50, 20))
        self.add_user_equipment(UserEquipment(0, 0))
        self.add_user_equipment(UserEquipment(20, 0))
        self.add_user_equipment(UserEquipment(40, 0))
        self.add_user_equipment(UserEquipment(60, 0))

        self.configure_downlink_test()

    def load_test_scenario_2(self):
        self.add_base_station(BaseStation(20, 20))
        self.add_base_station(BaseStation(10, 0))
        self.add_base_station(BaseStation(30, 0))
        self.add_user_equipment(UserEquipment(25, 20))
        self.add_user_equipment(UserEquipment(15, 0))
        self.add_user_equipment(UserEquipment(35, 0))
        self.add_user_equipment(UserEquipment(0, 10))

        self.configure_downlink_test()

    def load_test_scenario_3(self):
        self.add_base_station(BaseStation(10, 10))
        self.add_base_station(BaseStation(30, 35))
        self.add_base_station(BaseStation(50, 10))
        self.add_user_equipment(UserEquipment(0, 0))
        self.add_user_equipment(UserEquipment(20, 0))
        self.add_user_equipment(UserEquipment(20, 20))
        self.add_user_equipment(UserEquipment(0, 20))
        self.add_user_equipment(UserEquipment(20, 25))
        self.add_user_equipment(UserEquipment(40, 25))
        self.add_user_equipment(UserEquipment(20, 45))
        self.add_user_equipment(UserEquipment(40, 45))
        self.add_user_equipment(UserEquipment(40, 20))
        self.add_user_equipment(UserEquipment(40, 0))
        self.add_user_equipment(UserEquipment(60, 0))
        self.add_user_equipment(UserEquipment(60, 20))

        self.configure_downlink_test()

    def load_test_scenario_3_uplink(self):
        self.add_base_station(BaseStation(10, 10))
        self.add_base_station(BaseStation(30, 35))
        self.add_base_station(BaseStation(50, 10))
        self.add_user_equipment(UserEquipment(0, 0))
        self.add_user_equipment(UserEquipment(20, 0))
        self.add_user_equipment(UserEquipment(20, 20))
        self.add_user_equipment(UserEquipment(0, 20))
        self.add_user_equipment(UserEquipment(20, 25))
        self.add_user_equipment(UserEquipment(40, 25))
        self.add_user_equipment(UserEquipment(20, 45))
        self.add_user_equipment(UserEquipment(40, 45))
        self.add_user_equipment(UserEquipment(40, 20))
        self.add_user_equipment(UserEquipment(40, 0))
        self.add_user_equipment(UserEquipment(60, 0))
        self.add_user_equipment(UserEquipment(60, 20))

        self.configure_uplink_test()

    def load_test_scenario_4_uplink(self):
        self.add_base_station(BaseStation(2.5, 2.5))
        self.add_base_station(BaseStation(7.5, 2.5))
        self.add_base_station(BaseStation(2.5, 7.5))
        self.add_base_station(BaseStation(7.5, 7.5))

        for i in range(11):
            for j in range(11):
                self.add_user_equipment(UserEquipment(j, i))

        self.configure_uplink_test()

    def load_test_scenario_5_downlink(self):
        self.add_base_station(BaseStation(5, 5))
        self.add_base_station(BaseStation(25, 5))
        self.add_user_equipment(UserEquipment(0, 0))
        self.add_user_equipment(UserEquipment(10, 0))
        self.add_user_equipment(UserEquipment(0, 10))
        self.add_user_equipment(UserEquipment(10, 10))
        self.add_user_equipment(UserEquipment(20, 0))
        self.add_user_equipment(UserEquipment(30, 0))
        self.add_user_equipment(UserEquipment(20, 10))
        self.add_user_equipment(UserEquipment(30, 10))
        self.configure_downlink_test()

    def configure_downlink_test(self):
        self.set_all_base_stations_transmit_power_in_watts(50)
        self.configure_basics()

    def load_suburb_uplink_scenario(self):
        base_stations_separation_in_meters = 40
        base_stations_origin = [20, 0]
        self.add_ten_base_stations_in_horizontal_line_meters_apart_from_point(
            base_stations_separation_in_meters, base_stations_origin)
        base_stations_origin = [20, 30]
        self.add_ten_base_stations_in_horizontal_line_meters_apart_from_point

    def add_ten_base_stations_in_horizontal_line_meters_apart_from_point(self, separation_in_meters, origin_point):
        current_base_station_position = origin_point
        for _ in range(10):
            x, y = current_base_station_position
            base_station = BaseStation(x, y)
            self.add_base_station(base_station)
            current_base_station_position[0] += separation_in_meters

    def add_twenty_user_equipment_in_horizontal_line_meters_apart_from_point(self, separation_in_meters, origin_point):
        current_user_equipment_position = origin_point
        for _ in range(20):
            x, y = current_user_equipment_position
            user_equipment = UserEquipment(x, y)
            self.add_user_equipment(user_equipment)
            current_user_equipment_position[0] += separation_in_meters

    def load_downtown_residential_uplink_scenario(self):
        base_stations_separation_in_meters = 20
        base_stations_origin = [10, 0]
        self.add_ten_base_stations_in_horizontal_line_meters_apart_from_point(
            base_stations_separation_in_meters, base_stations_origin)
        base_stations_origin = [10, 17]
        self.add_ten_base_stations_in_horizontal_line_meters_apart_from_point(
            base_stations_separation_in_meters, base_stations_origin)

        user_equipment_separation_in_meters = 10
        user_equipment_origin = [5, 3]
        self.add_twenty_user_equipment_in_horizontal_line_meters_apart_from_point(
            user_equipment_separation_in_meters, user_equipment_origin)
        user_equipment_origin = [5, 14]
        self.add_twenty_user_equipment_in_horizontal_line_meters_apart_from_point(
            user_equipment_separation_in_meters, user_equipment_origin)
        self.configure_uplink_test()

    def load_building_uplink_scenario(self):
        base_stations_separation_in_meters = 3
        base_stations_origin = [4, 0]
        self.add_ten_base_stations_in_vertical_line_meters_apart_from_point(
            base_stations_separation_in_meters, base_stations_origin)
        base_stations_origin = [12, 0]
        self.add_ten_base_stations_in_vertical_line_meters_apart_from_point(
            base_stations_separation_in_meters, base_stations_origin)

        user_equipment_separation_in_meters = 3
        user_equipment_origin = [2, 0]
        self.add_ten_user_equipment_in_vertical_line_meters_apart_from_point(
            user_equipment_separation_in_meters, user_equipment_origin)
        user_equipment_origin = [6, 0]
        self.add_ten_user_equipment_in_vertical_line_meters_apart_from_point(
            user_equipment_separation_in_meters, user_equipment_origin)
        user_equipment_origin = [10, 0]
        self.add_ten_user_equipment_in_vertical_line_meters_apart_from_point(
            user_equipment_separation_in_meters, user_equipment_origin)
        user_equipment_origin = [14, 0]
        self.add_ten_user_equipment_in_vertical_line_meters_apart_from_point(
            user_equipment_separation_in_meters, user_equipment_origin)
        self.configure_uplink_test()

    def add_ten_base_stations_in_vertical_line_meters_apart_from_point(self, separation_in_meters, origin_point):
        current_base_station_position = origin_point
        for _ in range(10):
            x, y = current_base_station_position
            base_station = BaseStation(x, y)
            self.add_base_station(base_station)
            current_base_station_position[1] += separation_in_meters

    def add_ten_user_equipment_in_vertical_line_meters_apart_from_point(self, separation_in_meters, origin_point):
        current_user_equipment_position = origin_point
        for _ in range(10):
            x, y = current_user_equipment_position
            user_equipment = UserEquipment(x, y)
            self.add_user_equipment(user_equipment)
            current_user_equipment_position[1] += separation_in_meters

    def configure_basics(self):
        self.channel = FreeSpaceChannel(2600e6)
        self.update_all_user_equipment_slot_duration()
        self.update_downlink_links()
        self.update_uplink_links()
        self.inform_base_stations_links()
        self.associate_all_user_equipment()
        self.initialize_base_station_associated_user_equipment_scheduled_counters()
        self.initialize_base_station_round_robin_schedulers()
        self.form_clusters()

    def set_all_base_stations_transmit_power_in_watts(self, transmit_power):
        for base_station in self.base_stations:
            base_station.set_transmit_power_in_watts(transmit_power)

    def configure_uplink_test(self):
        self.set_all_user_equipment_transmit_power_in_watts(0.5)
        self.set_all_base_stations_transmit_power_in_watts(50)
        self.configure_basics()

    def set_all_user_equipment_transmit_power_in_watts(self, transmit_power):
        for user_equipment in self.user_equipment:
            user_equipment.set_transmit_power_in_watts(transmit_power)

    def inform_base_stations_links(self):
        for base_station in self.base_stations:
            self.inform_downlink_links(base_station)
            self.inform_uplink_links(base_station)

    def inform_downlink_links(self, base_station):
        links_from_base_station = self.find_links_from_base_station(
            base_station)
        self.add_links_from_base_station(base_station, links_from_base_station)

    def inform_uplink_links(self, base_station):
        links_to_base_station = self.find_links_to_base_station(base_station)
        self.add_links_to_base_station(base_station, links_to_base_station)

    def find_links_from_base_station(self, base_station):
        links_from_base_station = []
        for link in self.base_station_to_user_equipment_links:
            if link.base_station == base_station:
                links_from_base_station.append(link)
        return links_from_base_station

    def update_all_user_equipment_slot_duration(self):
        for user_equipment in self.user_equipment:
            user_equipment.slot_duration_in_seconds = self.slot_duration_in_seconds

    def initialize_base_station_round_robin_schedulers(self):
        for base_station in self.base_stations:
            base_station.set_number_of_resource_blocks_per_slot(
                self.resource_blocks_per_slot)
            base_station.initialize_round_robin_scheduler()
            base_station.inform_associated_user_equipment_to_scheduler()

    def form_clusters(self):
        cluster = Cluster()
        for base_station in self.base_stations:
            cluster.add_base_station_to_cluster(base_station)

        cluster.set_resource_blocks_per_slot(self.resource_blocks_per_slot)
        cluster.create_central_unit_coordinating_added_base_stations()
        links = self.base_station_to_user_equipment_links
        # cluster.pass_all_links_to_central_unit(links)

        self.clusters.append(cluster)
