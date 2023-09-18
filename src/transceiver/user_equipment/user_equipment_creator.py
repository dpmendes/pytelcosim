from transceiver.base.element_creator import ElementCreator
from transceiver.user_equipment.user_equipment import UserEquipment

class UserEquipmentCreator(ElementCreator):
    """A class to create instances of UserEquipment."""

    def create_random_user_equipment(self, upper_x_bound, upper_y_bound, frequency, bandwidth, transmisson_power, unique_id=None):
        element = super().create_random_element(upper_x_bound, upper_y_bound, frequency, bandwidth, transmisson_power, unique_id)
        return UserEquipment(element.x, element.y, element.frequency, element.bandwidth, element.transmisson_power, element.unique_id)

    def create_fixed_user_equipment(self, x, y, frequency, bandwidth, transmisson_power, unique_id=None):
        element = super().create_fixed_element(x, y, frequency, bandwidth, transmisson_power, unique_id)
        return UserEquipment(element.x, element.y, element.frequency, element.bandwidth, element.transmisson_power, element.unique_id)
