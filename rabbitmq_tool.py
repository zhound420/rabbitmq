import os
import json
import datetime
import pika
from abc import ABC
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection

class RabbitMQTool(BaseTool, BaseModel):
    logger: Any
    name: str = "RabbitMQTool"
    description: str = "Tool that contains various operations to interact with RabbitMQ"

    rabbitmq_server: str = Field(default_factory=lambda: os.getenv('RABBITMQ_SERVER', 'localhost'))
    rabbitmq_username: str = Field(default_factory=lambda: os.getenv('RABBITMQ_USERNAME', 'guest'))
    rabbitmq_password: str = Field(default_factory=lambda: os.getenv('RABBITMQ_PASSWORD', 'guest'))

    def build_connection_params(self):
        credentials = pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        return pika.ConnectionParameters(host=self.rabbitmq_server, credentials=credentials)

    def _execute(self, *args, **kwargs):
        tool_input = kwargs.get("tool_input", {})
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                tool_input = {"action": "send", "queue": "Linda", "message": tool_input}

        action = tool_input.get("action")
        if action == "send":
            queue = tool_input.get("queue")
            message = tool_input.get("message")
            return self._execute_send(queue, message)
        elif action == "receive":
            queue_name = tool_input.get("queue")
            return self._execute_receive(queue_name)
        else:
            raise ValueError(f"Unknown action: '{action}'")

    def _execute_send(self, queue, message, persistent=False, priority=0):
        connection_params = self.build_connection_params()
        connection = RabbitMQConnection(connection_params, "send", queue, message, persistent, priority)
        connection.run()

        # Construct the message to be sent
        message = {
            "sender": self.name,
            "receiver": queue,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "text",
            "content": message
        }
        return json.dumps(message)

    def _execute_receive(self, queue_name):
        connection_params = self.build_connection_params()
        connection = RabbitMQConnection(connection_params, "receive", queue_name)
        raw_message = connection.run()
        message = json.loads(raw_message)
        return message["content"]
