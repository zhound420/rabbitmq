from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from rabbitmq_connection import RabbitMQConnection
from superagi.agent.super_agi import SuperAgi

class RabbitMQReceiveToolInput(BaseModel):
    agent_id: str
    queue_name: str = Field(..., description="Name of the RabbitMQ queue to receive message from")

class RabbitMQReceiveTool(BaseTool):
    name: str = "RabbitMQ Receive Tool"
    args_schema: Type[BaseModel] = RabbitMQReceiveToolInput
    description: str = "This tool receives a message from a RabbitMQ queue."

    def _execute(self, ai_name: str):
        queue_name = f"{ai_name}_queue"
        # Initialize the RabbitMQ connection if it's not already initialized
        if self.rabbitmq_connection is None:
            self.rabbitmq_connection = RabbitMQConnection(
                server=self.get_tool_config('RABBITMQ_SERVER'),
                username=self.get_tool_config('RABBITMQ_USERNAME'),
                password=self.get_tool_config('RABBITMQ_PASSWORD')
            )

        # Use the RabbitMQConnection to establish a connection and receive a message
        self.rabbitmq_connection.connect()
        message = self.rabbitmq_connection.receive_message(f"{ai_name}_queue") or "No messages in the queue" or "No messages in the queue"
        return message or "No messages in the queue"