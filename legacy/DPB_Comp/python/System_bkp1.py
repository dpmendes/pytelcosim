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
            base_station.add_link_from_base_station(link)

    @staticmethod
    def find_greatest_gain_link(links_list):
        greatest_gain_link = max(links_list, key=lambda link: link.gain)
        return greatest_gain_link

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

    def update_all_user_equipment_slot_duration(self):
        for user_equipment in self.user_equipment_list:
            user_equipment.slot_duration_in_seconds = self.slot_duration_in_seconds

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
        links_to_user_equipment = []
        for link in self.base_station_to_user_equipment_links_list:
            if link.active_in_the_current_slot and link.user_equipment == user_equipment:
                links_to_user_equipment.append(link)
        return links_to_user_equipment

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

    def form_clusters(self):
        cluster = Cluster()
        for base_station in self.base_stations_list:
            cluster.add_base_station_to_cluster(base_station)

        cluster.set_resource_blocks_per_slot(self.resource_blocks_per_slot)
        cluster.create_central_unit_coordinating_added_base_stations()
        links_list = self.base_station_to_user_equipment_links_list
        self.clusters_list.append(cluster)

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

    def calculate_aggregate_capacity(self):
        self.update_all_user_equipment_reception_capacity()
        aggregate_capacity = 0
        for user_equipment in self.user_equipment_list:
            aggregate_capacity += user_equipment.current_capacity_in_bits_per_second
        return aggregate_capacity

    def update_all_user_equipment_reception_capacity(self):
        for user_equipment in self.user_equipment_list:
            user_equipment.calculate_reception_capacity()

    def configure_basics(self):
        self.channel = FreeSpaceChannel(2600e6)
        self.update_all_user_equipment_slot_duration()
        self.update_downlink_links_list()
        self.update_uplink_links_list()
        self.inform_base_stations_links()
        self.associate_all_user_equipment()
        self.initialize_base_station_associated_user_equipment_scheduled_counters()
        self.initialize_base_station_round_robin_schedulers()
        self.update_all_user_equipment_reception_capacity()
        self.form_clusters()

    def configure_downlink_test(self):
        self.set_all_base_stations_transmit_power_in_watts(50)
        self.configure_basics()

    def load_test_scenario_1(self):
        self.add_base_station(BaseStation(10, 20))
        self.add_base_station(BaseStation(50, 20))
        self.add_user_equipment(UserEquipment(0, 0))
        self.add_user_equipment(UserEquipment(20, 0))
        self.add_user_equipment(UserEquipment(40, 0))
        self.add_user_equipment(UserEquipment(60, 0))
        self.configure_downlink_test()
