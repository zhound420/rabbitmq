
from superagi.tools.base_tool import BaseTool


class RabbitMQConnection(BaseTool):
    def __init__(self, rabbitmq_server: str, rabbitmq_username: str, rabbitmq_password: str):
        self.rabbitmq_server = rabbitmq_server
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password

    def connect(self):
        pass