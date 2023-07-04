class Monitor:
    def __init__(self):
        self.system = []
        self.ue_list = []
        self.bs_list = []

    def show_user_equipment_received_bits(self):
        for ue in self.ue_list:
            x, y = ue.get_position()
            bits = ue.total_bits_received
            print(f'UE at ({x},{y}) received {bits} bits.')

    def show_user_equipment_transmitted_bits(self):
        for ue in self.ue_list:
            x, y = ue.get_position()
            bits = ue.total_bits_transmitted
            print(f'UE at ({x},{y}) transmitted {bits} bits.')

    def show_base_stations_received_bits(self):
        for bs in self.bs_list:
            x, y = bs.get_position()
            bits = bs.total_bits_received
            print(f'BS at ({x},{y}) received {bits} bits.')

    def show_associated_user_equipment(self):
        for i, bs in enumerate(self.bs_list, 1):
            x, y = bs.get_position()
            associated_ue_list = bs.associated_user_equipment_list
            print(f'\nBS {i} at ({x},{y}).')

            for ue in associated_ue_list:
                x, y = ue.get_position()
                print(f'UE at ({x},{y}) associated.')

    def show_all_base_stations_next_schedule(self):
        all_base_stations_schedule = self.system.schedule_resource_blocks_for_base_stations()

        for i, base_stations in enumerate(self.system.base_stations_list, 1):
            for j, ue in enumerate(base_stations, 1):
                x, y = ue.get_position()
                print(f'UE at ({x},{y}) scheduled in resource block {j}.')

    def show_all_base_stations_user_equipment_times_scheduled(self):
        for i, bs in enumerate(self.bs_list, 1):
            print(f'\nBS {i} UE times served =',
                  bs.user_equipment_times_scheduled)

    def set_monitor_system(self, system):
        self.system = system
        self.initialize_monitor_lists()

    def initialize_monitor_lists(self):
        self.ue_list = self.system.user_equipment_list
        self.bs_list = self.system.base_stations_list
