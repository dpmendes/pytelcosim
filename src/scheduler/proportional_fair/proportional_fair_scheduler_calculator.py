from link.link_manager import LinkManager
from transceiver.base_station.base_station_manager import BaseStationManager
from transceiver.user_equipment.user_equipment_manager import UserEquipmentManager
from transmission_calc.signal_calculator import SignalCalculator


class ProportionalFairCapacityCalculator:

    def __init__(self,
                 bs_manager: BaseStationManager,
                 ue_manager: UserEquipmentManager,
                 link_manager: LinkManager,
                 number_of_slots: int,
                 resource_blocks_per_slot: int,
                 slot_duration_in_seconds: float):
        self._bs_manager = bs_manager
        self._ue_manager = ue_manager
        self._link_manager = link_manager
        self._number_of_slots = number_of_slots
        self._resource_blocks_per_slot = resource_blocks_per_slot
        self._slot_duration_in_seconds = slot_duration_in_seconds
        self._bits_transmitted_in_resource_block_dict = {}
        self._bits_transmitted_this_slot_list = []
        self._total_bits_transmitted = 0
        self._aggregate_throughput = 0

    def _calculate_signals(self, user_equipment, links_to_user_equipment):
        intended_signal = SignalCalculator.calculate_intended_signal_to_user_equipment(user_equipment, links_to_user_equipment)
        interfering_signal = SignalCalculator.calculate_interfering_signal_at_user_equipment(user_equipment, links_to_user_equipment)
        return intended_signal, interfering_signal

    def _schedule_resource_blocks_for_base_stations(self):
        all_base_stations_schedule = []
        for base_station in self._bs_manager.base_stations:
            slot_schedule = base_station.request_next_schedule_to_scheduler()
            all_base_stations_schedule.append(slot_schedule)
        return all_base_stations_schedule

    def _get_scheduled_users_from_all_schedules(self, all_base_stations_schedule, resource_block):
        return [bs_schedule.get_user_in_resource_block(resource_block) for bs_schedule in all_base_stations_schedule]

    def _update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio(self):
        for user_equipment in self._ue_manager.user_equipments:
            links_to_user_equipment = self._link_manager.find_links_to_user_equipment(user_equipment)
            intended_signal, interfering_signal = self._calculate_signals(user_equipment, links_to_user_equipment)
            user_equipment.update_signal_to_interference_plus_noise_ratio(intended_signal, interfering_signal)

    def _update_all_user_equipment_reception_capacity(self):
        for user_equipment in self._ue_manager.user_equipments:
            user_equipment.calculate_reception_capacity()

    def _calculate_bits_transmitted_in_downlink_resource_block(self, scheduled_users, current_slot):
        bits_transmitted_in_resource_block = 0

        if current_slot not in self._bits_transmitted_in_resource_block_dict:
            self._bits_transmitted_in_resource_block_dict[current_slot] = []

        for user_equipment in scheduled_users:
            user_equipment.receive_resource_block()
            bits_transmitted_per_user_equipment = (
                        user_equipment.current_capacity_in_bits_per_second * self._slot_duration_in_seconds)
            bits_transmitted_in_resource_block += bits_transmitted_per_user_equipment

            transmission_detail = f"{user_equipment.unique_id}, UE ({user_equipment.x:.2f},{user_equipment.y:.2f}), Bits transmitted = {bits_transmitted_per_user_equipment}"
            self._bits_transmitted_in_resource_block_dict[current_slot].append(transmission_detail)

        return bits_transmitted_in_resource_block

    def _calculate_resource_block_transmission(self, all_base_stations_schedule, resource_block, current_slot):
        scheduled_users = self._get_scheduled_users_from_all_schedules(all_base_stations_schedule, resource_block)
        return self._calculate_bits_transmitted_in_downlink_resource_block(scheduled_users, current_slot)

    def _calculate_downlink_proportional_fair_scheduling_slot_transmitted_bits(self, current_slot):
        # Step 1: Update the reception capacities for all user equipment
        self._update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
        self._update_all_user_equipment_reception_capacity()
        # Step 2: Schedule resource blocks for base stations
        bits_transmitted_this_slot = 0
        all_base_stations_schedule = self._schedule_resource_blocks_for_base_stations()
        # Step 3: Continue with the existing logic
        for resource_block in range(self._resource_blocks_per_slot):
            bits_transmitted_in_resource_block = self._calculate_resource_block_transmission(all_base_stations_schedule,
                                                                                             resource_block,
                                                                                             current_slot)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        self._bits_transmitted_this_slot_list.append(bits_transmitted_this_slot)
        return bits_transmitted_this_slot

    def _calculate_slots_transmission(self):
        self._total_bits_transmitted = 0

        for current_slot in range(1, self._number_of_slots + 1):
            bits_transmitted_this_slot = self._calculate_downlink_proportional_fair_scheduling_slot_transmitted_bits(current_slot)
            self._total_bits_transmitted += bits_transmitted_this_slot

    def calculate_downlink_aggregate_throughput_over_number_of_slots(self):
        self._calculate_slots_transmission()
        aggregate_throughput = (self._total_bits_transmitted / (self._number_of_slots * self._slot_duration_in_seconds))
        self._aggregate_throughput = aggregate_throughput
        return self._aggregate_throughput

    @property
    def number_of_slots(self):
        return self._number_of_slots

    @property
    def resource_blocks_per_slot(self):
        return self._resource_blocks_per_slot

    @property
    def bits_transmitted_per_slot(self):
        return self._bits_transmitted_this_slot_list

    @property
    def bits_transmitted_in_resource_block(self):
        return self._bits_transmitted_in_resource_block_dict

    @property
    def total_bits_transmitted(self):
        return self._total_bits_transmitted

    @property
    def aggregate_throughput(self):
        return self._aggregate_throughput
