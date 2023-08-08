from basestationtouserequipmentlink import BaseStationToUserEquipmentLink
from userequipmenttobasestationlink import UserEquipmentToBaseStationLink


class LinkManager:
    def __init__(self, base_stations, user_equipments, channel):
        self._base_stations = base_stations
        self._user_equipments = user_equipments
        self._channel = channel
        self._base_station_to_user_equipment_links = []
        self._user_equipment_to_base_station_links = []

    @staticmethod
    def get_highest_gain_link_from_list(links):
        return max(links, key=lambda link: link.gain)

    def create_link(self, link_type, source_node, destination_node, channel):
        link = link_type(source_node, destination_node, channel)
        link.calculate_link_gain()
        return link

    def update_channel(self, new_channel):
        if new_channel != self._channel:
            self._channel = new_channel
            for link in self._base_station_to_user_equipment_links:
                link.channel = new_channel
                link.calculate_link_gain()
            for link in self._user_equipment_to_base_station_links:
                link.channel = new_channel
                link.calculate_link_gain()

    def update_links(self):
        self.update_downlink_links()
        self.update_uplink_links()

    def update_downlink_links(self):
        self._base_station_to_user_equipment_links = []
        for bs in self._base_stations:
            for ue in self._user_equipments:
                link = self.create_link(BaseStationToUserEquipmentLink, bs, ue, self._channel)
                self._base_station_to_user_equipment_links.append(link)
            self.inform_downlink_links(bs)

    def update_uplink_links(self):
        self._user_equipment_to_base_station_links = []
        for bs in self._base_stations:
            for ue in self._user_equipments:
                link = self.create_link(UserEquipmentToBaseStationLink, ue, bs, self._channel)
                self._user_equipment_to_base_station_links.append(link)
            self.inform_uplink_links(bs)

    def find_links_to_user_equipment(self, user_equipment, only_active=True):
        return [link for link in self._base_station_to_user_equipment_links
                if (not only_active or link.active_in_the_current_slot) and link.destination_node == user_equipment]

    def find_links_from_base_station(self, base_station, only_active=True):
        return [link for link in self._base_station_to_user_equipment_links
                if (not only_active or link.active_in_the_current_slot) and link.source_node == base_station]

    def inform_downlink_links(self, base_station):
        links_from_base_station = self.find_links_from_base_station(base_station, only_active=False)
        base_station.outgoing_links = links_from_base_station

    def find_links_to_base_station(self, base_station, only_active=True):
        return [link for link in self._user_equipment_to_base_station_links
                if (not only_active or link.active_in_the_current_slot) and link.destination_node == base_station]

    def inform_uplink_links(self, base_station):
        links_to_base_station = self.find_links_to_base_station(base_station, only_active=False)
        base_station.incoming_links = links_to_base_station

    def associate_all_user_equipment(self):
        for user_equipment in self._user_equipments:
            links_to_user_equipment = self.find_links_to_user_equipment(user_equipment)
            greatest_gain_link = self.get_highest_gain_link_from_list(links_to_user_equipment)
            user_equipment.connected_base_station = greatest_gain_link.destination_node
            base_station = greatest_gain_link.source_node
            base_station.connected_user_equipment = user_equipment

    @property
    def base_station_to_user_equipment_links(self):
        return self._base_station_to_user_equipment_links

    @property
    def user_equipment_to_base_station_links(self):
        return self._user_equipment_to_base_station_links

    @property
    def base_stations(self):
        return self._base_stations

    @base_stations.setter
    def base_stations(self, base_stations):
        self._base_stations = base_stations

    @property
    def user_equipments(self):
        return self._user_equipments

    @user_equipments.setter
    def user_equipments(self, user_equipments):
        self._user_equipments = user_equipments