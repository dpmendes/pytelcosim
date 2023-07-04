import unittest
from src.roundrobinscheduler import RoundRobinScheduler
from src.userequipment import UserEquipment

class TestRoundRobinScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = RoundRobinScheduler(number_of_resource_blocks_per_slot=4)
        self.user_equipment_list = [
            UserEquipment(0, 0, 800, "ue1"),
            UserEquipment(1, 1, 800, "ue2"),
            UserEquipment(2, 2, 800, "ue3"),
            UserEquipment(3, 3, 800, "ue4")
        ]
        self.scheduler.update_user_equipment_to_be_scheduled_list(self.user_equipment_list)

    def test_schedule_next_slot(self):
        slot_schedule = self.scheduler.schedule_next_slot()
        scheduled_user_equipment = slot_schedule.get_scheduled_user_equipment()

        print("Scheduled User Equipment:")
        for ue in scheduled_user_equipment:
            print(ue)

        print("\nExpected User Equipment:")
        for ue in self.user_equipment_list:
            print(ue)

        self.assertEqual(scheduled_user_equipment, self.user_equipment_list, "Round Robin scheduling failed")

if __name__ == '__main__':
    unittest.main()
