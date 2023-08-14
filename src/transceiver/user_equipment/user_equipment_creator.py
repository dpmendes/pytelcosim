from transceiver.base.element_creator import ElementCreator
from transceiver.user_equipment.user_equipment import UserEquipment


class UserEquipmentCreator(ElementCreator):
    """A class to create instances of UserEquipment."""

    def create_user_equipment(self, frequency: float, unique_id: str):
        element = self.create_random_element(frequency)
        return UserEquipment(element.x, element.y, element.frequency, unique_id)

    def create_fixed_user_equipment(self, x: float, y: float, frequency: float, unique_id: str):
        element = self.create_fixed_element(x, y, frequency)
        return UserEquipment(element.x, element.y, element.frequency, unique_id)
