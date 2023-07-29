from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from rabbitmq_connection import RabbitMQConnection

class RabbitMQSendToolInput(BaseModel):
    queue_name: str = Field(..., description="Name of the RabbitMQ queue to send message to")
    message: str = Field(..., description="Message to be sent")
    persistent: int = Field(..., description="Message persistence. 1 for non-persistent, 2 for persistent")
    priority: int = Field(..., description="Message priority")

class RabbitMQSendTool(BaseTool):
    name: str = "RabbitMQ Send Tool"
    args_schema: Type[BaseModel] = RabbitMQSendToolInput
    description: str = "A tool for sending messages to a RabbitMQ server."
    rabbitmq_connection: RabbitMQConnection = None

    def _execute(self, queue_name: str, message: str, persistent: int, priority: int):
        # Initialize the RabbitMQ connection if it's not already initialized
        if self.rabbitmq_connection is None:
            self.rabbitmq_connection = RabbitMQConnection(
                server=self.get_tool_config('RABBITMQ_SERVER'),
                username=self.get_tool_config('RABBITMQ_USERNAME'),
                password=self.get_tool_config('RABBITMQ_PASSWORD')
            )

        # Use the RabbitMQConnection to establish a connection and send a message
        self.rabbitmq_connection.connect()
        self.rabbitmq_connection.send_message(queue_name, message, persistent, priority)
        