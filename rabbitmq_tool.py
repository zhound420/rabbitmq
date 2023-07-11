import json
import os
import pika
import logging
from pika.exceptions import AMQPConnectionError, AMQPChannelError
from superagi.tools.rabbitmq.rabbitmq_connection import RabbitMQConnection
from superagi.tools.base_tool import BaseTool

class RabbitMQTool(BaseTool):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def build_connection_params(self):
        credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USERNAME", "guest"), os.getenv("RABBITMQ_PASSWORD", "guest"))
        connection_params = pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "192.168.4.194"), credentials=credentials)
        return connection_params

    def _execute(self, *args, **kwargs):
        tool_input = kwargs.get("tool_input", {})
        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except json.JSONDecodeError:
                tool_input = {"operation": "send_message", "receiver": "Linda", "message": tool_input}

        operation = tool_input.get("operation")
        if operation == "send_message":
            receiver = tool_input.get("receiver")
            message = tool_input.get("message")
            return self._execute_send(receiver, message)
        elif operation == "receive_message":
            queue_name = tool_input.get("queue_name")
            return self._execute_receive(queue_name)
        elif operation == "publish_message":
            exchange = tool_input.get("exchange")
            routing_key = tool_input.get("routing_key")
            message = tool_input.get("message")
            return self._execute_publish(exchange, routing_key, message)
        else:
            raise ValueError(f"Unknown operation: '{operation}'")

    def _execute_send(self, receiver, message, persistent=False, priority=0):
        if not receiver or not isinstance(receiver, str):
            self.logger.error("Invalid receiver.")
            return None
        if not message or not isinstance(message, str):
            self.logger.error("Invalid message.")
            return None

        try:
            connection_params = self.build_connection_params()
            connection = RabbitMQConnection(connection_params, "send", queue_name=receiver, message=message, persistent=persistent, priority=priority)
            return connection.run()
        except (AMQPConnectionError, AMQPChannelError) as e:
            self.logger.error(f"Error while sending message: {str(e)}")
            return None

    def _execute_receive(self, queue_name):
        if not queue_name or not isinstance(queue_name, str):
            self.logger.error("Invalid queue name.")
            return None

        try:
            connection_params = self.build_connection_params()
            connection = RabbitMQConnection(connection_params, "receive", queue_name=queue_name)
            return connection.run()
        except (AMQPConnectionError, AMQPChannelError) as e:
            self.logger.error(f"Error while receiving message: {str(e)}")
            return None

    def _execute_publish(self, exchange, routing_key, message):
        if not exchange or not isinstance(exchange, str):
            self.logger.error("Invalid exchange.")
            return None
        if not routing_key or not isinstance(routing_key, str):
            self.logger.error("Invalid routing key.")
            return None
        if not message or not isinstance(message, str):
            self.logger.error("Invalid message.")
            return None

        try:
            connection_params = self.build_connection_params()
            connection = RabbitMQConnection(connection_params, "publish", exchange=exchange, routing_key=routing_key, message=message)
            return connection.run()
        except (AMQPConnectionError, AMQPChannelError) as e:
            self.logger.error(f"Error while publishing message: {str(e)}")
            return None
