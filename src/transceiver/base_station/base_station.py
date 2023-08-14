from scheduler.round_robin.round_robin_scheduler import RoundRobinScheduler
from transceiver.base.element import Element


class BaseStation(Element):

    def __init__(self, x, y, frequency=None, unique_id=None):
        super().__init__(x, y, frequency, unique_id)
        self._number_of_resource_blocks_per_slot = 0
        self._scheduler = None
        self._connected_user_equipment = []
        self._incoming_links = []
        self._outgoing_links = []
        self._user_equipment_times_scheduled = []

    @property
    def connected_user_equipment(self):
        return self._connected_user_equipment

    @connected_user_equipment.setter
    def connected_user_equipment(self, user_equipment):
        if user_equipment not in self._connected_user_equipment:
            self._connected_user_equipment.append(user_equipment)

    def find_user_equipment_in_list(self, user_equipment):
        try:
            return self._connected_user_equipment.index(user_equipment)
        except ValueError:
            return -1

    def count_connected_user_equipment(self):
        number_of_connected_user_equipment = len(
            self._connected_user_equipment)
        return number_of_connected_user_equipment

    def remove_connected_user_equipment(self, user_equipment):
        if user_equipment in self._connected_user_equipment:
            self._connected_user_equipment.remove(user_equipment)

    def clear_connected_ues(self):
        self._connected_user_equipment = []

    @property
    def outgoing_links(self):
        return self._outgoing_links

    @outgoing_links.setter
    def outgoing_links(self, outgoing_link):
        if outgoing_link not in self._outgoing_links:
            self._outgoing_links.append(outgoing_link)

    def remove_outgoing_link(self, outgoing_link):
        if outgoing_link in self._outgoing_links:
            self._outgoing_links.remove(outgoing_link)

    @property
    def incoming_links(self):
        return self._incoming_links

    @incoming_links.setter
    def incoming_links(self, incoming_link):
        if incoming_link not in self._incoming_links:
            self._incoming_links.append(incoming_link)

    def remove_incoming_link(self, incoming_link):
        if incoming_link in self._incoming_links:
            self._incoming_links.remove(incoming_link)

    @property
    def number_of_resource_blocks_per_slot(self):
        return self._number_of_resource_blocks_per_slot

    @number_of_resource_blocks_per_slot.setter
    def number_of_resource_blocks_per_slot(self, number_of_resource_blocks_per_slot):
        self._number_of_resource_blocks_per_slot = number_of_resource_blocks_per_slot

    def initialize_user_equipment_times_scheduled_counters(self):
        number_of_connected_user_equipment = len(
            self._connected_user_equipment)
        self._user_equipment_times_scheduled = [
                                                   0] * number_of_connected_user_equipment

    def inform_connected_user_equipment_to_scheduler(self):
        base_station_scheduler = self._scheduler
        base_station_scheduler.update_user_equipment_to_be_scheduled_list(
            self._connected_user_equipment)
        base_station_scheduler.reset_resource_blocks_served()

    def request_next_schedule_to_scheduler(self):
        base_station_scheduler = self._scheduler
        number_of_resource_blocks = self.number_of_resource_blocks_per_slot
        base_station_scheduler.set_number_of_resource_blocks_per_slot(number_of_resource_blocks)
        slot_schedule = base_station_scheduler.schedule_next_slot()
        self.update_times_served()
        return slot_schedule

    def update_times_served(self):
        scheduler = self._scheduler
        self._user_equipment_times_scheduled = scheduler.get_resource_blocks_served_per_user_equipment_list()

    def initialize_round_robin_scheduler(self):
        self._scheduler = RoundRobinScheduler(self.number_of_resource_blocks_per_slot)

    def __str__(self) -> str:
        return f"BaseStation: ID={self._unique_id}, Location=({self._x:.2f},{self._y:.2f}), Frequency={self._frequency:.2f}"
