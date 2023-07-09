from typing import Any
import os
import logging
import pika
from superagi.tools.base_tool import BaseTool

class RabbitMQTool(BaseTool):  # RabbitMQTool should only inherit from BaseTool
    name = "RabbitMQ Tool"
    description = "A tool for interacting with RabbitMQ"
    rabbitmq_server: str = os.getenv('RABBITMQ_SERVER', 'localhost')
    rabbitmq_username: str = os.getenv('RABBITMQ_USERNAME', 'guest')
    rabbitmq_password: str = os.getenv('RABBITMQ_PASSWORD', 'guest')
    connection_params: Any
    logger: Any

    def _execute(self, action, queue_name, message=None, persistent=False, priority=0, callback=None, consumer_tag=None, delivery_tag=None):
        """
        Execute a RabbitMQ operation.
        
        The operation can be either "send", "receive", "create_queue", "delete_queue", "add_consumer", "remove_consumer", or "send_ack". 
        """
        connection = RabbitMQConnection(self.connection_params, action, queue_name, message, persistent, priority, callback, consumer_tag, delivery_tag)
        connection.run()

    def send_natural_language_message(self, receiver, content, msg_type="text", priority=0):
        """
        Send a natural language message to a specified queue (receiver).
        """
        message = {
            "sender": self.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": content
        }
        self.execute("send", receiver, json.dumps(message), priority=priority)

    def receive_natural_language_message(self, queue_name):
        """
        Receive a natural language message from a specified queue.
        """
        raw_message = self.execute("receive", queue_name)
        message = json.loads(raw_message)
        return message["content"]
    
   