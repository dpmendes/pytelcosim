from CoordinatedScheduler import CoordinatedScheduler
from DynamicPointBlankingScheduler import DynamicPointBlankingScheduler

class CentralUnit:
    def __init__(self):
        self.scheduler = None
        self.resource_blocks_per_slot = 0
        self.cluster_base_stations_list = []

    def request_schedule_to_dynamic_point_blanking_scheduler(self):
        scheduler = self.scheduler
        cluster_schedule = scheduler.schedule_next_slot()
        return cluster_schedule

    def initialize_coordinated_scheduler(self):
        new_scheduler = CoordinatedScheduler()
        self.scheduler = new_scheduler

    def initialize_dynamic_point_blanking_scheduler(self):
        new_scheduler = DynamicPointBlankingScheduler(self.resource_blocks_per_slot)
        new_scheduler.set_number_of_resource_blocks_per_slot(self.resource_blocks_per_slot)
        new_scheduler.receive_cluster_base_stations_list(self.cluster_base_stations_list)
        new_scheduler.initialize_pivot_counters()
        self.scheduler = new_scheduler

    def receive_base_stations_list(self, base_stations_list):
        self.cluster_base_stations_list = base_stations_list

    def pass_all_links_list_to_scheduler(self, all_links_list):
        scheduler = self.scheduler
        scheduler.receive_all_links_list(all_links_list)

    def set_resource_blocks_per_slot(self, resource_blocks_per_slot):
        self.resource_blocks_per_slot = resource_blocks_per_slot

    def get_current_scheduler(self):
        return self.scheduler


