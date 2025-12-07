from queue import Queue

class Subscriber:
    def __init__(self, subscriber_id, handler, mode="new", last_n=None, batch_size=1, deliver_immediately=True):
        self.id = subscriber_id #id
        self.handler = handler #
        self.last_n = last_n
        self.batch_size = batch_size #количество сообщений для выдачи
        self.deliver_immediately = deliver_immediately
        self.cursor = 0 #курсор 


    def receive(self, message):
        print(f"Subscriber {self.id} received message: {message}")

    def subscribe(self, queue):
        pass

    def unsubscribe(self, queue):
        pass

    def show_all(self, queue, subscriber, batch_size=None):
        all_messages = queue.main_queue[:]
        if batch_size is None or batch_size == 0:
            subscriber.receive(all_messages)
        else:
            for i in range(0, len(all_messages), batch_size):
                subscriber.receive(all_messages[i:i + batch_size])

    def show_lastN(self, queue, subscriber, lastN, batch_size=None):
        last_messages = queue.main_queue[-lastN:]
        if batch_size is None or batch_size == 0:
            subscriber.receive(last_messages)
        else:
            for i in range(0, len(last_messages), batch_size):
                subscriber.receive(last_messages[i:i + batch_size])

