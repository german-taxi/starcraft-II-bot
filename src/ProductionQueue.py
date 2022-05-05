class ProductionQueue():
    queue = []

    def __init__(self):
        self.queue = []

    def add(self, queue_item):
        self.queue.append(queue_item)

    def remove_from_queue(self, queue_item):
        self.queue.remove(queue_item)

    def remove_first(self):
        return self.queue.pop(0)

    def get_first(self):
        if self.queue:
            return self.queue[0]
        else:
            return None
