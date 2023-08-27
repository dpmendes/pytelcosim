from scheduler.base.schedule import Schedule
from scheduler.base.scheduler import Scheduler

import numpy as np

class ProportionalFairScheduler(Scheduler):
    def __init__(self, number_of_resource_blocks_per_slot, ewma_time_constant, starvation_threshold):
        super().__init__(number_of_resource_blocks_per_slot)
        self.ewma_time_constant = ewma_time_constant
        self.starvation_threshold = starvation_threshold
        self.small_constant = 1e-9
        self.T = None  # to be initialized in update_user_equipment_to_be_scheduled_list
        self.slots_since_last_scheduled = None  # to be initialized in update_user_equipment_to_be_scheduled_list

    def update_user_equipment_to_be_scheduled_list(self, user_equipment_to_be_scheduled_list):
        self.user_equipment_to_be_scheduled_list = user_equipment_to_be_scheduled_list
        self.num_users = len(self.user_equipment_to_be_scheduled_list)
        self.T = np.array([self.small_constant] * self.num_users)
        self.slots_since_last_scheduled = np.zeros(self.num_users)

    def schedule_next_slot(self):
        R = np.array([ue.link_capacity for ue in self.user_equipment_to_be_scheduled_list])
        norm_rates = R / (self.T + self.small_constant)

        # Check for starvation
        if np.max(self.slots_since_last_scheduled) >= self.starvation_threshold:
            user = np.argmax(self.slots_since_last_scheduled)
        else:
            user = np.argmax(norm_rates)

        # Update averages:
        self.T = (1 - (1 / self.ewma_time_constant)) * self.T
        self.T[user] += (1 / self.ewma_time_constant) * R[user]

        # Update slots since last scheduled
        self.slots_since_last_scheduled += 1
        self.slots_since_last_scheduled[user] = 0

        slotSchedule = Schedule(self.number_of_resource_blocks_per_slot)
        user_equipment = self.user_equipment_to_be_scheduled_list[user]
        slotSchedule.add_user_to_resource_block(user_equipment)

        return slotSchedule