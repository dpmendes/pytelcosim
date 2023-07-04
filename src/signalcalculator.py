from src.basestation import BaseStation
from src.userequipment import UserEquipment


class SignalCalculator:

    @staticmethod
    def calculate_intended_signal_to_user_equipment(user_equipment, links_to_user_equipment):
        intended_signal = 0
        for current_link in links_to_user_equipment:
            if current_link.base_station == user_equipment.serving_base_station:
                base_station = current_link.base_station
                intended_signal += base_station.get_transmit_power_in_watts() * current_link.gain
        return intended_signal

    @staticmethod
    def calculate_interfering_signal_at_user_equipment(base_stations, user_equipment, links_to_user_equipment):
        interfering_signal = 0
        for current_link in links_to_user_equipment:
            if current_link.base_station != user_equipment.serving_base_station:
                base_station = current_link.base_station
                interfering_signal += base_station.get_transmit_power_in_watts() * \
                    current_link.gain
        return interfering_signal

    @classmethod
    def calculate_aggregate_capacity(cls, user_equipment_manager):
        user_equipment_manager.update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio()
        user_equipment_manager.update_all_user_equipment_reception_capacity()

        # Assuming that user_equipment_manager has a method `get_aggregate_capacity`
        aggregate_capacity = user_equipment_manager.get_aggregate_capacity()

        return aggregate_capacity


    @classmethod
    def calculate_downlink_round_robin_aggregate_throughput_over_number_of_slots(cls, slot_duration_in_seconds, number_of_slots, calculate_transmitted_bits_method):
        current_slot = 1
        total_bits_transmitted = 0

        while current_slot <= number_of_slots:
            bits_transmitted_this_slot = calculate_transmitted_bits_method()
            total_bits_transmitted += bits_transmitted_this_slot
            current_slot += 1

            if current_slot % 10 == 0:
                print(f'Current Slot = {current_slot}')

        aggregate_throughput = total_bits_transmitted / \
            (number_of_slots * slot_duration_in_seconds)
        return aggregate_throughput

    @classmethod
    def calculate_downlink_round_robin_scheduling_slot_transmitted_bits(cls, resource_blocks_per_slot, schedule_resource_blocks_for_base_stations_method, update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio_method, update_all_user_equipment_reception_capacity_method, calculate_bits_transmitted_in_downlink_resource_block_method):
        bits_transmitted_this_slot = 0
        all_base_stations_schedule = schedule_resource_blocks_for_base_stations_method()

        for resource_block in range(resource_blocks_per_slot):
            scheduled_users = cls.get_scheduled_users_from_all_schedules(
                all_base_stations_schedule, resource_block)
            update_all_user_equipment_rx_signal_to_interference_plus_noise_ratio_method()
            update_all_user_equipment_reception_capacity_method()
            bits_transmitted_in_resource_block = calculate_bits_transmitted_in_downlink_resource_block_method(
                scheduled_users)
            bits_transmitted_this_slot += bits_transmitted_in_resource_block

        return bits_transmitted_this_slot

    @classmethod
    def calculate_bits_transmitted_in_downlink_resource_block(cls, scheduled_users, slot_duration_in_seconds):
        bits_transmitted_in_resource_block = 0

        for user_equipment in scheduled_users:
            user_equipment.receive_resource_block()
            bits_transmitted_per_user_equipment = (
                user_equipment.current_capacity_in_bits_per_second
                * slot_duration_in_seconds
            )

            bits_transmitted_in_resource_block += bits_transmitted_per_user_equipment

        return bits_transmitted_in_resource_block
