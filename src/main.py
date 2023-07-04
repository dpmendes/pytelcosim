import datetime
import os
import time
from src.monitor import Monitor
from src.system import System


def create_log_directory(log_directory='./logs'):
    """Function to create a log directory if it doesn't exist and return the log file path."""
    os.makedirs(log_directory, exist_ok=True)
    return os.path.join(log_directory, 'system_log.txt')

def main():

    start_time = time.time()
    start_datetime = datetime.datetime.fromtimestamp(start_time)
    print(f'Starting simulation at: {start_datetime}')

    system = System()
    system.simulate_scenario_1()

    #// Create log directory and get log file path.
    log_file_path = create_log_directory()
    log_name = "SystemMonitor"

    #// Create a Monitor object with the system, log_name, and log file path.
    monitor = Monitor(system, log_name, log_file_path)

    #// Monitor actions.
    monitor.print_base_stations()
    monitor.print_connected_ues()
    monitor.plot_elements()

    end_time = time.time()
    end_datetime = datetime.datetime.fromtimestamp(end_time)
    print(f'Finishing simulation at: {end_datetime}')
    print(f' Total execution time: {end_time - start_time:.2f} seconds')

if __name__ == '__main__':
    main()


# import time
# import datetime
# from System import System

# system = System()
# system.load_test_scenario_1()

# print('')
# start_time = time.time()
# start_datetime = datetime.datetime.fromtimestamp(start_time)
# print(f'Starting simulation at: {start_datetime}')

# print('')
# print('Base Stations:')
# print('')

# base_stations = system.base_stations_list
# for i, base_station in enumerate(base_stations):
#     x, y = base_station.get_position()
#     print(f'Base Station {i}, ({x}, {y})')

#     print('Associated User Equipment')
#     user_equipment_list = base_station.get_associated_user_equipment()
#     for j, user_equipment in enumerate(user_equipment_list):
#         x, y = user_equipment.get_position()
#         print(f'User Equipment at ({x}, {y})')
#     print('')

# print('')
# print('User Equipments:')
# print('')

# user_equipments = system.user_equipment_list
# for j, user_equipment in enumerate(user_equipments):
#     x, y = user_equipment.get_position()
#     print(f'User Equipment {j}, ({x}, {y})')

#     serving_base_station = user_equipment.get_serving_base_station()
#     x, y = serving_base_station.get_position()
#     print(f'Serving Base Station at ({x}, {y})\n\n')


# aggregate_throughput = system.calculate_downlink_round_robin_aggregate_throughput_over_number_of_slots(
#     20)

# print(f'Aggregate throughput = {aggregate_throughput:.2e} bps')

# print('')
# end_time = time.time()
# end_datetime = datetime.datetime.fromtimestamp(end_time)
# print(f'Finishing simulation at: {end_datetime}')
# print(f'Total execution time: {end_time - start_time:.2f} seconds')
# print('')