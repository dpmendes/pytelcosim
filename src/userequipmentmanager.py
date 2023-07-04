from src.userequipment import UserEquipment
from src.userequipmentcreator import UserEquipmentCreator


class UserEquipmentManager:
    def __init__(self, slot_duration_in_seconds, resource_blocks_per_slot):
        self._user_equipments = []
        self._slot_duration_in_seconds = slot_duration_in_seconds
        self._resource_blocks_per_slot = resource_blocks_per_slot

    def add_user_equipment(self, user_equipment):
        if not self.find_user_equipment(user_equipment):
            self._user_equipments.append(user_equipment)

    def find_user_equipment(self, user_equipment):
        return user_equipment in self._user_equipments

    def update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio(self):
        for user_equipment in self._user_equipments:
            links_to_user_equipment = self.find_links_to_user_equipment(
                user_equipment)
            intended_signal = self.calculate_intended_signal_to_user_equipment(
                user_equipment, links_to_user_equipment)
            interfering_signal = self.calculate_interfering_signal_at_user_equipment(
                user_equipment, links_to_user_equipment)
            user_equipment.update_signal_to_interference_plus_noise_ratio(
                intended_signal, interfering_signal)

    def update_all_user_equipment_reception_capacity(self):
        for user_equipment in self._user_equipments:
            user_equipment.calculate_reception_capacity()

    def update_all_user_equipment_slot_duration(self):
        for user_equipment in self._user_equipments:
            user_equipment.slot_duration_in_seconds = self._slot_duration_in_seconds

    def create_user_equipments(self, upper_x_bound, upper_y_bound, number_of_ues, default_frequency=None, unique_id=None):

        user_equipment_creator = UserEquipmentCreator(
            upper_x_bound, upper_y_bound,)

        for _ in range(number_of_ues):
            user_equipment = user_equipment_creator.create_user_equipment(
                default_frequency, unique_id)
            self._user_equipments.append(user_equipment)

        return self._user_equipments

    def clear_user_equipments(self):
        self._user_equipments = []

    @property
    def user_equipments(self):
        return self._user_equipments
