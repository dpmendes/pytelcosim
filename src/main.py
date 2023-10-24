import datetime
import time

from properties.properties import settings
from system.monitor.monitor import Monitor
from system.system import System
from utils.utils import generate_log_file_name



def main():
    """
    Main function to run the simulation for each scenario defined in the settings.
    Initializes the system, runs the simulation, and logs the details of each scenario.
    """
    try:
        # Extract all scenario names from settings:
        scenario_names = settings["scenarios"].keys()

        start_time = time.time()
        start_datetime = datetime.datetime.fromtimestamp(start_time)
        print(f'Starting simulation at: {start_datetime}')

        for scenario_name in scenario_names:
            print(f"Running simulation for {scenario_name}")

            scenario_start_time = time.time()

            system = System(scenario_name)
            system.simulate_scenario()

            log_file_name = generate_log_file_name(scenario_name, settings, False)
            monitor = Monitor(system, log_file_name, False)

            # Monitor actions:
            monitor.log_scenario_data()

            #monitor.plot_elements()

            scenario_end_time = time.time()
            print(f"Simulation for {scenario_name} completed in {scenario_end_time - scenario_start_time:.2f} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        end_time = time.time()
        end_datetime = datetime.datetime.fromtimestamp(end_time)
        print(f'Finishing simulation at: {end_datetime}')
        print(f'Total execution time: {end_time - start_time:.2f} seconds')

if __name__ == '__main__':
    main()
