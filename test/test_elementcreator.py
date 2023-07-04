import unittest
from src.element import Element
from src.elementcreator import ElementCreator


class TestElementCreator(unittest.TestCase):

    def setUp(self):
        self.upper_x_bound = 100
        self.upper_y_bound = 200
        self.element_creator = ElementCreator(
            self.upper_x_bound, self.upper_y_bound)

    def test_create_element(self):
        element = self.element_creator.create_element()
        self.assertIsInstance(element, Element)
        self.assertGreaterEqual(element.x, 0)
        self.assertLessEqual(element.x, self.upper_x_bound)
        self.assertGreaterEqual(element.y, 0)
        self.assertLessEqual(element.y, self.upper_y_bound)
        self.assertIsNone(element.frequency)

        frequency = 700e6
        element_with_frequency = self.element_creator.create_element(frequency)
        self.assertEqual(element_with_frequency.frequency, frequency)

    def test_create_fixed_element(self):
        x = 50
        y = 100
        element = self.element_creator.create_fixed_element(x, y)
        self.assertIsInstance(element, Element)
        self.assertEqual(element.x, x)
        self.assertEqual(element.y, y)
        self.assertIsNone(element.frequency)

        frequency = 800e6
        element_with_frequency = self.element_creator.create_fixed_element(
            x, y, frequency)
        self.assertEqual(element_with_frequency.frequency, frequency)


if __name__ == '__main__':
    unittest.main()
