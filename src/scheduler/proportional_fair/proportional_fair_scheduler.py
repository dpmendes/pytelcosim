import numpy as np
from scheduler.base.schedule import Schedule
from scheduler.base.scheduler import Scheduler


class ProportionalFairScheduler(Scheduler):

    def __init__(self, number_of_resource_blocks_per_slot, ewma_time_constant, starvation_threshold):
        super().__init__(number_of_resource_blocks_per_slot)
        self.ewma_time_constant = ewma_time_constant
        self.starvation_threshold = starvation_threshold
        self.small_constant = 1e-9
        self.num_users = 0
        self.T = np.array([])
        self.slots_since_last_scheduled = np.array([])

    def get_resource_blocks_served_per_user_equipment_list(self):
        return self.resource_blocks_served_per_user_equipment_list

    def update_user_equipment_to_be_scheduled_list(self, user_equipment_to_be_scheduled_list):
        self.user_equipment_to_be_scheduled_list = user_equipment_to_be_scheduled_list
        self.num_users = len(self.user_equipment_to_be_scheduled_list)
        self.resource_blocks_served_per_user_equipment_list = [0] * self.num_users
        self.T = np.array([self.small_constant] * self.num_users)
        self.slots_since_last_scheduled = np.zeros(self.num_users)

    def schedule_next_slot(self):
        R = np.array([ue.current_capacity_in_bits_per_second for ue in self.user_equipment_to_be_scheduled_list])
        slotSchedule = Schedule(self.number_of_resource_blocks_per_slot)
        for _ in range(self.number_of_resource_blocks_per_slot):
            norm_rates = R / (self.T + self.small_constant)

            # Check for starvation
            max_slots_since_last_scheduled = np.max(self.slots_since_last_scheduled)
            if max_slots_since_last_scheduled >= self.starvation_threshold:
                # find all users that are starving
                starving_users = np.argwhere(self.slots_since_last_scheduled == max_slots_since_last_scheduled).flatten()
                # select the starving user with the highest normalized rate
                user = starving_users[np.argmax(norm_rates[starving_users])]
            else:
                user = np.argmax(norm_rates)

            # Update averages:
            self.T = (1 - (1 / self.ewma_time_constant)) * self.T
            self.T[user] += (1 / self.ewma_time_constant) * R[user]

            # Update slots since last scheduled
            self.slots_since_last_scheduled += 1
            self.slots_since_last_scheduled[user] = 0

            user_equipment = self.user_equipment_to_be_scheduled_list[user]
            slotSchedule.add_user_to_resource_block(user_equipment)

            # Update resource blocks served
            self.resource_blocks_served_per_user_equipment_list[user] += 1

        return slotSchedule

    def reset_resource_blocks_served(self):
        self.resource_blocks_served_per_user_equipment_list = [0] * self.num_users

    def remove_user_equipment_from_current_schedule(self, userEquipment):
        pass