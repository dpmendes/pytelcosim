class Schedule:
    def __init__(self, number_of_resource_blocks):
        self._base_station = None
        self._users_in_resource_blocks = []
        self._number_of_resource_blocks = number_of_resource_blocks

    def add_user_to_resource_block(self, user_equipment):
        if len(self._users_in_resource_blocks) < self._number_of_resource_blocks:
            self._users_in_resource_blocks.append(user_equipment)

    def get_user_in_resource_block(self, resource_block):
        if 0 <= resource_block < len(self._users_in_resource_blocks):
            return self._users_in_resource_blocks[resource_block]
        else:
            return None

    @property
    def base_station(self):
        return self._base_station

    @base_station.setter
    def base_station(self, base_station):
        self._base_station = base_station
