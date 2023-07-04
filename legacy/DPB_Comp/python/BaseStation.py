from RoundRobinScheduler import RoundRobinScheduler
from Transceiver import Transceiver


class BaseStation(Transceiver):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.number_of_resource_blocks_per_slot = None
        self.scheduler = None
        self.associated_user_equipment = []
        self.user_equipment_times_scheduled = []
        self.links_from_base_station = []
        self.links_to_base_station = []

    def get_associated_user_equipment(self):
        return self.associated_user_equipment

    def associate_user_equipment(self, user_equipment):
        if user_equipment not in self.associated_user_equipment:
            self.associated_user_equipment.append(user_equipment)

    def dissociate_user_equipment(self, user_equipment):
        if user_equipment in self.associated_user_equipment:
            self.associated_user_equipment.remove(user_equipment)

    def get_links_from_base_station(self):
        return self.links_from_base_station

    def add_link_from_base_station(self, link_from_base_station):
        if link_from_base_station not in self.links_from_base_station:
            self.links_from_base_station.append(link_from_base_station)

    def remove_link_from_base_station(self, link_from_base_station):
        if link_from_base_station in self.links_from_base_station:
            self.links_from_base_station.remove(link_from_base_station)

    def get_links_to_base_station(self):
        return self.links_to_base_station

    def add_link_to_base_station(self, link_to_base_station):
        if link_to_base_station not in self.links_to_base_station:
            self.links_to_base_station.append(link_to_base_station)

    def remove_link_to_base_station(self, link_to_base_station):
        if link_to_base_station in self.links_to_base_station:
            self.links_to_base_station.remove(link_to_base_station)

    def get_number_of_resource_blocks_per_slot(self):
        return self.number_of_resource_blocks_per_slot

    def set_number_of_resource_blocks_per_slot(self, number_of_resource_blocks_per_slot):
        self.number_of_resource_blocks_per_slot = number_of_resource_blocks_per_slot

    def initialize_user_equipment_times_scheduled_counters(self):
        number_of_associated_user_equipment = len(self.associated_user_equipment)
        self.user_equipment_times_scheduled = [0] * number_of_associated_user_equipment

    def inform_associated_user_equipment_to_scheduler(self):
        base_station_scheduler = self.scheduler
        base_station_scheduler.update_user_equipment_to_be_scheduled_list(self.associated_user_equipment)
        base_station_scheduler.reset_resource_blocks_served()

    def request_next_schedule_to_scheduler(self):
        base_station_scheduler = self.scheduler
        number_of_resource_blocks = self.number_of_resource_blocks_per_slot
        base_station_scheduler.set_number_of_resource_blocks_per_slot(number_of_resource_blocks)
        slot_schedule = base_station_scheduler.schedule_next_slot()
        self.update_times_served()
        return slot_schedule

    def update_times_served(self):
        scheduler = self.scheduler
        self.user_equipment_times_scheduled = scheduler.get_resource_blocks_served_per_user_equipment_list()

    def initialize_round_robin_scheduler(self):
        self.scheduler = RoundRobinScheduler(self.number_of_resource_blocks_per_slot)

    def find_user_equipment_in_list(self, user_equipment):
            try:
                index_in_list = self.associated_user_equipment.index(user_equipment)
            except ValueError:
                index_in_list = -1
            return index_in_list

    def find_minimum_user_equipment_number_of_times_served(self):
        minimum_user_equipment_number_of_times_served = min(self.user_equipment_times_scheduled)
        return minimum_user_equipment_number_of_times_served

    def count_associated_user_equipment(self):
        number_of_associated_user_equipment = len(self.associated_user_equipment)
        return number_of_associated_user_equipment