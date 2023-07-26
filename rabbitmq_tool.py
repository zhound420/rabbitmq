from pika import PlainCredentials
from pika.exceptions import AMQPConnectionError, AMQPChannelError
import os
import json
import datetime
import pika
import logging
from abc import ABC
from typing import Type, Optional, Any
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from superagi.agent.super_agi import SuperAgi
from rabbitmq_connection import RabbitMQConnection

class RabbitMQTool(BaseTool, BaseModel):
    logger: Any
    name: str  
    description: str = "Tool that contains various operations to interact with RabbitMQ"
    agent_name: str = Field(default_factory=lambda: os.getenv('ai_name', 'superagi'))

    rabbitmq_server: str = Field(default_factory=lambda: os.getenv('RABBITMQ_SERVER', 'localhost'))
    rabbitmq_username: str = Field(default_factory=lambda: os.getenv('RABBITMQ_USERNAME', 'guest'))
    rabbitmq_password: str = Field(default_factory=lambda: os.getenv('RABBITMQ_PASSWORD', 'guest'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)

    def _execute(self, *args, agent_name: str = None, **kwargs):
        action_mapping = {
            "send_message": self._execute_send,
            "send": self._execute_send,
            "transmit": self._execute_send,
            "dispatch": self._execute_send,
            "receive_message": self._execute_receive,
            "receive": self._execute_receive,
            "fetch": self._execute_receive,
            "get": self._execute_receive,
        }

        tool_input = kwargs.get("tool_input", {})
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                tool_input = {"action": "send_message", "queue_name": self.agent_name, "message": tool_input}
        else:
            if "queue_name" not in tool_input or tool_input["queue_name"] is None:
                tool_input["queue_name"] = agent_name if agent_name is not None else self.agent_name

        tool_input["action"] = tool_input.get("action", "send_message")

        action = tool_input.get("action")
        mapped_action = action_mapping.get(action)
        if callable(mapped_action):
            queue_name = tool_input.get("queue_name")
            message = tool_input.get("message")
            return mapped_action(queue_name, message)
        else:
            raise ValueError(f"Unknown action: '{action}'")

    def _execute_send(self, queue_name, message):
        connection_params = self.build_connection_params()
        conn = RabbitMQConnection(connection_params, 'send', queue_name, message)
        return conn.send()

    def _execute_receive(self, queue_name):
        connection_params = self.build_connection_params()
        conn = RabbitMQConnection(connection_params, 'receive', queue_name)
        return conn.receive()

    def build_connection_params(self):
        self.logger.debug("Building connection params.")
        credentials = pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        self.logger.debug("Connection params built.")
        return pika.ConnectionParameters(host=self.rabbitmq_server, credentials=credentials)

    def send_message(self, message, msg_type="text", priority=0, queue_name=None):
        queue_name = queue_name or self.agent_name
        message = {
            "sender": self.agent_name,
            "receiver": queue_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": message
        }
        return self._execute_send(queue_name, json.dumps(message))

    def receive_message(self, queue_name=None):
        queue_name = queue_name or self.agent_name
        raw_message = self._execute_receive(queue_name)
        if raw_message:
            message = json.loads(raw_message)
            return message["content"]
        return None
