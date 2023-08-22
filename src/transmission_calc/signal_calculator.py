class SignalCalculator:

    @staticmethod
    def calculate_intended_signal_to_user_equipment(user_equipment, links_to_user_equipment):
        intended_signal = 0
        for current_link in links_to_user_equipment:
            if current_link._destination_node == user_equipment.connected_base_station:
                base_station = current_link._destination_node
                intended_signal += base_station.transmisson_power * current_link.gain

        # print("Intended signal",{intended_signal})
        return intended_signal

    @staticmethod
    def calculate_interfering_signal_at_user_equipment(user_equipment, links_to_user_equipment):
        interfering_signal = 0
        for current_link in links_to_user_equipment:
            if current_link.source_node != user_equipment.connected_base_station:
                base_station = current_link.source_node
                interfering_signal += base_station.transmisson_power * current_link.gain

        # print("Interfering signal",{interfering_signal})
        return interfering_signal
