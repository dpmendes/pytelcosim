from datetime import datetime
import numpy as np

# Constants:
TOTAL_SLOTS = 20
NUM_USERS = 4
MIN_RATE = 100.0
MAX_RATE = 1200.0
EWMA_CONSTANT = 20.0
SMALL_CONSTANT = 1e-9

class ProportionalFairScheduler:
    def __init__(self, num_users, min_rate, max_rate, ewma_constant):
        self.num_users = num_users
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.ewma_constant = ewma_constant
        self.average_throughputs = np.array([SMALL_CONSTANT] * num_users)
        self.link_rates = self._generate_link_rates()

    def _generate_link_rates(self):
        current_timestamp = datetime.now().timestamp()
        seed_value = int(current_timestamp)
        np.random.seed(seed_value)
        return np.random.uniform(self.min_rate, self.max_rate, self.num_users)

    def run_simulation(self, total_slots):
        for slot in range(total_slots):
            norm_rates = self.link_rates / (self.average_throughputs + SMALL_CONSTANT)
            user = np.argmax(norm_rates)
            print(f"Slot {slot} user {user+1} rate {self.link_rates[user]:.2f}")

            self.average_throughputs = (1 - (1 / self.ewma_constant)) * self.average_throughputs
            self.average_throughputs[user] += (1 / self.ewma_constant) * self.link_rates[user]

if __name__ == "__main__":
    scheduler = ProportionalFairScheduler(NUM_USERS, MIN_RATE, MAX_RATE, EWMA_CONSTANT)
    scheduler.run_simulation(TOTAL_SLOTS)
