from scipy.interpolate import interp1d
import numpy as np


# It's a class that stores a list of tasks and a task count.
class Planer():
    def __init__(self, bot):
        self.bot = bot
        self.tasks = []
        self.task_count = 0


# TODO: Double check whether average_collection_rate_per_s calculations is correct
# The Plan class is a class that keeps track of the current time, the average collection rate per
# second, the bot, the mineral guess, the time, the mineral collection rate, the mining workers, the
# working until, the empty worker space total, and the buildings under construction.
class Plan():
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
        """
        If there are empty worker spaces and a worker is done building, then add a worker to the empty
        worker space and update the mining rate
        """
        for index, i in enumerate(self.working_until):
            if i < self.current_time and self.empty_worker_space_total > 0:
                self.working_until[index] += 11  # time to make one SCV
                self.empty_worker_space_total -= 1
                self.mining_workers += 1
                self.update_mineral_rate(
                    self.current_time + 11, self.mining_workers * self.average_collection_rate_per_s)

    def empty_worker_space(w_manager):
        """
        > This function returns the number of workers that can be assigned to mine minerals

        Args:
          w_manager: The worker manager object.

        Returns:
          The number of workers that can be assigned to mine minerals.
        """
        return w_manager.max_mineral_workers - w_manager.worker_tags.amount

    def get_mineral_rate(self, time):
        """
        > If the time is before the first time in the list, return the first mineral collection rate.
        Otherwise, return the mineral collection rate of the time before the given time

        Args:
          time: The time at which you want to know the mineral collection rate.

        Returns:
          The mineral collection rate at the time before the time given.
        """
        index_before = 0
        for index, i in enumerate(self.time):
            if i >= time:
                index_before = index-1
                break

        if index_before >= 0:
            return self.mineral_collection_rate[index_before]

    def update_mineral_rate(self, t, m):
        """
        `update_mineral_rate` takes in a time and a mineral collection rate, and appends them to the `time`
        and `mineral_collection_rate` arrays

        Args:
          t: time
          m: mineral collection rate
        """
        self.time = np.append(self.time, t)
        self.mineral_collection_rate = np.append(
            self.mineral_collection_rate, m)
        # self.mineral_guess = interp1d(self.time, self.mineral_collection_rate, 'linear')

    def update_minerals_collected(self, time):
        """
        It takes the time at which you want to know the number of minerals collected, and returns the number
        of minerals collected at that time

        Args:
          time: the time in seconds that you want to know the mineral rate for
        """
        x = np.array([50])
        y = np.array([0])
        for i in range(1, int(time)+1):
            x = np.append(x, x[i-1] + self.get_mineral_rate(i))
            y = np.append(y, i)
        self.mineral_guess = interp1d(x, y, 'linear')

    def build_base(self):
        """
        `build_base` adds a building to the list of buildings under construction
        """
        self.buildings_under_construction.append()
