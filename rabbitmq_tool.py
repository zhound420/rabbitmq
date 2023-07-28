
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
    rabbitmq_virtual_host: str = os.getenv('RABBITMQ_VIRTUAL_HOST', '/')
    rabbitmq_port: int = os.getenv('RABBITMQ_PORT', 5672)
    connection_params: pika.ConnectionParameters = pika.ConnectionParameters(
        host=rabbitmq_server,
        port=rabbitmq_port,
        virtual_host=rabbitmq_virtual_host,
        credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    )

class RabbitMQTool(BaseTool):
    config: RabbitMQToolConfig
    connection: RabbitMQConnection

    def __init__(self, config: RabbitMQToolConfig):
        self.config = config
        self.connection = RabbitMQConnection(self.config.connection_params)
        super().__init__()

    def __del__(self):
        # Close the connection when the tool is destroyed
        self.connection.close()

    def _execute(self, action, queue_name, message=None, msg_type="text", priority=0):
        # Enhanced error handling
        try:
            if action == "send":
                self.send_natural_language_message(queue_name, message, msg_type, priority)
            elif action == "receive":
                return self.receive_natural_language_message(queue_name)
            else:
                raise ValueError(f"Unsupported action: {action}")
        except Exception as e:
            # Log the error and re-raise the exception
            self.logger.error(f"An error occurred during execution: {e}")
            raise

    ...

    def send_natural_language_message(self, receiver, content, msg_type="text", priority=0):
        message = {
            "sender": self.config.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": content
        }
        self.execute("send", receiver, json.dumps(message), priority=priority)
