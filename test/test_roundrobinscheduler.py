import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.roundrobinscheduler import RoundRobinScheduler
from src.userequipment import UserEquipment


class TestRoundRobinScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = RoundRobinScheduler(4)

    def test_schedule_next_slot(self):
        user_equipment1 = UserEquipment(0, 0, 700e6, "ue1")
        user_equipment2 = UserEquipment(0, 0, 700e6, "ue2")
        user_equipment3 = UserEquipment(0, 0, 700e6, "ue3")

        self.scheduler.update_user_equipment_to_be_scheduled_list([user_equipment1, user_equipment2, user_equipment3])
        slot_schedule = self.scheduler.schedule_next_slot()

        self.assertEqual(slot_schedule.getUserInResourceBlock(0), user_equipment1)
        self.assertEqual(slot_schedule.getUserInResourceBlock(1), user_equipment2)
        self.assertEqual(slot_schedule.getUserInResourceBlock(2), user_equipment3)
        self.assertEqual(slot_schedule.getUserInResourceBlock(3), user_equipment1)

    def test_remove_user_equipment_from_current_schedule(self):
        user_equipment1 = UserEquipment(0, 0, 700e6, "ue1")
        user_equipment2 = UserEquipment(0, 0, 700e6, "ue2")
        user_equipment3 = UserEquipment(0, 0, 700e6, "ue3")

        self.scheduler.update_user_equipment_to_be_scheduled_list([user_equipment1, user_equipment2, user_equipment3])

        self.scheduler.remove_user_equipment_from_current_schedule(user_equipment2)

        self.assertEqual(len(self.scheduler.userEquipmentToBeScheduledList), 2)
        self.assertNotIn(user_equipment2, self.scheduler.userEquipmentToBeScheduledList)

        self.assertEqual(len(self.scheduler.resourceBlocksServedPerUserEquipmentList), 2)
        self.assertEqual(self.scheduler.resourceBlocksServedPerUserEquipmentList, [0, 0])

if __name__ == '__main__':
    unittest.main()
