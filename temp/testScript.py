import time
import datetime
from System import System

system = System()
system.load_test_scenario_1()

print('')
start_time = time.time()
start_datetime = datetime.datetime.fromtimestamp(start_time)
print(f'Starting simulation at: {start_datetime}')

print('')
print('Base Stations:')
print('')

base_stations = system.base_stations_list
for i, base_station in enumerate(base_stations):
    x, y = base_station.get_position()
    print(f'Base Station {i}, ({x}, {y})')

    print('Associated User Equipment')
    user_equipment_list = base_station.get_associated_user_equipment()
    for j, user_equipment in enumerate(user_equipment_list):
        x, y = user_equipment.get_position()
        print(f'User Equipment at ({x}, {y})')
    print('')

print('')
print('User Equipments:')
print('')

user_equipments = system.user_equipment_list
for j, user_equipment in enumerate(user_equipments):
    x, y = user_equipment.get_position()
    print(f'User Equipment {j}, ({x}, {y})')

    serving_base_station = user_equipment.get_serving_base_station()
    x, y = serving_base_station.get_position()
    print(f'Serving Base Station at ({x}, {y})\n\n')


aggregate_throughput = system.calculate_downlink_round_robin_aggregate_throughput_over_number_of_slots(
    20)

print(f'Aggregate throughput = {aggregate_throughput:.2e} bps')

print('')
end_time = time.time()
end_datetime = datetime.datetime.fromtimestamp(end_time)
print(f'Finishing simulation at: {end_datetime}')
print(f'Total execution time: {end_time - start_time:.2f} seconds')
print('')
