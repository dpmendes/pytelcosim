import math
from userequipment import UserEquipment

class Link:

    def __init__(self, source_node, destination_node, channel):
        self._source_node = source_node
        self._destination_node = destination_node
        self._capacity = None
        self._gain = None
        self.active_in_the_current_slot = True
        self.channel = channel

    def calculate_distance(self):
        origin_x, origin_y = self._source_node.x, self._source_node.y
        destination_x, destination_y = self._destination_node.x , self._destination_node.y

        horizontal_distance = destination_x - origin_x
        vertical_distance = destination_y - origin_y

        distance = math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2)

        if isinstance(self._source_node, UserEquipment):
            self._source_node.distance_from_bs = distance
        if isinstance(self._destination_node, UserEquipment):
            self._destination_node.distance_from_bs = distance

        return distance

    def calculate_link_gain(self):
        distance = self.calculate_distance()
        self._gain = self.channel.calculate_gain(distance)

    def calculate_link_capacity(self, W=180e3, J=40):
        l = self.calculate_distance()
        N0 = 290 * 1.38064852e-23
        a = 2
        snr = (J/((l**a)*N0*W))
        if snr <= 0:
            self._capacity = 0
        else:
            self._capacity = W * (math.log2(1 + snr))

    def deactivate_link(self):
        self.active_in_the_current_slot = False

    def activate_link(self):
        self.active_in_the_current_slot = True

    @property
    def source_node(self):
        return self._source_node

    @property
    def destination_node(self):
        return self._destination_node

    @property
    def capacity(self):
        return self._capacity

    @property
    def gain(self):
        return self._gain
