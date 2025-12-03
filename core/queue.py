from subscriber import Subscriber

class Queue:
    def __init__(self, capacity=100):
        self.main_queue = []
        self.priority_queue = []
        self.capacity = capacity
        self.subscribers = []

    # Методы
    def enqueue(self, message):
        if len(self.main_queue) >= self.capacity: 
            return
        self.main_queue.append(message)
        self.notify_subscriber(message)


    def dequeue(self, subscriber_id, batch_size=1):
        sub = None
        for s in self.subscribers:
            if s.id == subscriber_id:
                sub = s
                break
        if sub is None:
            return None


    def register_subscriber(self, subscriber):
        for s in self.subscribers:
            if s.id == subscriber.id:
                return
        self.subscribers.append(subscriber)

    def unregister_subscriber(self, subscriber_id):
        for s in self.subscribers:
            if s.id == subscriber_id:
                self.subscribers.remove(s)
                break

    def notify_subscriber(self, message):
        for subscriber in self.subscribers:
            subscriber.receive(message)

    def clean_expired_messages(self):
        pass

    def handle_overflow(self):
        pass
