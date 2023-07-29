
import abc
import pika
from typing import Optional


class RabbitMQConnection(abc.ABC):
    connection: Optional[pika.BlockingConnection] = None
    channel: Optional[pika.channel.Channel] = None

    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.username = username
        self.password = password

    def open_connection(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.server, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def close_connection(self):
        if self.connection is not None and self.connection.is_open:
            self.connection.close()
            self.connection = None
            self.channel = None

    @abc.abstractmethod
    def send_message(self, queue_name: str, message: str, persistent: int, priority: int):
        pass

    @abc.abstractmethod
    def receive_message(self, queue_name: str):
        pass