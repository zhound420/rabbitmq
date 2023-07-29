
from abc import ABC, abstractmethod
import pika

class RabbitMQConnection(ABC):
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self, server: str, username: str, password: str):
        credentials = pika.PlainCredentials(username, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(server, 5672, '/', credentials))
        self.channel = self.connection.channel()

    def send_message(self, queue_name: str, message: str, persistent: int, priority: int):
        self.channel.queue_declare(queue=queue_name, durable=True)
        properties = pika.BasicProperties(delivery_mode=persistent, priority=priority)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message, properties=properties)

    def receive_message(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name, durable=True)
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return body.decode()
        else:
            return None

    @abstractmethod
    def close_connection(self):
        if self.connection:
            self.connection.close()