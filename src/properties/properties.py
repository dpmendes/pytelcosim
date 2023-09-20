settings = {
    "scenarios": {
        "scenario_1": {
            # General Settings:
            "bandwidth": 180e3,
            "frequency": 2600e6,
            "slot_duration_in_seconds": 0.5e-3,
            "number_of_slots": 5,
            "resource_blocks_per_slot": 3,
            "tx_power": 40,

            # Proportional Fair:
            "ewma_time_constant": 20,
            "starvation_threshold": 5,

            "base_stations": [
                {"mode": "FIXED", "x": 31, "y": 9}
            ],
            "user_equipments": [
                {"mode": "FIXED", "x": 0, "y": 0, "number_of_ues": 1,"user_id": 'User-1'},
                {"mode": "FIXED", "x": 20, "y": 0, "number_of_ues": 1,"user_id": 'User-2'},
                {"mode": "FIXED", "x": 40, "y": 0, "number_of_ues": 1,"user_id": 'User-3'},
                {"mode": "FIXED", "x": 60, "y": 0, "number_of_ues": 1,"user_id": 'User-4'}
            ],
            "capacity_calculator": "RoundRobinCapacityCalculator"
        },
        "scenario_2": {
            # General Settings:
            "bandwidth": 180e3,
            "frequency": 2600e6,
            "slot_duration_in_seconds": 0.5e-3,
            "number_of_slots": 5,
            "resource_blocks_per_slot": 3,
            "tx_power": 40,

            # Proportional Fair:
            "ewma_time_constant": 20,
            "starvation_threshold": 5,

            "base_stations": [
                {"mode": "FIXED", "x": 31, "y": 9}
            ],
            "user_equipments": [
                {"mode": "FIXED", "x": 0, "y": 0, "number_of_ues": 1,"user_id": 'User-1'},
                {"mode": "FIXED", "x": 20, "y": 0, "number_of_ues": 1,"user_id": 'User-2'},
                {"mode": "FIXED", "x": 40, "y": 0, "number_of_ues": 1,"user_id": 'User-3'},
                {"mode": "FIXED", "x": 60, "y": 0, "number_of_ues": 1,"user_id": 'User-4'}
            ],
            "capacity_calculator": "ProportionalFairCapacityCalculator"
        }
    }
}
