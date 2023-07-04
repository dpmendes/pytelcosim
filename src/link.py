import math

class Link:

    def __init__(self, source_node, destination_node, channel):
        self.source_node = source_node
        self.destination_node = destination_node
        self.channel = channel
        self.capacity = None
        self.gain = None
        self.active_in_the_current_slot = True

    def calculate_distance(self):
        origin_x, origin_y = self.source_node.get_position()
        destination_x, destination_y = self.destination_node.get_position()

        horizontal_distance = destination_x - origin_x
        vertical_distance = destination_y - origin_y

        distance = math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2)
        return distance

    def calculate_link_gain(self):
        distance = self.calculate_distance()
        self.gain = self.channel.calculate_gain(distance)

    def calculate_link_capacity(self, W=180e3, J=40):
        l = self.calculate_distance()
        N0 = 290 * 1.38064852e-23
        a = 2
        snr = (J/((l**a)*N0*W))
        if snr <= 0:
            self.capacity = 0
        else:
            self.capacity = W * (math.log2(1 + snr))

    def deactivate_link(self):
        self.active_in_the_current_slot = False

    def activate_link(self):
        self.active_in_the_current_slot = True
