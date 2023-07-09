from typing import List
from superagi.tools.base_tool import BaseTool
import pika
import os
import logging
import datetime
import json
from rabbitmq_connection import RabbitMQConnection
from pydantic import BaseModel
from typing import Any

    
class RabbitMQTool(BaseModel):
    name = "RabbitMQ Tool"
    description = "A tool for interacting with RabbitMQ"
    rabbitmq_server: str
    rabbitmq_username: str
    rabbitmq_password: str
    #connection_params: RabbitMQConnection
    logger: Any
    base_tool: BaseTool

    def __init__(self):
        self.rabbitmq_server = os.getenv('RABBITMQ_SERVER', 'localhost')
        self.rabbitmq_username = os.getenv('RABBITMQ_USERNAME', 'guest')
        self.rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.connection_params = pika.ConnectionParameters(
            host=self.rabbitmq_server,
            credentials=pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        )
        self.logger = logging.getLogger(__name__)
        # You may need to provide the specific parameters needed for BaseTool
        self.base_tool = BaseTool()

    def execute(self, action, queue_name, message=None, persistent=False, priority=0, callback=None, consumer_tag=None, delivery_tag=None):
        """
        Execute a RabbitMQ operation.
        
        The operation can be either "send", "receive", "create_queue", "delete_queue", "add_consumer", "remove_consumer", or "send_ack". 
        """
        try:
            connection = RabbitMQConnection(self.connection_params, action, queue_name, message, persistent, priority, callback, consumer_tag, delivery_tag)
            connection.run()
        except Exception as e:
            self.logger.error(f"Error executing action '{action}': {e}")
            # Return a default value or re-raise the exception, depending on your needs
            return None

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
        if raw_message is None:
            return None
        message = json.loads(raw_message)
        return message["content"]
