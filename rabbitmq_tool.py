from typing import Any
from superagi.tools.base_tool import BaseTool
import pika
import os
import logging
import datetime
import json
from rabbitmq_connection import RabbitMQConnection
from pydantic import BaseModel, Field

class RabbitMQToolConfig(BaseModel):
    name: str = Field("RabbitMQ Tool")
    description: str = Field("A tool for interacting with RabbitMQ")
    rabbitmq_server: str = Field(default_factory=lambda: os.getenv('RABBITMQ_SERVER', 'localhost'))
    rabbitmq_username: str = Field(default_factory=lambda: os.getenv('RABBITMQ_USERNAME', 'guest'))
    rabbitmq_password: str = Field(default_factory=lambda: os.getenv('RABBITMQ_PASSWORD', 'guest'))
    connection_params: Any = Field(default_factory=lambda: pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_SERVER', 'localhost'),
            credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USERNAME', 'guest'), os.getenv('RABBITMQ_PASSWORD', 'guest'))
        ))
    logger: Any = Field(default_factory=lambda: logging.getLogger(__name__))

class RabbitMQTool(BaseTool, BaseModel):  # note the change in inheritance order
    config: RabbitMQToolConfig

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
