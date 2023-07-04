import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.userequipment import UserEquipment

class TestUserEquipment(unittest.TestCase):

    def setUp(self):
        self.user_equipment = UserEquipment(1, 2, 700e6, "unique_id_1")

    def test_user_equipment_creation(self):
        ue = self.user_equipment

        self.assertEqual(ue.x, 1)
        self.assertEqual(ue.y, 2)
        self.assertEqual(ue.frequency, 700e6)
        self.assertEqual(ue.unique_id, "unique_id_1")
        self.assertIsNone(ue.connected_bs)
        self.assertIsNone(ue.distance_from_bs)
        self.assertIsNone(ue.link_capacity)
        self.assertIsNone(ue.serving_base_station)

    def test_user_equipment_setters(self):
        ue = self.user_equipment

        ue.connected_bs = "BaseStation_1"
        ue.distance_from_bs = 100
        ue.link_capacity = 1e6
        ue.serving_base_station = "BaseStation_1"

        self.assertEqual(ue.connected_bs, "BaseStation_1")
        self.assertEqual(ue.distance_from_bs, 100)
        self.assertEqual(ue.link_capacity, 1e6)
        self.assertEqual(ue.serving_base_station, "BaseStation_1")

    def test_user_equipment_dissociate_from_base_stations(self):
        ue = self.user_equipment
        ue.serving_base_station = "BaseStation_1"

        ue.dissociate_from_base_stations()

        self.assertIsNone(ue.serving_base_station)

    def test_user_equipment_is_dummy(self):
        ue = self.user_equipment

        ue.x = -1
        ue.y = -1

        self.assertTrue(ue.is_dummy())

        ue.x = 1
        ue.y = 1

        self.assertFalse(ue.is_dummy())

if __name__ == '__main__':
    unittest.main()
