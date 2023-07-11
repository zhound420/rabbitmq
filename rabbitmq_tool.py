from superagi.tools.rabbitmq.rabbitmq_connection import RabbitMQConnection
from superagi.tools.base_toolkit import BaseToolkit
from superagi.helper.tool_helper import Operation

class RabbitMQTool(BaseToolkit):
    def __init__(self, config, operation_type=None, input=None):
        super().__init__(config, operation_type, input)
        self.rabbitmq_server = config.rabbitmq_server
        self.rabbitmq_username = config.rabbitmq_username
        self.rabbitmq_password = config.rabbitmq_password
        self.queue_name = config.queue_name
        self.message = config.message

        if not isinstance(self.queue_name, str):
            raise TypeError('queue_name must be a string')

    def send_message(self):
        rabbitmq_connection = RabbitMQConnection(
            queue_name=self.queue_name,
            message=self.message,
            rabbitmq_server=self.rabbitmq_server,
            rabbitmq_username=self.rabbitmq_username,
            rabbitmq_password=self.rabbitmq_password,
        )from base_toolkit import BaseToolkit
from rabbitmq_connection import RabbitMQConnection
import json

class RabbitMQTool(BaseToolkit):

    def __init__(self, tool_name, queue_name, username, password, host):
        super().__init__(tool_name=tool_name)
        self.rabbitmq_connection = RabbitMQConnection(
            queue_name=queue_name, username=username, password=password, host=host
        )
        self.queue_name = queue_name

    def execute(self, operation, data=None):
        super().execute(operation=operation)
        if operation == "send_message":
            self.rabbitmq_connection.message = json.dumps(data)
            self.rabbitmq_connection.connect()
        elif operation == "receive_message":
            self.rabbitmq_connection.connect()
            return self.rabbitmq_connection.message

        rabbitmq_connection.run()

    def run_operation(self, operation_type, input):
        if operation_type == Operation.SEND_MESSAGE:
            self.send_message()
        else:
            raise NotImplementedError

    @staticmethod
    def get_tool_name():
        return "rabbitmq"

    @staticmethod
    def get_operations():
        return [
            Operation.SEND_MESSAGE,
        ]
