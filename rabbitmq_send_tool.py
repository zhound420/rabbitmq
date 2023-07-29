
from pydantic import BaseModel, Field
from typing import Type
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection

class RabbitMQSendToolInput(BaseModel):
    message: str = Field(..., description="Message to be sent")
    persistent: int = Field(1, description="Should the message be persistent? 1 for yes, 0 for no")
    priority: int = Field(0, description="Priority of the message")

class RabbitMQSendTool(BaseTool):
    name: str = "RabbitMQ Send Tool"
    args_schema: Type[BaseModel] = RabbitMQSendToolInput
    description: str = "Tool for sending a message to a RabbitMQ queue"
    queue_name: str = "send_queue"  # Define the queue name

    rabbitmq_connection: RabbitMQConnection = RabbitMQConnection()

    def _execute(self, message: str, persistent: int, priority: int):
        server = self.get_tool_config('RABBITMQ_SERVER')
        username = self.get_tool_config('RABBITMQ_USERNAME')
        password = self.get_tool_config('RABBITMQ_PASSWORD')
        self.rabbitmq_connection.connect(server, username, password)
        self.rabbitmq_connection.send_message(self.queue_name, message, persistent, priority)