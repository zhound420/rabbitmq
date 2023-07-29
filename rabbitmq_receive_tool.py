from pydantic import BaseModel, Field
from typing import Type
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection

class RabbitMQReceiveToolInput(BaseModel):
    pass

class RabbitMQReceiveTool(RabbitMQConnection, BaseTool):
    name: str = "RabbitMQ Receive Tool"
    args_schema: Type[BaseModel] = RabbitMQReceiveToolInput
    description: str = "Tool for receiving a message from a RabbitMQ queue"
    queue_name: str = "conversation_queue"  # Define the queue name

    def _execute(self):
        return self.receive_message(self.queue_name)
        
    def send_message(self, queue_name: str, message: str, persistent: int, priority: int):
        pass  # This method is not used in this class, but it's required by the parent class

    def receive_message(self, queue_name: str):
        self.channel.queue_declare(queue=queue_name, durable=True)
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return body.decode('utf-8')
        else:
            return 'No message in queue'
