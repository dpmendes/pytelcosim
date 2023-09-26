from datetime import datetime
import numpy as np
import time

# Constants:
NUMBER_OF_SLOTS = 5
SLOT_DURATION = 0.5e-3
RESOURCE_BLOCKS = 3
NUM_USERS = 4
MIN_CAPACITY = 10.0e3
MAX_CAPACITY = 100.0e3

start_time = time.time()
start_datetime = datetime.fromtimestamp(start_time)
print(f'Starting simulation at: {start_datetime}')
print("")

# Get the current timestamp
current_timestamp = datetime.now().timestamp()

# Initialize arrays to track total bits transmitted per slot and aggregate throughput
total_bits_per_slot = np.zeros(NUMBER_OF_SLOTS)
aggregate_throughput = 0.0

# Initialize the current user
current_user = 0

# Generate random link rates between MIN_CAPACITY and MAX_CAPACITY for NUM_USERS:
seed_value = int(current_timestamp)  # Incorporate slot into the seed for unique rates per slot
np.random.seed(seed_value)
R = np.random.uniform(MIN_CAPACITY, MAX_CAPACITY, NUM_USERS)


for slot in range(NUMBER_OF_SLOTS):
    # Generate random link rates between MIN_CAPACITY and MAX_CAPACITY for NUM_USERS:
    # seed_value = int(current_timestamp + slot)  # Incorporate slot into the seed for unique rates per slot
    # np.random.seed(seed_value)
    # R = np.random.uniform(MIN_CAPACITY, MAX_CAPACITY, NUM_USERS)

    print(f"User capacities for slot {slot}:")
    for i, rate in enumerate(R, 1):
        print(f"User {i}: {rate:.2f}")

    total_bits_transmitted = 0.0

    for resource_block in range(RESOURCE_BLOCKS):
        # Round Robin scheduling
        user = current_user % NUM_USERS

        # Update the total bits transmitted in this slot
        total_bits_transmitted += R[user] * SLOT_DURATION

        print(f"Slot {slot}, Resource Block {resource_block+1} - user {user+1} rate {R[user]:.2f} bps")

        # Update current user
        current_user += 1

    total_bits_per_slot[slot] = total_bits_transmitted
    aggregate_throughput += (total_bits_transmitted / (NUMBER_OF_SLOTS * SLOT_DURATION))

    print(f"Total bits transmitted in slot {slot}: {total_bits_transmitted:.2f} bits")
    print("")

print(f'Aggregate throughput: {aggregate_throughput:.2f} bits')
print("")
end_time = time.time()
end_datetime = datetime.fromtimestamp(end_time)
print(f'Finishing simulation at: {end_datetime}')
print(f'Total execution time: {end_time - start_time:.2f} seconds')
