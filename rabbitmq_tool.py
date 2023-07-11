
from base_toolkit import BaseToolkit
from rabbitmq_connection import RabbitMQConnection
import json

class RabbitMQTool(BaseToolkit):

    def __init__(self, tool_name, queue_name, username, password, host):
        super().__init__(tool_name=tool_name)
        self.rabbitmq_connection = RabbitMQConnection(
            queue_name=queue_name, username=username, password=password, host=host
        )
        self.queue_name = queue_name

    def _execute(self, operation, data=None):
        super()._execute(operation=operation)
        if operation == "send_message":
            self.rabbitmq_connection.message = json.dumps(data)
            self.rabbitmq_connection.connect()
        elif operation == "receive_message":
            self.rabbitmq_connection.connect()
            return self.rabbitmq_connection.message

    def _execute_send(self, receiver, message):
        # Ensure that the arguments match with the __init__ method of RabbitMQConnection
        connection = RabbitMQConnection(
            queue_name=self.rabbitmq_connection.queue_name,
            username=self.rabbitmq_connection.username,
            password=self.rabbitmq_connection.password,
            host=self.rabbitmq_connection.host
        )
        connection.send_message(message)
        return message

    @staticmethod
    def get_tool_name():
        return "rabbitmq"

    @staticmethod
    def get_operations():
        return ["send_message", "receive_message"]
