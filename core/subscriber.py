class Subscriber:
    def __init__(self, subscriber_id, handler, mode="new", last_n=None, batch_size=1, deliver_immediately=True):
        self.id = subscriber_id
        self.handler = handler
        self.mode = mode  # "all", "new", "lastN"
        self.last_n = last_n
        self.batch_size = batch_size
        self.deliver_immediately = deliver_immediately
        self.cursor = 0

    def receive(self, message):
        print(f"Subscriber {self.id} received message: {message}")

    def subscribe(self, queue):
        pass

    def unsubscribe(self, queue):
        pass
