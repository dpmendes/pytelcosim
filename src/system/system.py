from channel.free_space_channel import FreeSpaceChannel
from link.link_manager import LinkManager
from properties.properties import settings
from scheduler.round_robin.round_robin_capacity_calculator import RoundRobinCapacityCalculator
from scheduler.proportional_fair.proportional_fair_scheduler_calculator import ProportionalFairCapacityCalculator
from transceiver.base_station.base_station_manager import BaseStationManager
from transceiver.user_equipment.user_equipment_manager import UserEquipmentManager


class System:
    def __init__(self, scenario_name):

        # Check if the scenario name exists in settings
        if scenario_name not in settings["scenarios"]:
            raise ValueError(
                f"Scenario '{scenario_name}' not found in settings.")
        # Extract scenario specific settings:
        self._scenario_config = settings["scenarios"][scenario_name]
        self._scenario_name = scenario_name
        self._bandwidth = self._scenario_config['bandwidth']
        self._frequency = self._scenario_config['frequency']
        self._slot_duration_in_seconds = self._scenario_config['slot_duration_in_seconds']
        self._number_of_slots = self._scenario_config['number_of_slots']
        self._resource_blocks_per_slot = self._scenario_config['resource_blocks_per_slot']
        self._tx_power = self._scenario_config['tx_power']
        self._ewma_time_constant = self._scenario_config['ewma_time_constant']
        self._starvation_threshold = self._scenario_config['starvation_threshold']
        self._aggregate_throughput= 0
        self._base_station_manager = BaseStationManager(
            self._slot_duration_in_seconds, self._resource_blocks_per_slot)
        self._user_equipment_manager = UserEquipmentManager(
            self._slot_duration_in_seconds, self._resource_blocks_per_slot)
        self._capacity = None

    @property
    def base_stations(self):
        return self._base_station_manager.base_stations

    @property
    def user_equipments(self):
        return self._user_equipment_manager.user_equipments

    @property
    def base_station_to_user_equipment_links(self):
        return self._link_manager.base_station_to_user_equipment_links

    @property
    def user_equipment_to_base_station_links(self):
        return self._link_manager.user_equipment_to_base_station_links

    @property
    def capacity(self):
        return self._capacity

    @property
    def throughput(self):
        return self._aggregate_throughput

    @property
    def scenario_name(self):
        return self._scenario_name

    @property
    def scenario_config(self):
        return self._scenario_config

    def _setup_base_stations(self, base_stations_config):
        for bs in base_stations_config:
            self._base_station_manager.create_base_station(
                bs["mode"], bs["x"], bs["y"], self._frequency, self._bandwidth, self._tx_power)

    def _setup_user_equipments(self, user_equipments_config):
        if isinstance(user_equipments_config, list):
            for ue in user_equipments_config:
                self._user_equipment_manager.create_user_equipments(ue["mode"],
                                                                    ue["x"],
                                                                    ue["y"],
                                                                    ue["number_of_ues"],
                                                                    self._frequency,
                                                                    self._bandwidth,
                                                                    self._tx_power,
                                                                    ue["user_id"])
        elif isinstance(user_equipments_config, dict):
            self._user_equipment_manager.create_user_equipments(user_equipments_config["mode"],
                                                                user_equipments_config["upper_x_bound"],
                                                                user_equipments_config["upper_y_bound"],
                                                                user_equipments_config["number_of_ues"],
                                                                self._frequency,
                                                                self._bandwidth,
                                                                self._tx_power)
        else:
            raise ValueError("Invalid user equipment configuration")

    def _initialize_capacity_calculator(self, calculator_type):
        if calculator_type == "RoundRobinCapacityCalculator":
            self._base_station_manager.initialize_base_station_round_robin_schedulers()
            return RoundRobinCapacityCalculator(
                self._base_station_manager,
                self._user_equipment_manager,
                self._link_manager,
                self._number_of_slots,
                self._resource_blocks_per_slot,
                self._slot_duration_in_seconds
            )
        elif calculator_type == "ProportionalFairCapacityCalculator":
            self._base_station_manager.initialize_base_station_proportional_fair_schedulers(
                self._ewma_time_constant, self._starvation_threshold)
            return ProportionalFairCapacityCalculator(
                self._base_station_manager,
                self._user_equipment_manager,
                self._link_manager,
                self._number_of_slots,
                self._resource_blocks_per_slot,
                self._slot_duration_in_seconds
            )
        else:
            raise ValueError(
                f"Unknown capacity calculator type '{calculator_type}'")

    def _configure_basics(self):

        self._channel = FreeSpaceChannel(self._frequency)

        self._base_station_manager.set_all_base_stations_transmit_power_in_watts(self._tx_power)
        self._user_equipment_manager.update_all_user_equipment_slot_duration(self._slot_duration_in_seconds)

        self._link_manager = LinkManager(self._base_station_manager.base_stations, self._user_equipment_manager.user_equipments, self._channel)
        self._link_manager.update_links()
        self._link_manager.associate_all_user_equipment()

        self._base_station_manager.initialize_base_station_associated_user_equipment_scheduled_counters()

    def simulate_scenario(self):
        if self._scenario_name not in settings["scenarios"]:
            raise ValueError(
                f"Scenario '{self._scenario_name}' not found in settings.")

        self._scenario_config = settings["scenarios"][self._scenario_name]

        self._setup_base_stations(self._scenario_config["base_stations"])
        self._setup_user_equipments(self._scenario_config["user_equipments"])
        self._configure_basics()

        self._capacity = self._initialize_capacity_calculator(self._scenario_config["capacity_calculator"])
        self._aggregate_throughput= self._capacity.calculate_downlink_aggregate_throughput_over_number_of_slots()
