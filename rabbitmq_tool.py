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

    def _execute(self, *args, **kwargs):
        """
        Adjusted _execute method to handle kwargs.
        """
        tool_input = kwargs.get("tool_input", {})
        # Check if tool_input is a string and try to load it as a JSON object
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON string in tool_input: {tool_input}")
        elif not isinstance(tool_input, dict):
            raise TypeError(f"tool_input must be a string (containing JSON) or a dictionary, not {type(tool_input).__name__}")

        operation = tool_input.get("operation")
        if operation == "send_message":
            receiver = tool_input.get("receiver")
            content = tool_input.get("content")
            priority = tool_input.get("priority", 0)
            return self.send_message(receiver, content, priority=priority)
        elif operation == "receive_message":
            queue_name = tool_input.get("queue_name")
            return self.receive_message(queue_name)
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

    def _execute(self, *args, **kwargs):
        """
        Adjusted _execute method to handle kwargs.
        """
        tool_input = kwargs.get("tool_input", {})

        # Check if tool_input is a plain string
        if isinstance(tool_input, str):
            # If it's a string, treat it as a message to be sent
            tool_input = {
                "operation": "send_message",
                "receiver": "default_receiver",  # This is a placeholder; ideally, this should be determined dynamically
                "content": tool_input
            }
        elif isinstance(tool_input, dict):
            # If it's a dict, it's expected to be in the right format
            pass
        else:
            try:
                # Try to parse it as a JSON string
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                raise ValueError(f"Invalid JSON string in tool_input: {tool_input}")

        operation = tool_input.get("operation")
        if operation == "send_message":
            receiver = tool_input.get("receiver")
            content = tool_input.get("content")
            priority = tool_input.get("priority", 0)
            return self.send_message(receiver, content, priority=priority)
        elif operation == "receive_message":
            queue_name = tool_input.get("queue_name")
            return self.receive_message(queue_name)
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
"""
