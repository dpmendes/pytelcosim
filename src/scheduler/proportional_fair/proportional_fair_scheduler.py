import numpy as np
from scheduler.base.schedule import Schedule
from scheduler.base.scheduler import Scheduler


class ProportionalFairScheduler(Scheduler):

    def __init__(self, number_of_resource_blocks_per_slot, ewma_time_constant, starvation_threshold, starvation_flag=False):
        super().__init__(number_of_resource_blocks_per_slot)
        self._small_constant = 1e-9
        self.ewma_time_constant = ewma_time_constant
        self.starvation_threshold = starvation_threshold
        self.starvation_flag = starvation_flag
        self.num_users = 0
        self.T = np.array([])
        self.slots_since_last_scheduled = np.array([])

    def get_resource_blocks_served_per_user_equipment_list(self):
        return self.resource_blocks_served_per_user_equipment_list

    def update_user_equipment_to_be_scheduled_list(self, user_equipment_to_be_scheduled_list):
        new_T = []
        for ue in user_equipment_to_be_scheduled_list:
            # Check if this user was already in the list:
            if ue in self.user_equipment_to_be_scheduled_list:
                index = self.user_equipment_to_be_scheduled_list.index(ue)
                new_T.append(self.T[index])
            else:
                new_T.append(self._small_constant)

        self.user_equipment_to_be_scheduled_list = user_equipment_to_be_scheduled_list
        self.num_users = len(self.user_equipment_to_be_scheduled_list)
        self.resource_blocks_served_per_user_equipment_list = [0] * self.num_users
        self.T = np.array(new_T)
        self.slots_since_last_scheduled = np.zeros(self.num_users)

    def schedule_next_slot(self):
        R = np.array([ue.current_capacity_in_bits_per_second for ue in self.user_equipment_to_be_scheduled_list])
        slotSchedule = Schedule(self.number_of_resource_blocks_per_slot)
        # We will store the indices of users that have already been scheduled this slot:
        users_already_scheduled = set()
        for _ in range(self.number_of_resource_blocks_per_slot):
            # norm_rates = R / (self.T + self._small_constant)

            norm_rates = R / (self.T + self._small_constant)
            for user in users_already_scheduled:
                norm_rates[user] = -1

            if self.starvation_flag:
                # Check for starvation:
                max_slots_since_last_scheduled = np.max(
                    self.slots_since_last_scheduled)
                if max_slots_since_last_scheduled >= self.starvation_threshold:
                    starving_users = np.argwhere(
                        self.slots_since_last_scheduled == max_slots_since_last_scheduled).flatten()
                    user = starving_users[np.argmax(
                        norm_rates[starving_users])]
                else:
                    user = np.argmax(norm_rates)
            else:
                user = np.argmax(norm_rates)

            # Add the selected user to the list of scheduled users for this slot:
            users_already_scheduled.add(user)

            # Update averages:
            self.T = (1 - (1 / self.ewma_time_constant)) * self.T
            self.T[user] += (1 / self.ewma_time_constant) * R[user]

            # Update slots since last scheduled:
            self.slots_since_last_scheduled += 1
            self.slots_since_last_scheduled[user] = 0

            user_equipment = self.user_equipment_to_be_scheduled_list[user]
            slotSchedule.add_user_to_resource_block(user_equipment)

            # Update resource blocks served:
            self.resource_blocks_served_per_user_equipment_list[user] += 1

        return slotSchedule

    def reset_resource_blocks_served(self):
        self.resource_blocks_served_per_user_equipment_list = [0] * self.num_users

    def remove_user_equipment_from_current_schedule(self, userEquipment):
        pass
