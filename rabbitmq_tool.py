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
    connection_params: Any
    logger: Any

    name: str = "RabbitMQTool"
    description: str = "Tool that contains various operations to interact with RabbitMQ"

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

    def _execute_create_queue(self, queue_name):
        """
        Execute a RabbitMQ create_queue operation.
        """
        connection = RabbitMQConnection(self.connection_params, "create_queue", queue_name)
        return connection.run()

    def _execute_delete_queue(self, queue_name):
        """
        Execute a RabbitMQ delete_queue operation.
        """
        connection = RabbitMQConnection(self.connection_params, "delete_queue", queue_name)
        return connection.run()

    def _execute_add_consumer(self, queue_name, callback=None):
        """
        Execute a RabbitMQ add_consumer operation.
        """
        connection = RabbitMQConnection(self.connection_params, "add_consumer", queue_name, callback=callback)
        return connection.run()

    def _execute_remove_consumer(self, queue_name, consumer_tag=None):
        """
        Execute a RabbitMQ remove_consumer operation.
        """
        connection = RabbitMQConnection(self.connection_params, "remove_consumer", queue_name, consumer_tag=consumer_tag)
        return connection.run()

    def _execute_send_ack(self, queue_name, delivery_tag=None):
        """
        Execute a RabbitMQ send_ack operation.
        """
        connection = RabbitMQConnection(self.connection_params, "send_ack", queue_name, delivery_tag=delivery_tag)
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

    def create_queue(self, queue_name):
        """
        Create a queue.
        """
        return self._execute_create_queue(queue_name)

    def delete_queue(self, queue_name):
        """
        Delete a queue.
        """
        return self._execute_delete_queue(queue_name)

    def add_consumer(self, queue_name, callback=None):
        """
        Add a consumer.
        """
        return self._execute_add_consumer(queue_name, callback=callback)

    def remove_consumer(self, queue_name, consumer_tag=None):
        """
        Remove a consumer.
        """
        return self._execute_remove_consumer(queue_name, consumer_tag=consumer_tag)

    def send_ack(self, queue_name, delivery_tag=None):
        """
        Send an acknowledgement.
        """
        return self._execute_send_ack(queue_name, delivery_tag=delivery_tag)
