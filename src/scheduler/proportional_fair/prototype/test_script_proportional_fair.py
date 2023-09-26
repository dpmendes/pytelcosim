
from datetime import datetime
import numpy as np
import time

# Constants:
INITIAL_THROUGHPUT = 1e-9
SMALL_CONSTANT = 1e-9

NUMBER_OF_SLOTS = 10
SLOT_DURATION = 0.5e-3
RESOURCE_BLOCKS = 3
NUM_USERS = 4
MIN_CAPACITY = 10.0e3
MAX_CAPACITY = 100.0e3
EWMA_TIME_CONSTANT = 20.0 # EWMA time constant for throughput averaging.Affects how fast the EWMA adapts to new rate changes
STARVATION_THRESHOLD = 3

DEBUG_FLAG = False # Enable this flag for debugging; it will print internal variables for inspection
DYNAMIC_RATES = False # This flag controls whether the rates for users change dynamically during the simulation
RESET_T_FLAG = True
STARVATION_FLAG = False

start_time = time.time()
start_datetime = datetime.fromtimestamp(start_time)
print(f'Starting simulation at: {start_datetime}')
print("")

# Get the current timestamp
current_timestamp = datetime.now().timestamp()

# Initial values close to zero to avoid division by zero in the first iteration:
T = np.array([INITIAL_THROUGHPUT] * NUM_USERS)
# Initialize slots since last scheduled for each user
slots_since_last_scheduled = np.zeros(NUM_USERS)

# Initialize arrays to track total bits transmitted per slot and aggregate throughput
total_bits_per_slot = np.zeros(NUMBER_OF_SLOTS)
aggregate_throughput = 0.0

# Generate random link rates between MIN_CAPACITY and MAX_CAPACITY for NUM_USERS:
if not DYNAMIC_RATES:
    seed_value = int(current_timestamp)  # Incorporate slot into the seed for unique rates per slot
    np.random.seed(seed_value)
    R = np.random.uniform(MIN_CAPACITY, MAX_CAPACITY, NUM_USERS)

for slot in range(NUMBER_OF_SLOTS):

    if DYNAMIC_RATES:
        seed_value = int(current_timestamp + slot)
        np.random.seed(seed_value)
        R = np.random.uniform(MIN_CAPACITY, MAX_CAPACITY, NUM_USERS)

    print(f"User capacities for slot {slot+1}:")
    print(f"User capacities for slot {slot+1}:")
    for i, rate in enumerate(R, 1):
        print(f"User {i}: {rate:.2f}")

    total_bits_transmitted = 0.0

    if DEBUG_FLAG:
        print(f"")
        print(f"Current Rates: {R}")
        print(f"Current Throughput Averages: {T}")

    for resource_block in range(RESOURCE_BLOCKS):


        # Calculate the user with the highest normalized rate
        norm_rates = R / (T + SMALL_CONSTANT)

        if STARVATION_FLAG:
            if np.max(slots_since_last_scheduled) >= STARVATION_THRESHOLD:
                user = np.argmax(slots_since_last_scheduled)
            else:
                user = np.argmax(norm_rates)
        else:
            user = np.argmax(norm_rates)

        scheduled_rate = R[user]

        if DEBUG_FLAG:
            print(f"Normalized Rates: {norm_rates}")
            print(f"Scheduled Rates: {scheduled_rate}")
            print(f"")

        # Update the total bits transmitted in this slot
        total_bits_transmitted += scheduled_rate * SLOT_DURATION
        print(f"Slot {slot+1}, Resource Block {resource_block+1} - user {user+1} rate {scheduled_rate:.2f} bps")

        # Update averages:
        # T = (1 - (1 / EWMA_TIME_CONSTANT)) * T
        # T[user] += (1 / EWMA_TIME_CONSTANT) * scheduled_rate
        T[user] = (0.9 * T[user]) + (0.1 * scheduled_rate)

        if STARVATION_FLAG:
            # Update slots since last scheduled
            slots_since_last_scheduled += 1
            slots_since_last_scheduled[user] = 0
        else:
            pass

    if RESET_T_FLAG:
        T = np.array([INITIAL_THROUGHPUT] * NUM_USERS)

    total_bits_per_slot[slot] = total_bits_transmitted
    aggregate_throughput += total_bits_transmitted / SLOT_DURATION

    print(f"Total bits transmitted in slot {slot+1}: {total_bits_transmitted:.2f} bits")
    print(f"Total bits transmitted in slot {slot+1}: {total_bits_transmitted:.2f} bits")
    print("")

aggregate_throughput /= NUMBER_OF_SLOTS
print(f'Aggregate throughput: {aggregate_throughput:.2f} bits')
print("")
end_time = time.time()
end_datetime = datetime.fromtimestamp(end_time)
print(f'Finishing simulation at: {end_datetime}')
print(f'Total execution time: {end_time - start_time:.2f} seconds')
