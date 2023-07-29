
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from rabbitmq_connection import RabbitMQConnection

class RabbitMQReceiveToolInput(BaseModel):
    pass

class RabbitMQReceiveTool(BaseTool):
    name: str = "RabbitMQ Receive Tool"
    args_schema: Type[BaseModel] = RabbitMQReceiveToolInput
    description: str = "Tool for receiving a message from a RabbitMQ queue"
    queue_name: str = "conversation_queue"  # Define the queue name

    rabbitmq_connection: RabbitMQConnection = RabbitMQConnection()

    def _execute(self):
        # We no longer need to call the connect() method
        # self.rabbitmq_connection.connect()
        
        return self.rabbitmq_connection.receive_message(self.queue_name)