
# This Python script simulates a proportional fair scheduling algorithm with starvation prevention in a telecommunication system's downlink.
#
# The simulation runs for a predefined number of time slots and resource blocks. For each resource block in a slot, the scheduler allocates the resource block to the user with the highest normalized rate, or if any user has been waiting for more than a specified threshold, the one who has been waiting the longest is selected. This is done to prevent starvation.
# The normalized rate is calculated by dividing the instantaneous rate by the exponential weighted moving average (EWMA) of past rates. The script also updates the EWMA of the throughput for each user and the number of slots since each user was last scheduled, then repeats this process for each resource block in each slot.
# At the end of the simulation, the script prints the total bits transmitted in each slot and the aggregate throughput across all slots, providing valuable insights into the scheduler's performance in a telecommunication network context.
#
# Key Components of the Script:
# Constants: Defines several constants used in the simulation like NUMBER_OF_SLOTS, RESOURCE_BLOCKS, NUM_USERS, MIN_RATE, MAX_RATE, EWMA_TIME_CONSTANT, SMALL_CONSTANT, INITIAL_THROUGHPUT, STARVATION_THRESHOLD.
# Initializations: Initializes arrays to track total bits transmitted per slot, aggregate throughput, average throughput (T), and slots since last scheduled for each user.
#
# Simulation Loop: Runs a loop for each slot doing the following:
# a. Generate random link rates between MIN_RATE and MAX_RATE for each user.
# b. Calculate normalized rates for each user.
# c. Determine the user to schedule based on the highest normalized rate or starvation.
# d. Update total bits transmitted in the current slot.
# e. Update EWMA of throughput and number of slots since each user was last scheduled.
#
# Output: Prints user capacities, allocated slots, total bits transmitted in each slot, and the aggregate throughput.
#
# The script helps in analyzing the performance of the proportional fair scheduler in a telecommunication network, taking into account factors like varying user capacities, resource block allocations, and preventing user starvation.

from datetime import datetime
import numpy as np
import time

# Constants:
NUMBER_OF_SLOTS = 10
SLOT_DURATION = 0.5e-3
RESOURCE_BLOCKS = 3
NUM_USERS = 4
MIN_RATE = 10.0e3
MAX_RATE = 100.0e3
EWMA_TIME_CONSTANT = 20.0
SMALL_CONSTANT = 1e-9
INITIAL_THROUGHPUT = 1e-9
STARVATION_THRESHOLD = 3

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

for slot in range(NUMBER_OF_SLOTS):
    # Generate random link rates between MIN_RATE and MAX_RATE for NUM_USERS:
    seed_value = int(current_timestamp + slot)  # Incorporate slot into the seed for unique rates per slot
    np.random.seed(seed_value)
    R = np.random.uniform(MIN_RATE, MAX_RATE, NUM_USERS)

    print(f"User capacities for slot {slot}:")
    for i, rate in enumerate(R, 1):
        print(f"User {i}: {rate:.2f}")

    total_bits_transmitted = 0.0

    for resource_block in range(RESOURCE_BLOCKS):
        # Calculate the user with the highest normalized rate
        norm_rates = R / (T + SMALL_CONSTANT)

        # Check for starvation
        if np.max(slots_since_last_scheduled) >= STARVATION_THRESHOLD:
            user = np.argmax(slots_since_last_scheduled)
        else:
            user = np.argmax(norm_rates)

        # Update the total bits transmitted in this slot
        total_bits_transmitted += R[user] * SLOT_DURATION

        print(f"Slot {slot}, Resource Block {resource_block+1} - user {user+1} rate {R[user]:.2f} bps")

        # Update averages:
        T = (1 - (1 / EWMA_TIME_CONSTANT)) * T
        T[user] += (1 / EWMA_TIME_CONSTANT) * R[user]

        # Update slots since last scheduled
        slots_since_last_scheduled += 1
        slots_since_last_scheduled[user] = 0

    total_bits_per_slot[slot] = total_bits_transmitted
    # aggregate_throughput += total_bits_transmitted
    aggregate_throughput += (total_bits_transmitted / (NUMBER_OF_SLOTS * SLOT_DURATION))

    print(f"Total bits transmitted in slot {slot}: {total_bits_transmitted:.2f} bits")
    print("")

print(f'Aggregate throughput: {aggregate_throughput:.2f} bits')
print("")
end_time = time.time()
end_datetime = datetime.fromtimestamp(end_time)
print(f'Finishing simulation at: {end_datetime}')
print(f'Total execution time: {end_time - start_time:.2f} seconds')
