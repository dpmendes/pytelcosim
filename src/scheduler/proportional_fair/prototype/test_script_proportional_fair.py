# The code provided aims to implement a Proportional Fair Scheduler for downlink.
# Overview :

# General overview:
# The scheduler works by adjusting the average
# throughput for each user and then determining which user
# to allocate the slot to based on the ratio of their instantaneous
# rate to their average throughput.

# Code Breakdown:

# TOTAL_SLOTS: This is the total number of time slots for which the simulation will run.
# NUM_USERS: The total number of users in the system.
# T: A list containing the average throughputs of all users. It's initialized with values close to zero.
# R: A list containing the link rates for each user.
# t_C: The EWMA (Exponentially Weighted Moving Average) constant.
# Inside the while loop, for each time slot:
# The normalized rates (instantaneous rate / average throughput) for all users are calculated.
# The user with the maximum normalized rate is then scheduled for this time slot.
# The average throughputs for all users are then updated.

from datetime import datetime
import numpy as np

# Constants:
TOTAL_SLOTS = 10
NUM_USERS = 20
MIN_RATE = 100.0
MAX_RATE = 1200.0
EWMA_TIME_CONSTANT = 20.0
SMALL_CONSTANT = 1e-9
INITIAL_THROUGHPUT = 1e-9
STARVATION_THRESHOLD = 5

# Get the current timestamp
current_timestamp = datetime.now().timestamp()

# Initial values close to zero to avoid division by zero in the first iteration:
T = np.array([INITIAL_THROUGHPUT] * NUM_USERS)
# Initialize slots since last scheduled for each user
slots_since_last_scheduled = np.zeros(NUM_USERS)

# Generate random link rates between MIN_RATE and MAX_RATE for NUM_USERS:
seed_value = int(current_timestamp)
np.random.seed(seed_value)
R = np.random.uniform(MIN_RATE, MAX_RATE, NUM_USERS)

print("")
print("Generated link rates:")
for i, rate in enumerate(R, 1):
    print(f"User {i}: {rate:.2f}")
print("")

for slot in range(TOTAL_SLOTS):
    # Avoid division by zero by adding a small constant
    norm_rates = R / (T + SMALL_CONSTANT)

    # Check for starvation
    if np.max(slots_since_last_scheduled) >= STARVATION_THRESHOLD:
        user = np.argmax(slots_since_last_scheduled)
    else:
        user = np.argmax(norm_rates)

    print(f"Slot {slot} user {user+1} rate {R[user]:.2f} bps")

    # Update averages:
    T = (1 - (1 / EWMA_TIME_CONSTANT)) * T
    T[user] += (1 / EWMA_TIME_CONSTANT) * R[user]

    # Update slots since last scheduled
    slots_since_last_scheduled += 1
    slots_since_last_scheduled[user] = 0
