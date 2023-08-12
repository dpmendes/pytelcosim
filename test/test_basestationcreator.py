import unittest
from transceiver.base_station import BaseStation
from transceiver.base_station.base_station_creator import BaseStationCreator


class TestBaseStationCreator(unittest.TestCase):
    def setUp(self):
        self.base_station_creator = BaseStationCreator(100, 100)

    def test_create_base_station(self):
        frequency = 1000
        unique_id = 1
        base_station = self.base_station_creator.create_base_station(
            frequency, unique_id)

        self.assertIsInstance(base_station, BaseStation)
        self.assertEqual(base_station.frequency, frequency)
        self.assertEqual(base_station.unique_id, unique_id)
        self.assertTrue(0 <= base_station.x <= 100)
        self.assertTrue(0 <= base_station.y <= 100)

    def test_create_fixed_base_station(self):
        x = 50
        y = 50
        frequency = 2000
        unique_id = 2
        base_station = self.base_station_creator.create_fixed_base_station(
            x, y, frequency, unique_id)

        self.assertIsInstance(base_station, BaseStation)
        self.assertEqual(base_station.x, x)
        self.assertEqual(base_station.y, y)
        self.assertEqual(base_station.frequency, frequency)
        self.assertEqual(base_station.unique_id, unique_id)


if __name__ == '__main__':
    unittest.main()
