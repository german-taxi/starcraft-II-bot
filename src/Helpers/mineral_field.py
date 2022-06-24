# Class representing a mineral field
class MineralField:
    def __init__(self, bot, tag):
        self._bot = bot
        self.tag = tag
        self._worker_tags = set()
        self.occupation = 0

    def update(self):
        """
        If the worker is idle or gathering, and it's not already gathering from this mineral patch, send it
        to gather from this mineral patch
        """
        workers = self._bot.get_units_by_tag(self._worker_tags)

        for worker in workers:
            if worker.is_gathering or worker.is_idle:
                if not worker.orders or worker.orders[0].target != self.tag:
                    mineral = self._bot.unit_by_tag.get(self.tag)
                    worker.gather(mineral, queue=False)
                    # print("Send worker to gather, reason wrong target/idle")  # Debug

    def add_worker(self, worker_tag):
        """
        > The function `add_worker` takes in a worker tag and adds it to the set of worker tags

        Args:
          worker_tag: the tag of the worker that is being added to the job
        """
        self._worker_tags.add(worker_tag)
        self.occupation += 1

    def remove_worker(self, worker_tag):
        """
        It removes a worker from the queue, and returns True if the worker was in the queue, and False
        otherwise

        Args:
          worker_tag: The tag of the worker that is being removed.

        Returns:
          A boolean value.
        """
        if worker_tag in self._worker_tags:
            self._worker_tags.discard(worker_tag)
            self.occupation -= 1
            return True
        return False

    def get_random_worker_tag(self):
        """
        If there are worker tags available, return one and decrement the occupation count

        Returns:
          A random worker tag is being returned.
        """
        if self._worker_tags:
            self.occupation -= 1
            return self._worker_tags.pop()
        return None
