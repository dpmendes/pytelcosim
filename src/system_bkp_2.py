from src.basestation import BaseStation
from src.basestationcreator import BaseStationCreator
from src.basestationtouserequipmentlink import BaseStationToUserEquipmentLink
from src.freespacechannel import FreeSpaceChannel
from src.userequipment import UserEquipment
from src.userequipmenttobasestationlink import UserEquipmentToBaseStationLink
from src.userequipmentcreator import UserEquipmentCreator

#// Backup after Log Removal: Delete it later:

from typing import List

class System:

    def __init__(self):
        self._base_stations = []
        self._base_station_to_user_equipment_links = []
        self.user_equipment = []
        self.user_equipment_to_base_station_links = []
        self.channel = None
        self.slot_duration_in_seconds = 0.5e-3
        self.resource_blocks_per_slot = 3
        self.results_file_handle = None

    @staticmethod
    def add_links_from_base_station(base_station, links_from_base_station):
        for link in links_from_base_station:
            base_station.add_link_from_base_station(link)

    @staticmethod
    def add_links_to_base_station(base_station, links_to_base_station):
        for link in links_to_base_station:
            base_station.add_link_to_base_station(link)

    @staticmethod
    def find_greatest_gain_link(links):
        greatest_gain_link = max(links, key=lambda link: link.gain)
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

    def add_base_station(self, base_station):
        index_of_base_station_in_list = self.find_base_station(base_station)

        if index_of_base_station_in_list == -1:
            self._base_stations.append(base_station)

    def add_user_equipment(self, user_equipment):
        index_of_user_equipment_in_list = self.find_user_equipment(
            user_equipment)

        if index_of_user_equipment_in_list == -1:
            self.user_equipment_list.append(user_equipment)

    def find_base_station(self, base_station):
        return base_station in self._base_stations

    def find_user_equipment(self, user_equipment):
        return user_equipment in self.user_equipment

    def set_all_base_stations_transmit_power_in_watts(self, transmit_power):
        for base_station in self._base_stations:
            base_station.set_transmit_power_in_watts(transmit_power)

    def update_downlink_links(self):
        self._base_station_to_user_equipment_links = []
        for base_station in self._base_stations:
            for user_equipment in self.user_equipment:
                link_channel = self.channel
                link = BaseStationToUserEquipmentLink(link_channel)
                link.base_station = base_station
                link.user_equipment = user_equipment
                link.calculate_link_gain()
                self._base_station_to_user_equipment_links.append(link)

    def update_uplink_links(self):
        self.user_equipment_to_base_station_links = []
        for base_station in self._base_stations:
            for user_equipment in self.user_equipment:
                link_channel = self.channel
                link = UserEquipmentToBaseStationLink(link_channel)
                link.base_station = base_station
                link.user_equipment = user_equipment
                link.calculate_link_gain()
                self.user_equipment_to_base_station_links.append(link)

    def find_links_from_base_station(self, base_station: BaseStation) -> List[BaseStationToUserEquipmentLink]:
        return [link for link in self._base_station_to_user_equipment_links
                if link.base_station == base_station]

    def find_links_to_base_station(self, base_station: BaseStation) -> List[UserEquipmentToBaseStationLink]:
        return [link for link in self.user_equipment_to_base_station_links
                if link.active_in_the_current_slot and link.base_station == base_station]

    def find_links_to_user_equipment(self, user_equipment):
        return [link for link in self._base_station_to_user_equipment_links
                if link.active_in_the_current_slot and link.user_equipment == user_equipment]

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
        for base_station in self._base_stations:
            base_station.initialize_user_equipment_times_scheduled_counters()

    def initialize_base_station_round_robin_schedulers(self):
        for base_station in self._base_stations:
            base_station.set_number_of_resource_blocks_per_slot(
                self.resource_blocks_per_slot)
            base_station.initialize_round_robin_scheduler()
            base_station.inform_associated_user_equipment_to_scheduler()

    def schedule_resource_blocks_for_base_stations(self):
        all_base_stations_schedule = []
        for base_station in self._base_stations:
            slot_schedule = base_station.request_next_schedule_to_scheduler()
            all_base_stations_schedule.append(
                slot_schedule)
        return all_base_stations_schedule

    def inform_base_stations_links(self):
        for base_station in self._base_stations:
            self.inform_downlink_links(base_station)
            self.inform_uplink_links(base_station)

    def inform_downlink_links(self, base_station):
        links_from_base_station = self.find_links_from_base_station(
            base_station)
        self.add_links_from_base_station(
            base_station, links_from_base_station)

    def inform_uplink_links(self, base_station):
        links_to_base_station = self.find_links_to_base_station(
            base_station)
        self.add_links_to_base_station(
            base_station, links_to_base_station)

    def calculate_aggregate_capacity(self):
        self.update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
        self.update_all_user_equipment_reception_capacity()
        aggregate_capacity = 0
        for user_equipment in self.user_equipment:
            aggregate_capacity += user_equipment.current_capacity_in_bits_per_second
        return aggregate_capacity

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

    def update_all_user_equipment_reception_capacity(self):
        for user_equipment in self.user_equipment:
            user_equipment.calculate_reception_capacity()

    def update_all_user_equipment_slot_duration(self):
        for user_equipment in self.user_equipment:
            user_equipment.slot_duration_in_seconds = self.slot_duration_in_seconds

    def calculate_downlink_round_robin_aggregate_throughput_over_number_of_slots(self, number_of_slots):
        current_slot = 1
        total_bits_transmitted = 0

        while current_slot <= number_of_slots:
            bits_transmitted_this_slot = self.calculate_downlink_round_robin_scheduling_slot_transmitted_bits()
            total_bits_transmitted += bits_transmitted_this_slot
            current_slot += 1

            if current_slot % 10 == 0:
                print(f'Current Slot = {current_slot}')

        slot_duration = self.slot_duration_in_seconds
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

    def _create_user_equipments(self, upper_x_bond, upper_y_bond, number_of_ues, default_frequency=None, unique_id=None):
        """Create a specified number of user equipment."""
        user_equipment_creator = UserEquipmentCreator(upper_x_bond, upper_y_bond,)

        for counter in range(number_of_ues):
            self._user_equipment = user_equipment_creator.create_user_equipment(default_frequency, unique_id)
            self._user_equipments.append(self._user_equipment)

        return self._user_equipments

    def _create_base_station(self,upper_x_bond, upper_y_bond, default_frequency=None, unique_id=None):
        """Create a base station."""
        base_station_creator = BaseStationCreator(0, 0)
        self._base_station = base_station_creator.create_fixed_base_station(upper_x_bond, upper_y_bond, default_frequency, unique_id)
        return self._base_station

    @property
    def base_stations(self):
        return self._base_stations

    @property
    def user_equipments(self):
        return self._user_equipments

    @property
    def links(self):
        return self._links

    def clear_base_stations(self):
        self._base_stations = []

    def clear_user_equipments(self):
        self._user_equipments = []

    def configure_basics(self):

        self.set_all_base_stations_transmit_power_in_watts(40)
        self.channel = FreeSpaceChannel(2600e6)
        self.update_all_user_equipment_slot_duration()
        self.update_downlink_links()
        self.update_uplink_links()
        self.inform_base_stations_links()
        self.associate_all_user_equipment()
        self.initialize_base_station_associated_user_equipment_scheduled_counters()
        self.initialize_base_station_round_robin_schedulers()

    def simulate_scenario_1(self):
        self.add_base_station(BaseStation(10, 20))
        self.add_base_station(BaseStation(50, 20))

        self.add_user_equipment(UserEquipment(0, 0))
        self.add_user_equipment(UserEquipment(20, 0))
        self.add_user_equipment(UserEquipment(40, 0))
        self.add_user_equipment(UserEquipment(60, 0))

        self.configure_basics()