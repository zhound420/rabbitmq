
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from rabbitmq_connection import RabbitMQConnection

class RabbitMQSendToolInput(BaseModel):
    message: str = Field(..., description="Message to be sent")
    persistent: int = Field(1, description="Should the message be persistent? 1 for yes, 0 for no")
    priority: int = Field(0, description="Priority of the message")

class RabbitMQSendTool(BaseTool):
    name: str = "RabbitMQ Send Tool"
    args_schema: Type[BaseModel] = RabbitMQSendToolInput
    description: str = "Tool for sending a message to a RabbitMQ queue"
    queue_name: str = "conversation_queue"  # Define the queue name

    rabbitmq_connection: RabbitMQConnection = RabbitMQConnection()

    def _execute(self, message: str, persistent: int, priority: int):
        # We no longer need to call the connect() method
        # self.rabbitmq_connection.connect()
        
        self.rabbitmq_connection.send_message(self.queue_name, message, persistent, priority)