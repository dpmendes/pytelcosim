from Transceiver import Transceiver


class UserEquipment(Transceiver):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.serving_base_station = None

    def associate_to_base_station(self, base_station):
        self.serving_base_station = base_station

    def dissociate_from_base_stations(self):
        self.serving_base_station = None

    def get_serving_base_station(self):
        return self.serving_base_station

    def is_dummy(self):
        x, y = self.get_position()
        return x < 0 and y < 0
