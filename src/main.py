import datetime
import time

from system.monitor.monitor import Monitor
from system.system import System
from properties.properties import settings

def main():

    # Extract all scenario names from settings:
    scenario_names = settings["scenarios"].keys()

    start_time = time.time()
    start_datetime = datetime.datetime.fromtimestamp(start_time)
    print(f'Starting simulation at: {start_datetime}')

    for scenario_name in scenario_names:
        print(f"Running simulation for {scenario_name}")

        system = System(scenario_name)
        system.simulate_scenario()

        log_file_name = f"log_{scenario_name}"
        monitor = Monitor(system, log_file_name, True)

        # Monitor actions:
        monitor.log_scenario_name()
        monitor.log_general_settings()
        monitor.log_base_stations()
        monitor.log_user_equipments()
        monitor.log_connected_ues()
        monitor.log_all_downlink_links()
        monitor.log_capacity()
        monitor.log_aggregate_throughput()
        # monitor.plot_elements()

    end_time = time.time()
    end_datetime = datetime.datetime.fromtimestamp(end_time)
    print(f'Finishing simulation at: {end_datetime}')
    print(f'Total execution time: {end_time - start_time:.2f} seconds')

if __name__ == '__main__':
    main()