from subscriber import Subscriber
from datetime import datetime

class Queue:
    def __init__(self, capacity=100):
        self.main_queue = []          # здесь хранятся ВСЕ обычные сообщения
        self.priority_queue = []      # здесь будут храниться важные / исключения
        self.capacity = capacity       # максимальное количество сообщений
        self.subscribers = []          # список всех подписчиков (объекты Subscriber)
        self.last_signature = None
        self.repeat_count = 0
        self.last_time = datetime.min
        self.cooldown = 5

    # добавление сообщения в очередь
    def enqueue(self, message):
        # 1. проверить, не переполнена ли очередь
        # 2. если переполнена — ничего не добавлять (или вызвать handle_overflow)
        # 3. если не переполнена — добавить сообщение в main_queue
        # 4. уведомить всех подписчиков о новом сообщении (notify_subscriber)
        now = datetime.now()
        seconds_passed = (now - self.last_time).total_seconds()
        if seconds_passed < self.cooldown:
            return
        if len(self.main_queue) >= self.capacity: 
            self.handle_overflow(batch_size = 10)
        self.main_queue.append(message)
        self.notify_subscriber(message)
        self.last_time = now


    # получение сообщений конкретным подписчиком
    def dequeue(self, subscriber_id, batch_size=1):
        # 1. найти нужного подписчика по id
        # 2. если такого нет — вернуть None
        # 3. узнать его cursor (откуда он читает)
        # 4. взять batch_size сообщений начиная с cursor
        # 5. передвинуть cursor у подписчика на batch_size
        # 6. вернуть эти сообщения

        sub = None
        for s in self.subscribers:
            if s.id == subscriber_id:
                sub = s
                if sub.cursor + batch_size <= len(self.main_queue):
                    messages = self.main_queue[sub.cursor : sub.cursor + batch_size]
                    sub.cursor += len(messages)
                else:
                    messages = self.main_queue[sub.cursor : len(self.main_queue)]
                    sub.cursor += len(messages)
                break

        if sub is None:
            return None
        return messages


    # регистрация подписчика
    def register_subscriber(self, subscriber):
        # 1. проверить, нет ли уже подписчика с таким id
        # 2. если есть — ничего не делать
        # 3. если нет — добавить его в список subscribers
        for s in self.subscribers:
            if s.id == subscriber.id:
                return
        self.subscribers.append(subscriber)


    # удаление подписчика из очереди
    def unregister_subscriber(self, subscriber_id):
        # 1. найти подписчика по id
        # 2. удалить его из списка subscribers
        for s in self.subscribers:
            if s.id == subscriber_id:
                self.subscribers.remove(s)
                break


    # уведомление всех подписчиков о новом сообщении
    def notify_subscriber(self, message):
        # 1. пройти по всем подписчикам
        # 2. у каждого вызвать метод receive(message)
        for subscriber in self.subscribers:
            subscriber.receive(message)


    # удаление старых сообщений (по времени жизни)
    def clean_expired_messages(self):
        # 1. пройти по очереди
        # 2. проверить, какие сообщения устарели
        # 3. удалить устаревшие
        pass

    # обработка переполнения очереди
    def handle_overflow(self, batch_size = 10):
        # 1. решаем, какие сообщения удаляем при переполнении
        # 2. например: самые старые
        while len(self.main_queue) > self.capacity:
            messages_to_delete = self.main_queue[:batch_size]
            for subscriber in self.subscribers:
                if subscriber.mode == "all" and subscriber.cursor < len(messages_to_delete):
                    subscriber.receive(messages_to_delete)
                    subscriber.cursor += len(messages_to_delete)
            self.main_queue = self.main_queue[batch_size:]