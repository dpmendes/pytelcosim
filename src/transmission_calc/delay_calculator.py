from transceiver.user_equipment.user_equipment import UserEquipment

class DelayCalculator:

    @staticmethod
    def _calculate_average_transmission_delay(user_equipment):
        """Calculates the average transmission delay based on the recorded slots.

        Args:
            user_equipment (UserEquipment): The user equipment instance.

        Returns:
            float: Average transmission delay in seconds.
        """
        if not isinstance(user_equipment, UserEquipment):
            raise ValueError("Provided object is not an instance of UserEquipment")
        if len(user_equipment.get_transmission_slots()) < 2:
            return 0

        delays = []
        transmission_slots = user_equipment.get_transmission_slots()
        for i in range(1, len(transmission_slots)):
            delay = (transmission_slots[i] - transmission_slots[i - 1]) * user_equipment.slot_duration_in_seconds
            delays.append(delay)

        average_delay = sum(delays) / len(delays)
        user_equipment.transmission_delay = average_delay
        return average_delay

    @staticmethod
    def calculate_delays(user_equipments_list):
        """
        Calculates the average transmission delay for each user equipment in the list.

        Returns:
            dict: Dictionary with user equipment unique IDs as keys and their average delays as values.
        """
        average_delays = {}
        for ue in user_equipments_list:
            average_delay = DelayCalculator._calculate_average_transmission_delay(ue)
            average_delays[ue.unique_id] = average_delay
        return average_delays


