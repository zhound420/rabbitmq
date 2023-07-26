
import os
from superagi.common.base_tool import BaseToolkit
from superagi.tools.rabbitmq.rabbitmq_tool import RabbitMQTool
from superagi.tools.rabbitmq.rabbitmq_connection import RabbitMQConnection


class RabbitMQToolkit(BaseToolkit):
    def __init__(self):
        self.rabbitmq_server = os.getenv('RABBITMQ_SERVER', 'localhost')
        self.rabbitmq_username = os.getenv('RABBITMQ_USERNAME', 'guest')
        self.rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

        self.tools = {
            "RabbitMQTool": RabbitMQTool,
            "RabbitMQConnection": RabbitMQConnection
        }