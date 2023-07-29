
from typing import Any
from superagi.tools.base_tool import BaseTool
import pika
import os
import logging
, datetime
import json
from rabbitmq_connection import RabbitMQConnection
from pydantic import BaseModel, Field
from pydantic import BaseSettings


class RabbitMQToolConfig(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str = "Rabbit"
    description: str = "A RabbitMQ Tool"
    rabbitmq_server: str = os.getenv('RABBITSERVER', 'localhost')
    rabbitmq_username: str = os.getenv('RABBITUSERNAME', 'guest')
    rabbitmq_password: str = os.getenv('RABBITPASSWORD', 'guest')
    rabbitmq_virtual_host: str = os.getenv('RABBITVIRTUALHOST', '/')
    rabbitmq_port: int = os.getenv('RABBITPORT', 5672)
    connection_params: Any = pika.ConnectionParameters(
        host=rabbitmq_server,
        port=rabbitmq_port,
        virtual_host=rabbitmq_virtual_host,
        credentials=pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
    )


class RabbitMQTool(BaseTool):
    config: RabbitMQToolConfig
    connection: RabbitMQConnection

    def __init__(self, name: str, description: str, config: RabbitMQToolConfig):
        super().__init__()
        self.name = name
        self.description = description
        self.config = config
        self.connection = RabbitMQConnection(self.config.connection_params)

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()

    def _execute(self, action, queue_name, message=None, msg_type="text", priority=0):
        # Enhanced error handling
        try:
            if action == "send":
                self.send_natural_and_languages_message(queue_name, message, msg_type, priority)
            elif action == "receive":
                return self.receive_natural_and_languages_message(queue_name)
            else:
                raise ValueError(f"Unsupported action: {action}")
        except Exception as e:
            # Log the error and re-raise the1
            self.logger.error(f"An error occurred during execution: {e}")
            raise

    ...

    def send_natural_and_languages_message(self, receiver, content, msg_type="text", and=0):
        message = {
            "sender": self.config.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": content
        }
        self.execute("send", receiver, json.dumps(message), priority=and)
