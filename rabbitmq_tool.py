import json
import os
import pika
import logging
from pydantic import BaseModel
from pika.exceptions import AMQPConnectionError, AMQPChannelError
from superagi.tools.rabbitmq.rabbitmq_connection import RabbitMQConnection
from superagi.tools.base_tool import BaseTool

class RabbitMQConfig(BaseModel):
    rabbitmq_server: str = os.getenv("RABBITMQ_HOST", "host.docker.internal")
    rabbitmq_username: str = os.getenv("RABBITMQ_USERNAME", "guest")
    rabbitmq_password: str = os.getenv("RABBITMQ_PASSWORD", "guest")

class RabbitMQTool(BaseTool):
    def __init__(self, config: RabbitMQConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def build_connection_params(self):
        credentials = pika.PlainCredentials(self.config.rabbitmq_username, self.config.rabbitmq_password)
        connection_params = pika.ConnectionParameters(host=self.config.rabbitmq_server, credentials=credentials)
        return connection_params

    def parse_tool_input(self, tool_input):
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                tool_input = {"operation": "send_message", "receiver": "Linda", "message": tool_input}
        return tool_input

    def _execute(self, *args, **kwargs):
        tool_input = self.parse_tool_input(kwargs.get("tool_input", {}))
        operation = tool_input.get("operation")

        if operation not in ["send_message", "receive_message", "publish_message"]:
            raise ValueError(f"Unknown operation: '{operation}'")

        if operation == "send_message":
            receiver = tool_input.get("receiver")
            message = tool_input.get("message")
            if not receiver or not isinstance(receiver, str):
                raise ValueError("Invalid receiver.")
            if not message or not isinstance(message, str):
                raise ValueError("Invalid message.")
            return self._execute_send(receiver, message)
        
        elif operation == "receive_message":
            queue_name = tool_input.get("queue_name")
            if not queue_name or not isinstance(queue_name, str):
                raise ValueError("Invalid queue name.")
            return self._execute_receive(queue_name)
        
        elif operation == "publish_message":
            exchange = tool_input.get("exchange")
            routing_key = tool_input.get("routing_key")
            message = tool_input.get("message")
            if not exchange or not isinstance(exchange, str):
                raise ValueError("Invalid exchange.")
            if not routing_key or not isinstance(routing_key, str):
                raise ValueError("Invalid routing key.")
            if not message or not isinstance(message, str):
                raise ValueError("Invalid message.")
            return self._execute_publish(exchange, routing_key, message)

    # ... other methods follow ...
