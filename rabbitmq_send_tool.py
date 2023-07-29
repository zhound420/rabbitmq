
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection
import os

class RabbitMQSendTool(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = "RabbitMQ Send Tool"
        self.description = "A tool for sending messages to a RabbitMQ server."
        self.rabbitmq_connection = RabbitMQConnection()

    def _execute(self, queue_name, message, persistent, priority):
        # Use the RabbitMQConnection to establish a connection and send a message
        self.rabbitmq_connection.connect()
        self.rabbitmq_connection.send_message(queue_name, message, persistent, priority)