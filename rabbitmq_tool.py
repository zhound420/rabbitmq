from typing import Any
import os
import logging
import datetime
import json
import pika
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection

class RabbitMQTool(BaseTool):  # RabbitMQTool should only inherit from BaseTool
    name = "RabbitMQ Tool"
    description = "A tool for interacting with RabbitMQ"
    rabbitmq_server: str = os.getenv('RABBITMQ_SERVER', 'localhost')
    rabbitmq_username: str = os.getenv('RABBITMQ_USERNAME', 'guest')
    rabbitmq_password: str = os.getenv('RABBITMQ_PASSWORD', 'guest')
    connection_params: Any
    logger: Any

    def __init__(self):
        super().__init__()  # Call the BaseTool's initializer if necessary
        self.connection_params = pika.ConnectionParameters(
            host=self.rabbitmq_server,
            credentials=pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        )
        self.logger = logging.getLogger(__name__)

    def _execute(self, action, queue_name, message=None, msg_type="text", priority=0):
        if action == "send":
            self.send_natural_language_message(queue_name, message, msg_type, priority)
        elif action == "receive":
            return self.receive_natural_language_message(queue_name)
        else:
            raise ValueError(f"Unsupported action: {action}")

    def execute(self, *args, **kwargs):
        # If args contains a single dictionary, unpack it into kwargs
        if len(args) == 1 and isinstance(args[0], dict):
            kwargs = args[0]

        # Extract thoughts from kwargs if present
        thoughts = kwargs.get('thoughts')
        if thoughts:
            # If 'thoughts' key is present, consider its 'text' value as the message argument if no message argument is provided
            kwargs['message'] = kwargs.get('message', thoughts.get('text'))

        # Extract variables from kwargs with default values
        action = kwargs.get('action')
        queue_name = kwargs.get('queue_name')
        message = kwargs.get('message', None)
        persistent = kwargs.get('persistent', False)
        priority = kwargs.get('priority', 0)
        callback = kwargs.get('callback', None)
        consumer_tag = kwargs.get('consumer_tag', None)
        delivery_tag = kwargs.get('delivery_tag', None)

        # Check for missing arguments and raise an error if any are missing
        if action is None or queue_name is None:
            raise ValueError('Missing required arguments for execute(). Arguments provided: {}'.format(kwargs))

        # Create a new RabbitMQConnection and run it
        connection = RabbitMQConnection(self.connection_params, action, queue_name, message, persistent, priority, callback, consumer_tag, delivery_tag)
        return connection.run()

    def send_natural_language_message(self, receiver, content, msg_type="text", priority=0):
        message = {
            "sender": self.name,
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
