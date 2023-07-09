from typing import Any
import os
import logging
import pika
from superagi.tools.base_tool import BaseTool

class RabbitMQTool(BaseTool):
    name = "RabbitMQ Tool"
    description = "A tool for interacting with RabbitMQ"
    rabbitmq_server: str = os.getenv('RABBITMQ_SERVER', 'localhost')
    rabbitmq_username: str = os.getenv('RABBITMQ_USERNAME', 'guest')
    rabbitmq_password: str = os.getenv('RABBITMQ_PASSWORD', 'guest')
    connection_params: Any
    logger: Any


    def __init__(self):
        super().__init__()  # Call the BaseTool's initializer if necessary
        self.connection_params = pika.ConnectionParameters(
            host=self.rabbitmq_server,
            credentials=pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        )
        self.logger = logging.getLogger(__name__)

    def _execute(self):
        # provide your implementation here
        pass

    def send_message(self, queue_name, message, persistent=False, priority=0):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        properties = pika.BasicProperties(delivery_mode=2) if persistent else None  # Makes message persistent
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message,
                              properties=properties,
                              priority=priority)
        connection.close()

    def receive_message(self, queue_name):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()

        method_frame, properties, body = channel.basic_get(queue_name, auto_ack=True)
        if method_frame:
            connection.close()
            return body.decode()
        else:
            connection.close()
            return None
