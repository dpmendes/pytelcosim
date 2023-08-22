import unittest
from transceiver.base_station import BaseStation
from transceiver.user_equipment.user_equipment import UserEquipment

class TestBaseStation(unittest.TestCase):

    def setUp(self):
        self.base_station = BaseStation(0, 0, 2000e6, 1)

    def test_add_connected_user_equipment(self):
        user_equipment = UserEquipment(1, 1, 2000e6, 1)
        self.base_station.add_connected_user_equipment(user_equipment)
        self.assertIn(user_equipment, self.base_station.connected_ues)

    def test_remove_connected_user_equipment(self):
        user_equipment = UserEquipment(1, 1, 2000e6, 1)
        self.base_station.add_connected_user_equipment(user_equipment)
        self.base_station.remove_connected_user_equipment(user_equipment)
        self.assertNotIn(user_equipment, self.base_station.connected_ues)

    def test_clear_connected_ues(self):
        user_equipment1 = UserEquipment(1, 1, 2000e6, 1)
        user_equipment2 = UserEquipment(2, 2, 2000e6, 2)
        self.base_station.add_connected_user_equipment(user_equipment1)
        self.base_station.add_connected_user_equipment(user_equipment2)
        self.base_station.clear_connected_ues()
        self.assertEqual(len(self.base_station.connected_ues), 0)

    # Add more test methods for other BaseStation class
