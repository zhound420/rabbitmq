import os
from abc import ABC
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection
import json
import datetime

class RabbitMQTool(BaseTool, BaseModel):
    """
    Class for RabbitMQ tools. This class includes various tools to interact with RabbitMQ.
    """
    logger: Any
    name: str = "RabbitMQTool"
    description: str = "Tool that contains various operations to interact with RabbitMQ"

    rabbitmq_server: str = Field(default_factory=lambda: os.getenv('RABBITMQ_SERVER', 'localhost'))
    rabbitmq_username: str = Field(default_factory=lambda: os.getenv('RABBITMQ_USERNAME', 'guest'))
    rabbitmq_password: str = Field(default_factory=lambda: os.getenv('RABBITMQ_PASSWORD', 'guest'))

    def _execute(self, operation, args):
        """
        Executes the desired operation.
        """
        if operation == "send_message":
            if "receiver" not in args or "content" not in args:
                raise ValueError("Incomplete tool args: 'receiver' and 'content' are required for send_message operation.")
            receiver = args["receiver"]
            content = args["content"]
            msg_type = args.get("msg_type", "text")
            priority = args.get("priority", 0)
            return self._execute_send(receiver, json.dumps(content), priority=priority)

        elif operation == "receive_message":
            if "queue_name" not in args:
                raise ValueError("Incomplete tool args: 'queue_name' is required for receive_message operation.")
            queue_name = args["queue_name"]
            return self._execute_receive(queue_name)

        else:
            raise ValueError(f"Unknown operation: '{operation}'")

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
        return self._execute("send_message", {
            "receiver": receiver,
            "content": json.dumps(message),
            "msg_type": msg_type,
            "priority": priority
        })

    def receive_message(self, queue_name):
        """
        Receive a message.
        """
        raw_message = self._execute("receive_message", {"queue_name": queue_name})
        message = json.loads(raw_message)
        return message["content"]

    # ... Similarly, define methods for other operations ...
