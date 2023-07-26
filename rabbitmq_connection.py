
import pika
from abc import ABC
from pydantic import BaseModel
from typing import Any, Optional
from superagi.tools.base_tool import BaseTool

class RabbitMQConnection(BaseTool, BaseModel, ABC):
    name: str  
    description: str = "Connection class for RabbitMQ"
    logger: Any
    connection_params: Any
    mode: str
    queue_name: str
    message: Optional[str] = None

    def __init__(self, connection_params, mode, queue_name, message=None):
        super().__init__(connection_params=connection_params, mode=mode, queue_name=queue_name, message=message)
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

    def send(self):
        if self.channel:
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=self.message)
            self.connection.close()
        else:
            print("Cannot send message. Channel is None.")
        
    def receive(self):
        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        if self.channel:
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()
        else:
            print("Cannot receive message. Channel is None.")

    def _execute(self, tool_input):
        if self.mode == 'send':
            self.send()
        elif self.mode == 'receive':
            self.receive()