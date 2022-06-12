from scipy.interpolate import interp1d
import numpy as np


class Planer():
    def __init__(self, bot):
        self.bot = bot
        self.tasks = []
        self.task_count = 0


class Plan():
    # TODO: Double check whether average_collection_rate_per_s calculations is correct
    def __init__(self, bot):
        self.current_time = 0
        self.average_collection_rate_per_s = 40 / 60
        self.bot = bot
        self.mineral_guess = None
        self.time = np.array([0])
        self.mineral_collection_rate = np.array([0])
        self.mining_workers = sum(
            [w_manager.worker_tags.amount for w_manager in self.bot.w_managers])
        self.working_until = [0 for _ in range(self.bot.townhalls.amount)]
        self.empty_worker_space_total = sum(
            [self.empty_worker_space(w_manager) for w_manager in self.bot.w_managers])
        self.mineral_guess = None
        self.buildings_under_construction = []

    def build_worker(self):
        for index, i in enumerate(self.working_until):
            if i < self.current_time and self.empty_worker_space_total > 0:
                self.working_until[index] += 11  # time to make one SCV
                self.empty_worker_space_total -= 1
                self.mining_workers += 1
                self.update_mineral_rate(
                    self.current_time + 11, self.mining_workers * self.average_collection_rate_per_s)

    def empty_worker_space(w_manager):
        return w_manager.max_mineral_workers - w_manager.worker_tags.amount

    def get_mineral_rate(self, time):
        index_before = 0
        for index, i in enumerate(self.time):
            if i >= time:
                index_before = index-1
                break

        if index_before >= 0:
            return self.mineral_collection_rate[index_before]

    def update_mineral_rate(self, t, m):
        self.time = np.append(self.time, t)
        self.mineral_collection_rate = np.append(
            self.mineral_collection_rate, m)
        # self.mineral_guess = interp1d(self.time, self.mineral_collection_rate, 'linear')

    def update_minerals_collected(self, time):
        x = np.array([50])
        y = np.array([0])
        for i in range(1, int(time)+1):
            x = np.append(x, x[i-1] + self.get_mineral_rate(i))
            y = np.append(y, i)
        self.mineral_guess = interp1d(x, y, 'linear')

    def build_base(self):
        self.buildings_under_construction.append()
