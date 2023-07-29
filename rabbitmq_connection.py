import pika
from abc import ABC, abstractmethod

class RabbitMQConnection(ABC):
    def __init__(self, server: str, username: str, password: str):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(server, credentials=credentials))
        self.channel = self.connection.channel()
        
    @abstractmethod
    def send_message(self, queue_name: str, message: str, persistent: int, priority: int):
        pass
    
    @abstractmethod
    def receive_message(self, queue_name: str):
        pass

    def close_connection(self):
        self.connection.close()
