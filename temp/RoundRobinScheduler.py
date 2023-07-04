from Schedule import Schedule
from Scheduler import Scheduler


class RoundRobinScheduler(Scheduler):
    def __init__(self, number_of_resource_blocks_per_slot):
        super().__init__(number_of_resource_blocks_per_slot)

    def schedule_next_slot(self):
        userEquipmentList = self.user_equipment_to_be_scheduled_list
        timesServedList = self.resource_blocks_served_per_user_equipment_list
        slotSchedule = Schedule(self.number_of_resource_blocks_per_slot)
        for i in range(self.number_of_resource_blocks_per_slot):
            lessServedIndex = timesServedList.index(min(timesServedList))
            timesServedList[lessServedIndex] += 1
            user_equipment = userEquipmentList[lessServedIndex]
            slotSchedule.add_user_to_resource_block(user_equipment)
        self.resource_blocks_served_per_user_equipment_list = timesServedList
        return slotSchedule

    def reset_resource_blocks_served(self):
        self.resource_blocks_served_per_user_equipment_list = [
            0 for _ in self.user_equipment_to_be_scheduled_list]

    def update_user_equipment_to_be_scheduled_list(self, user_equipment_to_be_scheduled_list):
        self.user_equipment_to_be_scheduled_list = user_equipment_to_be_scheduled_list

    def update_resource_blocks_served_per_user_equipment_list(self, resource_blocks_served_per_user_equipment_list):
        self.resource_blocks_served_per_user_equipment_list = resource_blocks_served_per_user_equipment_list

    def get_resource_blocks_served_per_user_equipment_list(self):
        return self.resource_blocks_served_per_user_equipment_list

    def find_user_equipment_index_in_list(self, userEquipment):
        try:
            userEquipmentIndex = self.user_equipment_to_be_scheduled_list.index(
                userEquipment)
        except ValueError:
            userEquipmentIndex = -1
        return userEquipmentIndex

    def remove_user_equipment_from_current_schedule(self, userEquipment):
        pass
