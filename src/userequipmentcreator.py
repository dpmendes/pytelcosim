from src.elementcreator import ElementCreator
from src.userequipment import UserEquipment


class UserEquipmentCreator(ElementCreator):
    """A class to create instances of UserEquipment."""

    def create_user_equipment(self, frequency: float, unique_id: str):
        return UserEquipment(self._draw_position(self._upper_x_bound), self._draw_position(self._upper_y_bound), frequency, unique_id)

    def create_fixed_user_equipment(self, x: float, y: float, frequency: float, unique_id: str):
        return UserEquipment(x, y, frequency, unique_id)
