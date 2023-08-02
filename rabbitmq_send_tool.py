from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from rabbitmq_connection import RabbitMQConnection
from superagi.agent.super_agi import SuperAgi

class RabbitMQSendToolInput(BaseModel):
    ai_name: str
    queue_name: str = Field(..., description="Name of the RabbitMQ queue to send message to")
    message: str = Field(..., description="Message to be sent")
    persistent: int = Field(..., description="Message persistence. 1 for non-persistent, 2 for persistent")
    priority: int = Field(..., description="Message priority")


class RabbitMQSendTool(BaseTool):
    name: str = "RabbitMQ Send Tool"
    args_schema: Type[BaseModel] = RabbitMQSendToolInput
    description: str = "This tool sends a message to a RabbitMQ queue."

    def _execute(self, ai_name: str, message: str, persistent: int = 1, priority: int = 1):
        queue_name = f"{ai_name}_queue"

        if self.rabbitmq_connection is None:
            self.rabbitmq_connection = RabbitMQConnection(
                server=self.get_tool_config('RABBITMQ_SERVER'),
                username=self.get_tool_config('RABBITMQ_USERNAME'),
                password=self.get_tool_config('RABBITMQ_PASSWORD')
            )

        # Use the RabbitMQConnection to establish a connection and send a message
        self.rabbitmq_connection.connect()
        return self.rabbitmq_connection.send_message(f"{ai_name}_queue", message, persistent, priority) or "Message sent" or "Message sent" or "Message sent"
        