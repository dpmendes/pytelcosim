# import sys
# import os
import unittest
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.userequipmentcreator import UserEquipmentCreator
from src.userequipment import UserEquipment

class TestUserEquipmentCreator(unittest.TestCase):

    def setUp(self):
        self.upper_x_bound = 100
        self.upper_y_bound = 100
        self.user_equipment_creator = UserEquipmentCreator(self.upper_x_bound, self.upper_y_bound)

    def test_create_user_equipment(self):
        frequency = 2.4e9
        unique_id = "ue1"
        user_equipment = self.user_equipment_creator.create_user_equipment(frequency, unique_id)

        self.assertIsInstance(user_equipment, UserEquipment)
        self.assertTrue(0 <= user_equipment.x <= self.upper_x_bound)
        self.assertTrue(0 <= user_equipment.y <= self.upper_y_bound)
        self.assertEqual(user_equipment.frequency, frequency)
        self.assertEqual(user_equipment.unique_id, unique_id)

    def test_create_fixed_user_equipment(self):
        x = 500
        y = 500
        frequency = 2.4e9
        unique_id = "ue2"
        user_equipment = self.user_equipment_creator.create_fixed_user_equipment(x, y, frequency, unique_id)

        self.assertIsInstance(user_equipment, UserEquipment)
        self.assertEqual(user_equipment.x, x)
        self.assertEqual(user_equipment.y, y)
        self.assertEqual(user_equipment.frequency, frequency)
        self.assertEqual(user_equipment.unique_id, unique_id)

if __name__ == '__main__':
    unittest.main()
