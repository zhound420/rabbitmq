
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
    queue_name: str  # Define the queue name

    rabbitmq_connection: RabbitMQConnection = RabbitMQConnection()

    def _execute(self):
        return self.rabbitmq_connection.receive_message(self.queue_name)