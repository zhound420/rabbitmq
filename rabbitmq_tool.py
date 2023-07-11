from base_toolkit import BaseToolkit
from rabbitmq_connection import RabbitMQConnection


class RabbitMQTool(BaseToolkit):
    def __init__(self, config, operation_type=None, input=None):
        super().__init__(config)
        self.operation_type = operation_type
        self.input = input

        self.rabbitmq_connection = RabbitMQConnection(config)

    def process(self):
        if self.operation_type == "send_message":
            return self.rabbitmq_connection.send_message(self.input)
        elif self.operation_type == "receive_message":
            return self.rabbitmq_connection.receive_message()
        else:
            raise Exception(f"Unsupported operation_type: {self.operation_type}")

    def get_env_keys(self):
        return ["rabbitmq_url"]

    def get_tools(self):
        return ["rabbitmq"]
