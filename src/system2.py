from src.basestation import BaseStation
from src.basestationcreator import BaseStationCreator
from src.basestationtouserequipmentlink import BaseStationToUserEquipmentLink
from src.basestationmanager import BaseStationManager
from src.freespacechannel import FreeSpaceChannel
from src.link import Link
from src.linkmanager import LinkManager
from src.userequipment import UserEquipment
from src.userequipmenttobasestationlink import UserEquipmentToBaseStationLink
from src.userequipmentcreator import UserEquipmentCreator
from src.userequipmentmanager import UserEquipmentManager


class System:

    def __init__(self):
        self._base_stations = []
        self._base_station_to_user_equipment_links = []
        self._user_equipments = []
        self._user_equipment_to_base_station_links = []
        self._channel = None
        self._results_file_handle = None
        self._slot_duration_in_seconds = 0.5e-3
        self._resource_blocks_per_slot = 3
        self._base_station_manager = BaseStationManager(
            self._slot_duration_in_seconds, self._resource_blocks_per_slot)
        self._user_equipment_manager = UserEquipmentManager(
            self._slot_duration_in_seconds, self._resource_blocks_per_slot)
        self._link_manager = LinkManager(
            self._base_stations, self._user_equipments, self._channel)

    @property
    def base_stations(self):
        return self._base_station_manager.base_stations

    @property
    def user_equipments(self):
        return self._user_equipment_manager.user_equipments

    @property
    def links(self):
        return self._link_manager.base_station_to_user_equipment_links + self._link_manager.user_equipment_to_base_station_links

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

    def find_links_to_user_equipment(self, user_equipment):
        return [link for link in self._link_manager.base_station_to_user_equipment_links
                if link.active_in_the_current_slot and link.user_equipment == user_equipment]

    def associate_all_user_equipment(self):
        for user_equipment in self._user_equipment_manager.user_equipments:
            links_to_user_equipment = self.find_links_to_user_equipment(
                user_equipment)
            greatest_gain_link = self._link_manager.find_greatest_gain_link(
                links_to_user_equipment)
            user_equipment.associate_to_base_station(
                greatest_gain_link.base_station)
            base_station = greatest_gain_link.base_station
            base_station.associate_user_equipment(user_equipment)

    def initialize_base_station_round_robin_schedulers(self):
        self._base_station_manager.initialize_base_station_round_robin_schedulers()

    def schedule_resource_blocks_for_base_stations(self):
        return self._base_station_manager.schedule_resource_blocks_for_base_stations()

    def calculate_aggregate_capacity(self):
        self._user_equipment_manager.update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
        self._user_equipment_manager.update_all_user_equipment_reception_capacity()

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

        self._base_station_manager.add_base_station(BaseStation(10, 20))
        self._base_station_manager.add_base_station(BaseStation(50, 20))

        self._user_equipment_manager.add_user_equipment(UserEquipment(0, 0))
        self._user_equipment_manager.add_user_equipment(UserEquipment(20, 0))
        self._user_equipment_manager.add_user_equipment(UserEquipment(40, 0))
        self._user_equipment_manager.add_user_equipment(UserEquipment(60, 0))

        self.configure_basics()
