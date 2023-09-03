import datetime
import time

from system.monitor.monitor import Monitor
from system.system import System

def main():
    start_time = time.time()
    start_datetime = datetime.datetime.fromtimestamp(start_time)
    print(f'Starting simulation at: {start_datetime}')

    system = System()
    #system.simulate_scenario_1()
    system.simulate_scenario_2()

    monitor = Monitor(system, "log", True)

    #// Monitor actions.
    monitor.log_base_stations()
    monitor.log_user_equipments()
    monitor.log_connected_ues()
    monitor.log_all_downlink_links()
    monitor.log_capacity()
    # monitor.plot_elements()

    end_time = time.time()
    end_datetime = datetime.datetime.fromtimestamp(end_time)
    print(f'Finishing simulation at: {end_datetime}')
    print(f'Total execution time: {end_time - start_time:.2f} seconds')

if __name__ == '__main__':
    main()
