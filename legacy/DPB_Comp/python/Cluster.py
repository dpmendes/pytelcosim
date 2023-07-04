from CentralUnit import CentralUnit


class Cluster:

    def __init__(self):
        self.cluster_base_stations_list = []
        self.resource_blocks_per_slot = 0
        self.central_unit = None

    def request_schedule_to_central_unit(self):
        return self.central_unit.request_schedule_to_dynamic_point_blanking_scheduler()

    def create_central_unit_coordinating_added_base_stations(self):
        new_central_unit = CentralUnit()
        new_central_unit.set_resource_blocks_per_slot(
            self.resource_blocks_per_slot)
        new_central_unit.receive_base_stations_list(
            self.cluster_base_stations_list)
        new_central_unit.initialize_dynamic_point_blanking_scheduler()
        self.central_unit = new_central_unit

    def set_resource_blocks_per_slot(self, resource_blocks_per_slot):
        self.resource_blocks_per_slot = resource_blocks_per_slot

    def pass_all_links_list_to_central_unit(self, all_links_list):
        self.central_unit.pass_all_links_list_to_scheduler(all_links_list)

    def add_base_station_to_cluster(self, base_station):
        index_of_base_station = self.find_base_station_in_list(base_station)
        if index_of_base_station == -1:
            self.cluster_base_stations_list.append(base_station)

    def remove_base_station_from_cluster(self, base_station):
        index_of_base_station = self.find_base_station_in_list(base_station)
        if index_of_base_station != -1:
            self.cluster_base_stations_list = self.cluster_base_stations_list[:index_of_base_station] + \
                self.cluster_base_stations_list[index_of_base_station + 1:]

    def find_base_station_in_list(self, base_station):
        try:
            index_in_list = self.cluster_base_stations_list.index(base_station)
        except ValueError:
            index_in_list = -1

        return index_in_list
