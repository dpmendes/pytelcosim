from abc import ABC, abstractmethod

class Scheduler(ABC):
    def __init__(self, number_of_resource_blocks_per_slot):
        self.number_of_resource_blocks_per_slot = number_of_resource_blocks_per_slot
        self.user_equipment_to_be_scheduled_list = []
        self.resource_blocks_served_per_user_equipment_list = []

    @abstractmethod
    def schedule_next_slot(self):
        pass

    def set_number_of_resource_blocks_per_slot(self, number_of_resource_blocks_per_slot):
        self.number_of_resource_blocks_per_slot = number_of_resource_blocks_per_slot
