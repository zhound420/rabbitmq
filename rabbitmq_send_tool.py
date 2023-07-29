
from pydantic import BaseModel, Field
from typing import Type
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection

class RabbitMQSendToolInput(BaseModel):
    message: str = Field(..., description="Message to be sent")
    persistent: int = Field(1, description="Should the message be persistent? 1 for yes, 0 for no")
    priority: int = Field(0, description="Priority of the message")

class RabbitMQSendTool(RabbitMQConnection, BaseTool):
    name: str = "RabbitMQ Send Tool"
    args_schema: Type[BaseModel] = RabbitMQSendToolInput
    description: str = "Tool for sending a message to a RabbitMQ queue"
    queue_name: str = "conversation_queue"  # Define the queue name

    def _execute(self, message: str, persistent: int, priority: int):
        self.send_message(self.queue_name, message, persistent, priority)
        
    def send_message(self, queue_name: str, message: str, persistent: int, priority: int):
        self.connect()
        self.channel.queue_declare(queue=queue_name, durable=True)
        properties = pika.BasicProperties(
            delivery_mode=persistent,
            priority=priority
        )
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=properties
        )
        
    def receive_message(self):
        pass  # This method is not used in this class, but it's required by the parent class