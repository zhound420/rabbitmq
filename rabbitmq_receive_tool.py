from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from rabbitmq_connection import RabbitMQConnection

class RabbitMQReceiveToolInput(BaseModel):
    queue_name: str = Field(..., description="Name of the RabbitMQ queue to receive message from")

class RabbitMQReceiveTool(BaseTool):
    name: str = "RabbitMQ Receive Tool"
    args_schema: Type[BaseModel] = RabbitMQReceiveToolInput
    description: str = "A tool for receiving messages from a RabbitMQ server."
    rabbitmq_connection: RabbitMQConnection = None

    def _execute(self, queue_name: str):
        # Initialize the RabbitMQ connection if it's not already initialized
        if self.rabbitmq_connection is None:
            self.rabbitmq_connection = RabbitMQConnection(
                server=self.get_tool_config('RABBITMQ_SERVER'),
                username=self.get_tool_config('RABBITMQ_USERNAME'),
                password=self.get_tool_config('RABBITMQ_PASSWORD')
            )

        # Use the RabbitMQConnection to establish a connection and receive a message
        self.rabbitmq_connection.connect()
        return self.rabbitmq_connection.receive_message(queue_name)