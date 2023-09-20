from transceiver.user_equipment.user_equipment_creator import UserEquipmentCreator


class UserEquipmentManager:
    def __init__(self, slot_duration_in_seconds, resource_blocks_per_slot):
        self._user_equipments = []
        self._slot_duration_in_seconds = slot_duration_in_seconds
        self._resource_blocks_per_slot = resource_blocks_per_slot

    def add_user_equipment(self, user_equipment):
        if not self.find_user_equipment(user_equipment):
            self._user_equipments.append(user_equipment)

    def create_user_equipments(self, mode='FIXED', fixed_x=None, fixed_y=None, number_of_ues=None, frequency=None, bandwidth=None, transmisson_power=None, unique_id=None):
        user_equipment_creator = UserEquipmentCreator()

        for i in range(number_of_ues):
            if mode == 'FIXED':
                if fixed_x is None or fixed_y is None:
                    raise ValueError("x and y coordinates must be provided for 'FIXED' mode.")
                user_equipment = user_equipment_creator.create_fixed_user_equipment(fixed_x, fixed_y, frequency, bandwidth, transmisson_power, unique_id)
            elif mode == 'RANDOM':
                if fixed_x is None or fixed_y is None:
                    raise ValueError("Upper x and y bounds must be provided for 'RANDOM' mode.")
                unique_id_random = f"User-{i+1}"
                user_equipment = user_equipment_creator.create_random_user_equipment(fixed_x, fixed_y, frequency, bandwidth, transmisson_power, unique_id_random)
            else:
                raise ValueError(f"Invalid mode '{mode}'. Must be 'FIXED' or 'RANDOM'.")

            self.add_user_equipment(user_equipment)


    def find_user_equipment(self, user_equipment):
        return user_equipment in self._user_equipments

    def update_all_user_equipment_reception_capacity(self):
        for user_equipment in self._user_equipments:
            user_equipment.calculate_reception_capacity()

    def update_all_user_equipment_slot_duration(self, slot_duration_in_seconds):
        self._slot_duration_in_seconds = slot_duration_in_seconds
        for user_equipment in self._user_equipments:
            user_equipment.slot_duration_in_seconds = self._slot_duration_in_seconds

    def clear_user_equipments(self):
        self._user_equipments = []

    @property
    def user_equipments(self):
        return self._user_equipments
