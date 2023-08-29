from transceiver.base_station.base_station import BaseStation

class SignalCalculator:

    @staticmethod
    def calculate_intended_signal_to_user_equipment(user_equipment, links_to_user_equipment):
        if not isinstance(user_equipment.connected_base_station, BaseStation):
            raise ValueError("Connected base station is not an instance of BaseStation")

        intended_signal = 0
        for current_link in links_to_user_equipment:
            if current_link.source_node == user_equipment.connected_base_station:
                if isinstance(current_link.source_node, BaseStation):
                    base_station = current_link.source_node
                    intended_signal += base_station.transmisson_power * current_link.gain
                else:
                    raise ValueError("Source node is the same as connected base station")
        return intended_signal

    @staticmethod
    def calculate_interfering_signal_at_user_equipment(user_equipment, links_to_user_equipment):
        if not isinstance(user_equipment.connected_base_station, BaseStation):
            raise ValueError("Connected base station is not an instance of BaseStation")

        interfering_signal = 0
        for current_link in links_to_user_equipment:
            if current_link.source_node != user_equipment.connected_base_station:
                if isinstance(current_link.source_node, BaseStation):
                    base_station = current_link.source_node
                    interfering_signal += base_station.transmisson_power * current_link.gain
                else:
                    raise ValueError("Source node is the same as connected base station")
        return interfering_signal
