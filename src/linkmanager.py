from src.basestation import BaseStation
from src.basestationtouserequipmentlink import BaseStationToUserEquipmentLink
from src.link import Link
from src.channel import Channel
from src.userequipment import UserEquipment
from src.userequipmenttobasestationlink import UserEquipmentToBaseStationLink


class LinkManager:
    def __init__(self, base_stations, user_equipment, channel):
        self._base_stations = base_stations
        self._user_equipment = user_equipment
        self._channel = channel
        self.base_station_to_user_equipment_links = []
        self.user_equipment_to_base_station_links = []

    @staticmethod
    def find_greatest_gain_link(links):
        return = max(links, key=lambda link: link.gain)

    def create_link(self, LinkType, base_station, user_equipment, channel):
        link = LinkType(channel)
        link.base_station = base_station
        link.user_equipment = user_equipment
        link.calculate_link_gain()
        return link

    def update_downlink_links(self):
        self.base_station_to_user_equipment_links = []
        for base_station in self._base_stations:
            for user_equipment in self._user_equipment:
                link = self.create_link(
                    BaseStationToUserEquipmentLink, base_station, user_equipment, self._channel)
                self.base_station_to_user_equipment_links.append(link)

    def update_uplink_links(self):
        self._user_equipment_to_base_station_links = []
        for base_station in self._base_stations:
            for user_equipment in self._user_equipment:
                link = self.create_link(
                    UserEquipmentToBaseStationLink, base_station, user_equipment, self._channel)
                self.user_equipment_to_base_station_links.append(link)

    def find_links_from_base_station(self, base_station):
        return [link for link in self.base_station_to_user_equipment_links if link.base_station == base_station]

    def inform_downlink_links(self, base_station):
        links_from_base_station = self.find_links_from_base_station(
            base_station)
        base_station.add_links_from_base_station(links_from_base_station)

    def find_links_to_base_station(self, base_station: BaseStation):
        return [link for link in self.user_equipment_to_base_station_links if link.active_in_the_current_slot and link.base_station == base_station]

    def inform_uplink_links(self, base_station):
        links_to_base_station = self.find_links_to_base_station(base_station)
        base_station.add_links_to_base_station(links_to_base_station)
