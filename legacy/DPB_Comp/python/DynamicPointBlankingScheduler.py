from Scheduler import Scheduler


class DynamicPointBlankingScheduler(Scheduler):
    def __init__(self, number_of_resource_blocks_per_slot):
        super().__init__(number_of_resource_blocks_per_slot)
        self.cluster_base_stations_list = []
        self.times_a_base_station_has_been_the_pivot = []
        self.current_pivot_base_station = None

    def receive_cluster_base_stations_list(self, cluster_base_stations_list):
        self.cluster_base_stations_list = cluster_base_stations_list

    def initialize_pivot_counters(self):
        number_of_base_stations_in_cluster = len(
            self.cluster_base_stations_list)
        self.times_a_base_station_has_been_the_pivot = [
            0] * number_of_base_stations_in_cluster

    def schedule_next_slot(self):
        self.select_pivot_base_station()
        cluster_schedule = self.pivot_round_robin_schedule()
        cluster_schedule.extend(self.schedule_non_pivot_base_station_users())
        return cluster_schedule

    def select_pivot_base_station(self):
        minimum_user_equipment_number_of_times_served = 1e20
        pivot_base_station = None
        number_of_base_stations_in_cluster = len(
            self.cluster_base_stations_list)
        for i in range(number_of_base_stations_in_cluster):
            base_station = self.cluster_base_stations_list[i]
            minimum_user_equipment_number_of_times_served_for_base_station = base_station.find_minimum_user_equipment_number_of_times_served()
            if minimum_user_equipment_number_of_times_served_for_base_station <= minimum_user_equipment_number_of_times_served:
                minimum_user_equipment_number_of_times_served = minimum_user_equipment_number_of_times_served_for_base_station
                pivot_base_station = base_station
        self.current_pivot_base_station = pivot_base_station
        self.update_times_a_base_station_has_been_the_pivot(pivot_base_station)

    def update_times_a_base_station_has_been_the_pivot(self, pivot_base_station):
        pivot_base_station_index = self.cluster_base_stations_list.index(
            pivot_base_station)
        self.times_a_base_station_has_been_the_pivot[pivot_base_station_index] += 1

    def pivot_round_robin_schedule(self):
        pivot_base_station = self.current_pivot_base_station
        pivot_base_station.set_number_of_resource_blocks_per_slot(
            self.number_of_resource_blocks_per_slot)
        slot_schedule = pivot_base_station.request_next_schedule_to_scheduler()
        return slot_schedule

    def schedule_non_pivot_base_station_users(self):
        non_pivot_schedule = []
        for i in range(len(self.cluster_base_stations_list)):
            base_station = self.cluster_base_stations_list[i]
            if base_station == self.current_pivot_base_station:
                continue
            resource_blocks_considering_one_free = self.number_of_resource_blocks_per_slot - 1
            base_station.set_number_of_resource_blocks_per_slot(
                resource_blocks_considering_one_free)
            base_station_schedule = base_station.request_next_schedule_to_scheduler()
            base_station_schedule.shift_users_in_resource_blocks_to_the_right()
            resource_blocks = resource_blocks_considering_one_free + 1
            self.number_of_resource_blocks_per_slot = resource_blocks
            base_station.set_number_of_resource_blocks_per_slot(
                resource_blocks)
            non_pivot_schedule.extend(base_station_schedule)
        return non_pivot_schedule
