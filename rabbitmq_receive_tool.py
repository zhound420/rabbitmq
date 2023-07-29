
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection
import os

class RabbitMQReceiveTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "RabbitMQ Receive Tool"
        self.description = "A tool for receiving messages from a RabbitMQ server."
        self.rabbitmq_connection = RabbitMQConnection()

    def _execute(self, queue_name):
        # Use the RabbitMQConnection to establish a connection and receive a message
        self.rabbitmq_connection.connect()
        return self.rabbitmq_connection.receive_message(queue_name)