from UserEquipment import UserEquipment


class Schedule:
    def __init__(self, number_of_resource_blocks):
        self.base_station = None
        self.users_in_resource_blocks = []
        self.number_of_resource_blocks = number_of_resource_blocks

    def add_user_to_resource_block(self, user_equipment):
        if len(self.users_in_resource_blocks) < self.number_of_resource_blocks:
            self.users_in_resource_blocks.append(user_equipment)

    def shift_users_in_resource_blocks_to_the_right(self):
        dummy_user = UserEquipment(-1, -1)
        self.users_in_resource_blocks.insert(0, dummy_user)

    def get_user_in_resource_block(self, resource_block):

        if 0 <= resource_block < len(self.users_in_resource_blocks):
            return self.users_in_resource_blocks[resource_block]
        else:
            raise IndexError(
                f"Resource block index {resource_block} is out of range")

    def set_base_station(self, base_station):
        self.base_station = base_station

    def get_base_station(self):
        return self.base_station
