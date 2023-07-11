from superagi.tools.rabbitmq.rabbitmq_connection import RabbitMQConnection
from superagi.tools.base_tool import BaseToolkit

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
        )

        rabbitmq_connection.run()

    def run_operation(self, operation_type, input):
        if operation_type == "send_message":
            self.send_message()
        else:
            raise NotImplementedError

    @staticmethod
    def get_tool_name():
        return "rabbitmq"

    @staticmethod
    def get_operations():
        return [
            "send_message",
        ]

    def get_env_keys(self):
        pass

    def get_tools(self):
        pass
