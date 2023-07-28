from typing import Any
from superagi.tools.base_tool import BaseTool
import pika
import os
import logging
import datetime
import json
from rabbitmq_connection import RabbitMQConnection
from pydantic import BaseModel, Field
from pydantic import BaseSettings

class RabbitMQToolConfig(BaseModel):
    name: str = "RabbitMQ Tool"
    description: str = "A tool for interacting with RabbitMQ"
    rabbitmq_server: str = os.getenv('RABBITMQ_SERVER', 'localhost')
    rabbitmq_username: str = os.getenv('RABBITMQ_USERNAME', 'guest')
    rabbitmq_password: str = os.getenv('RABBITMQ_PASSWORD', 'guest')
    connection_params: Any = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_SERVER', 'localhost'),
            credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USERNAME', 'guest'), os.getenv('RABBITMQ_PASSWORD', 'guest'))
        )
    logger: Any = logging.getLogger(__name__)

    def _execute(self):
        pass
class RabbitMQTool(BaseTool):
    config: RabbitMQToolConfig

    def __init__(self, config: RabbitMQToolConfig):
        self.config = config
        super().__init__()

    def _execute(self, action, queue_name, message=None, msg_type="text", priority=0):
        if action == "send":
            self.send_natural_language_message(queue_name, message, msg_type, priority)
        elif action == "receive":
            return self.receive_natural_language_message(queue_name)
        else:
            raise ValueError(f"Unsupported action: {action}")

    def execute(self, action, queue_name, message=None, persistent=False, priority=0, callback=None, consumer_tag=None, delivery_tag=None):
        connection = RabbitMQConnection(self.config.connection_params, action, queue_name, message, persistent, priority, callback, consumer_tag, delivery_tag)
        return connection.run()

    def send_natural_language_message(self, receiver, content, msg_type="text", priority=0):
        message = {
            "sender": self.config.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": content
        }
        self.execute("send", receiver, json.dumps(message), priority=priority)

    def receive_natural_language_message(self, queue_name):
        raw_message = self.execute("receive", queue_name)
        message = json.loads(raw_message)
        return message["content"]
