import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transceiver.user_equipment.user_equipment import UserEquipment
from scheduler.base.schedule import Schedule

class TestSchedule(unittest.TestCase):

    def setUp(self):
        self.numberOfResourceBlocks = 3
        self.schedule = Schedule(self.numberOfResourceBlocks)

    def test_addUserToResourceBlock(self):
        ue1 = UserEquipment(1, 1, None, 1)
        ue2 = UserEquipment(2, 2, None, 2)
        ue3 = UserEquipment(3, 3, None, 3)
        ue4 = UserEquipment(4, 4, None, 4)

        self.schedule.addUserToResourceBlock(ue1)
        self.schedule.addUserToResourceBlock(ue2)
        self.schedule.addUserToResourceBlock(ue3)
        self.schedule.addUserToResourceBlock(ue4)

        self.assertEqual(len(self.schedule.usersInResourceBlocks), self.numberOfResourceBlocks)
        self.assertEqual(self.schedule.usersInResourceBlocks, [ue1, ue2, ue3])

    def test_shiftUsersInResourceBlocksToTheRight(self):
        ue1 = UserEquipment(1, 1, None, 1)
        ue2 = UserEquipment(2, 2, None, 2)

        self.schedule.addUserToResourceBlock(ue1)
        self.schedule.addUserToResourceBlock(ue2)

        self.schedule.shiftUsersInResourceBlocksToTheRight()

        self.assertEqual(len(self.schedule.usersInResourceBlocks), self.numberOfResourceBlocks)
        self.assertIsInstance(self.schedule.usersInResourceBlocks[0], UserEquipment)
        self.assertEqual(self.schedule.usersInResourceBlocks[1], ue1)
        self.assertEqual(self.schedule.usersInResourceBlocks[2], ue2)

    def test_getUserInResourceBlock(self):
        ue1 = UserEquipment(1, 1, None, 1)
        ue2 = UserEquipment(2, 2, None, 2)

        self.schedule.addUserToResourceBlock(ue1)
        self.schedule.addUserToResourceBlock(ue2)

        self.assertEqual(self.schedule.getUserInResourceBlock(0), ue1)
        self.assertEqual(self.schedule.getUserInResourceBlock(1), ue2)

    def test_set_and_get_base_station(self):
        base_station = "dummy_base_station"

        self.schedule.setBaseStation(base_station)
        self.assertEqual(self.schedule.getBaseStation(), base_station)

if __name__ == '__main__':
    unittest.main()
