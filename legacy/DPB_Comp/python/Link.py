import math

class Link:
    def __init__(self, channel):
        self.base_station = None
        self.user_equipment = None
        self.channel = channel
        self.gain = None
        self.active_in_the_current_slot = True

    def calculate_link_gain(self):
        distance = self.calculate_distance()
        link_channel = self.channel
        self.gain = link_channel.calculate_gain(distance)

    def deactivate_link(self):
        self.active_in_the_current_slot = False

    def activate_link(self):
        self.active_in_the_current_slot = True

    def calculate_distance(self):
        origin_x, origin_y = self.base_station.get_position()
        destination_x, destination_y = self.user_equipment.get_position()

        horizontal_distance = destination_x - origin_x
        vertical_distance = destination_y - origin_y

        distance = math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2)
        return distance

