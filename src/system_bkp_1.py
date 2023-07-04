import math
from src.basestationcreator import BaseStationCreator
from src.link import Link
from src.userequipmentcreator import UserEquipmentCreator

#// Backup for alpha release for system class. Delete it later
#// Use it for reference when merging with the monitor class;

class System:

    _base_station = None
    _base_stations = None
    _user_equipment = None
    _user_equipments = None
    _links = None

    def __init__(self):
        self._base_stations = []
        self._user_equipments = []
        self._base_station = None
        self._user_equipment = None
        self._links = []

    @staticmethod
    def _calculate_distance_between_points(x1, y1, x2, y2):
        """Calculate the distance between two points."""
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def _clear_connected_user_equipment(self, base_stations):
        """Clear the connected user equipment for each base station."""
        for base_station in base_stations:
            base_station.clear_connected_ues()

    def _calculate_elements_distance(self, base_stations, user_equipments):
        """Calculate the distance between base stations and user equipment."""
        self._clear_connected_user_equipment(self._base_stations)
        for user_equipment in user_equipments:
            closest_bs = None
            closest_distance = float('inf')

            for base_station in base_stations:
                x1, y1 = user_equipment.x, user_equipment.y
                x2, y2 = base_station.x, base_station.y
                d = self._calculate_distance_between_points(x1, y1, x2, y2)

                if d < closest_distance:
                    closest_bs = base_station
                    closest_distance = d

            closest_bs.add_connected_ue(user_equipment)
            user_equipment.connected_bs = closest_bs
            user_equipment.distance_from_bs = closest_distance

    def _calculate_links_capacity(self, base_stations):
        """Calculate the link capacity from base stations to user equipment."""
        self._links = []
        for base_station in base_stations:
            connected_ues = base_station.connected_ues
            try:
                if not connected_ues:
                    raise ValueError("User Equipment object is None")
                else:
                    for connected_ue in connected_ues:
                        link = Link(base_station, connected_ue)
                        link.calculate_link_capacity()
                        link.set_link_capacity(connected_ue)
                        self._links.append(link)
            except ValueError as e:
                print(f"Error: {e}")

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

    def create_scenario_one(self):

        base_station_1 = self._create_base_station(5, 5)
        base_station_2 = self._create_base_station(15, 5)

        self._base_stations.append(base_station_1)
        self._base_stations.append(base_station_2)

        self._user_equipments = self._create_user_equipments(20, 10, 50)
        self._calculate_elements_distance(self._base_stations, self._user_equipments)

        self._links = self._calculate_links_capacity(self._base_stations)

        #// Schedule:
        #// Round Robin:

        #// Proportional Fair:

        #// For each slot calculate the new capacity;