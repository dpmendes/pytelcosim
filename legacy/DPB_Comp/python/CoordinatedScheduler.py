from Scheduler import Scheduler


class CoordinatedScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        self.cluster_base_stations_list = []
        self.all_links_list = []
        self.times_a_base_station_has_been_the_pivot = []
        self.current_pivot_base_station = None

    def receive_cluster_base_stations_list(self, cluster_base_stations_list):
        self.cluster_base_stations_list = cluster_base_stations_list

    def receive_all_links_list(self, all_links_list):
        self.all_links_list = all_links_list

    def initialize_pivot_counters(self):
        num_base_stations_in_cluster = len(self.cluster_base_stations_list)
        self.times_a_base_station_has_been_the_pivot = [
            0] * num_base_stations_in_cluster

    def schedule_next_slot(self):
        pivot_base_station = self.select_pivot_base_station()
        self.current_pivot_base_station = pivot_base_station
        slot_schedule = self.pivot_round_robin_schedule()
        slot_schedule.extend(
            self.schedule_users_from_non_pivot_base_stations())
        return slot_schedule

    def select_pivot_base_station(self):
        minimum_user_equipment_number_of_times_served = 0
        num_base_stations_in_cluster = len(self.cluster_base_stations_list)
        pivot_base_station = None

        for i in range(num_base_stations_in_cluster):
            base_station = self.cluster_base_stations_list[i]
            min_num_times_served_for_base_station = base_station.find_minimum_user_equipment_number_of_times_served()

            if min_num_times_served_for_base_station < minimum_user_equipment_number_of_times_served:
                minimum_user_equipment_number_of_times_served = min_num_times_served_for_base_station
                pivot_base_station = base_station

        self.current_pivot_base_station = pivot_base_station
        self.update_times_a_base_station_has_been_the_pivot(pivot_base_station)
        return pivot_base_station

    def update_times_a_base_station_has_been_the_pivot(self, pivot_base_station):
        pivot_base_station_index = self.cluster_base_stations_list.index(
            pivot_base_station)
        self.times_a_base_station_has_been_the_pivot[pivot_base_station_index] += 1

    def pivot_round_robin_schedule(self):
        pivot_base_station = self.current_pivot_base_station
        return pivot_base_station.request_next_schedule_to_scheduler()

    def schedule_users_from_non_pivot_base_stations(self):
        slot_schedule = []
        for base_station in self.cluster_base_stations_list:
            if base_station != self.current_pivot_base_station:
                new_slot_schedule = self.find_less_interfering_user_equipment_permutation_with_repetition(
                    base_station)
                slot_schedule.extend(new_slot_schedule)
        return slot_schedule

    def find_less_interfering_user_equipment_permutation_with_repetition(this_object, base_station):
        user_equipment_list = base_station.get_associated_user_equipment_list()
        number_of_user_equipment = len(user_equipment_list)
        number_of_resource_blocks = this_object.number_of_resource_blocks_per_slot
        number_of_permutations_with_repetition = number_of_user_equipment ** number_of_resource_blocks
        return number_of_permutations_with_repetition
