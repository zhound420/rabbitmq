
import pika
import json
from typing import Any, Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from superagi.agent.super_agi import SuperAgi

class RabbitMQSendToolInput(BaseModel):
    message: Any = Field(..., description="Message to be sent")
    queue_name: str = Field(..., description="Name of the RabbitMQ queue to send the message to")

class RabbitMQSendTool(BaseTool):
    name: str = "RabbitMQ Send Tool"
    args_schema: Type[BaseModel] = RabbitMQSendToolInput
    description: str = "This tool sends a message to a specified RabbitMQ queue"


    def _execute(self, message: str = None, queue_name: str = None):
        connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.4.194'))
        channel = connection.channel()

        queue_name = self.ai_name + "_" + queue_name
        channel.queue_declare(queue=queue_name)

        channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))

        connection.close()

        return "Sent"
