
import pika
from abc import ABC, abstractmethod

class RabbitMQConnection(ABC):
    def __init__(self, server="localhost", username="guest", password="guest"):
        self.server = server
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.server, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    @abstractmethod
    def send_message(self, queue_name: str, message: str, persistent: int, priority: int):
        pass

    @abstractmethod
    def receive_message(self, queue_name: str):
        pass