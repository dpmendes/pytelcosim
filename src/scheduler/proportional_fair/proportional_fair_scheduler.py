# The primary concept behind the Proportional Fair (PF) scheduler is to select a user u based on the ratio of the instantaneous rate ru to its average throughput Tu. The user with the highest ratio gets scheduled.

# Please note the following:
# This assumes that each user equipment (ue) provides an instantaneous rate using a method like get_instantaneous_rate(). You might need to implement this function based on how you model the user equipment and its conditions.
# The averaged throughput for each user equipment is updated whenever they're scheduled.
# We are using the value 20.0 as the constant ��tC (equivalent to the EWMA constant in your original PF code). You can adjust it as required.
# This class should give you a starting point for a proportional fair scheduler. You might need to adjust and improve it based on the specifics of your simulation and environment.


# Please note the following:
# This assumes that each user equipment (ue) provides an instantaneous rate using a method like get_instantaneous_rate(). You might need to implement this function based on how you model the user equipment and its conditions.
# The averaged throughput for each user equipment is updated whenever they're scheduled.
# We are using the value 20.0 as the constant tC (equivalent to the EWMA constant in your original PF code). You can adjust it as required.
# This class should give you a starting point for a proportional fair scheduler. You might need to adjust and improve it based on the specifics of your simulation and environment.

# The constant tC is not necessarily equivalent to the number of slots. Instead, it's related to the Exponential Weighted Moving Average (EWMA) filter and is used to determine how quickly the scheduler reacts to changes in instantaneous rates.
# Here's an intuition:
# When tC is small (e.g., close to 1), the averaged throughput T is highly influenced by recent rates, making the scheduler react quickly to changes.
# When tC is large, T changes more slowly and is less influenced by recent instantaneous rates, making the scheduler more stable and less responsive to instantaneous changes.
# In the context of proportional fair scheduling:
# A small tC can make the scheduler quickly adapt to users whose conditions improve suddenly, ensuring fairness in the short term.
# A large tC can make the scheduler prioritize users who've had consistently good rates over those who only recently improved, ensuring fairness in the long term.
# So, tC is a design parameter that balances short-term and long-term fairness. It's not directly related to the number of slots. Instead, it's more about how much weight you want to give to recent rates versus historical rates in making scheduling decisions.
# However, it's worth noting that if you know you have a fixed number of slots over which you want to average, you could set tC roughly to that number. Still, in most cases, you'll want to tune tC based on the desired system behavior rather than strictly tie it to the number of slots.


from scheduler.base.schedule import Schedule
from scheduler.base.scheduler import Scheduler

class ProportionalFairScheduler(Scheduler):
    def __init__(self, number_of_resource_blocks_per_slot):
        super().__init__(number_of_resource_blocks_per_slot)
        self.averaged_throughputs = []

    def schedule_next_slot(self):
        userEquipmentList = self.user_equipment_to_be_scheduled_list
        instantaneous_rates = [ue.current_capacity_in_bits_per_second() for ue in userEquipmentList]

        #// Calculate normalized rates (instantaneous rate / averaged throughput)
        if not self.averaged_throughputs:
            #// Initialize averaged_throughputs with instantaneous rates if it's empty
            self.averaged_throughputs = [rate for rate in instantaneous_rates]
        normalized_rates = [instantaneous_rates[i] / self.averaged_throughputs[i] for i in range(len(userEquipmentList))]

        slotSchedule = Schedule(self.number_of_resource_blocks_per_slot)
        for i in range(self.number_of_resource_blocks_per_slot):
            #// Select user with the maximum normalized rate
            userIndex = normalized_rates.index(max(normalized_rates))
            user_equipment = userEquipmentList[userIndex]
            slotSchedule.add_user_to_resource_block(user_equipment)

            #// Update the averaged throughput for the selected user equipment
            self.averaged_throughputs[userIndex] = (1 - (1 / 20.0)) * self.averaged_throughputs[userIndex] + (1 / 20.0) * instantaneous_rates[userIndex]

            #// Set the normalized rate to -1 so that this user is not picked again in this iteration
            normalized_rates[userIndex] = -1

        return slotSchedule

    def reset_averaged_throughputs(self):
        self.averaged_throughputs = [0 for _ in self.user_equipment_to_be_scheduled_list]

    def update_user_equipment_to_be_scheduled_list(self, user_equipment_to_be_scheduled_list):
        super().update_user_equipment_to_be_scheduled_list(user_equipment_to_be_scheduled_list)
        self.reset_averaged_throughputs()
