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

    rabbitmq_server: str = "localhost"
    rabbitmq_username: str = "guest"
    rabbitmq_password: str = "guest"

    def build_connection_params(self):
        try:
            credentials = pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
            return pika.ConnectionParameters(host=self.rabbitmq_server, credentials=credentials)
        except Exception as e:
            self.logger.error(f"Failed to build RabbitMQ connection parameters: {e}")
            raise

    def _execute(self, *args, **kwargs):
        tool_input = kwargs.get("tool_input", {})
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                tool_input = {"operation": "send_message", "receiver": "Linda", "message": tool_input}
        
        operation = tool_input.get("operation")
        if operation in ["send_message", "publish"]:
            receiver = tool_input.get("receiver")
            message = tool_input.get("message")
            return self.send_message(receiver, message)
        elif operation == "receive_message":
            queue_name = tool_input.get("queue_name")
            return self.receive_message(queue_name)
        else:
            raise ValueError(f"Unknown operation: '{operation}'")

    def _execute_send(self, receiver, message, persistent=False, priority=0):
        connection_params = self.build_connection_params()
        connection = RabbitMQConnection(connection_params, "send", receiver, message, persistent, priority)
        return connection.run()

    def _execute_receive(self, queue_name):
        connection_params = self.build_connection_params()
        connection = RabbitMQConnection(connection_params, "receive", queue_name)
        return connection.run()

    def send_message(self, receiver, message, msg_type="text", priority=0):
        message = {
            "sender": self.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": message
        }
        return self._execute_send(receiver, json.dumps(message), priority=priority)

    def receive_message(self, queue_name):
        raw_message = self._execute_receive(queue_name)
        message = json.loads(raw_message)
        return message["content"]
