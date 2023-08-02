
import pika
import json
from typing import Any
from pydantic import BaseModel, Field

from superagi.tools.base_tool import BaseTool

class RabbitMQReceiveToolInput(BaseModel):
    queue_name: str = Field(..., description="Name of the RabbitMQ queue to receive the message from")

class RabbitMQReceiveTool(BaseTool):
    name: str = "RabbitMQ Receive Tool"
    args_schema: Type[BaseModel] = RabbitMQReceiveToolInput
    description: str = "This tool receives a message from a specified RabbitMQ queue"

    def __init__(self, ai_name):
        super().__init__()
        self.ai_name = ai_name

    def _execute(self, queue_name: str = None):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        queue_name = self.ai_name + "_" + queue_name
        channel.queue_declare(queue=queue_name)

        method_frame, header_frame, body = channel.basic_get(queue=queue_name)
        if method_frame:
            channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            return "No messages in the queue"