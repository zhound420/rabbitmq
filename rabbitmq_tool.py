from abc import ABC
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection
import json
import datetime

class RabbitMQTool(BaseTool, ABC):
    """
    Class for RabbitMQ tools. This class includes various tools to interact with RabbitMQ.
    """
    rabbitmq_server: str
    rabbitmq_username: str
    rabbitmq_password: str
    logger: Any

    name: str = "RabbitMQTool"
    description: str = "Tool that contains various operations to interact with RabbitMQ"

    def __init__(self, rabbitmq_server, rabbitmq_username, rabbitmq_password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rabbitmq_server = rabbitmq_server
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password

    def _execute(self, *args, **kwargs):
        """
        Placeholder for the _execute method.
        """
        raise NotImplementedError("Each subclass must implement its own _execute method.")

    def _execute_send(self, receiver, message, persistent=False, priority=0):
        """
        Execute a RabbitMQ send operation.
        """
        connection = RabbitMQConnection(self.connection_params, "send", receiver, message, persistent, priority)
        return connection.run()

    def _execute_receive(self, queue_name):
        """
        Execute a RabbitMQ receive operation.
        """
        connection = RabbitMQConnection(self.connection_params, "receive", queue_name)
        return connection.run()

    # ... Similarly, define _execute methods for other operations ...

    def send_message(self, receiver, content, msg_type="text", priority=0):
        """
        Send a message.
        """
        message = {
            "sender": self.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": content
        }
        return self._execute_send(receiver, json.dumps(message), priority=priority)

    def receive_message(self, queue_name):
        """
        Receive a message.
        """
        raw_message = self._execute_receive(queue_name)
        message = json.loads(raw_message)
        return message["content"]

    # ... Similarly, define methods for other operations ...
