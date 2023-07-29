
from pydantic import BaseModel, Field
from typing import Type
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection

class RabbitMQReceiveToolInput(BaseModel):
    pass

class RabbitMQReceiveTool(BaseTool):
    name: str = "RabbitMQ Receive Tool"
    args_schema: Type[BaseModel] = RabbitMQReceiveToolInput
    description: str = "Tool for receiving a message from a RabbitMQ queue"
    queue_name: str = "receive_queue"  # Define the queue name

    rabbitmq_connection: RabbitMQConnection = RabbitMQConnection()

    def _execute(self):
        server = self.get_tool_config('RABBITMQ_SERVER')
        username = self.get_tool_config('RABBITMQ_USERNAME')
        password = self.get_tool_config('RABBITMQ_PASSWORD')
        self.rabbitmq_connection.connect(server, username, password)
        return self.rabbitmq_connection.receive_message(self.queue_name)