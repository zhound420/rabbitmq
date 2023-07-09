from typing import Any
import os
import logging
import pika
import datetime
import json
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection

class RabbitMQTool(BaseTool):
    name = "RabbitMQ Tool"
    description = "A tool for interacting with RabbitMQ"
    rabbitmq_server: str = os.getenv('RABBITMQ_SERVER', 'localhost')
    rabbitmq_username: str = os.getenv('RABBITMQ_USERNAME', 'guest')
    rabbitmq_password: str = os.getenv('RABBITMQ_PASSWORD', 'guest')
    connection_params: Any
    logger: Any

    def _execute(self, action, queue_name, message=None, persistent=False, priority=0, callback=None, consumer_tag=None, delivery_tag=None):
        """
        Execute a RabbitMQ operation.
        
        The operation can be either "send", "receive", "create_queue", "delete_queue", "add_consumer", "remove_consumer", or "send_ack". 
        """
        connection = RabbitMQConnection(self.connection_params, action, queue_name, message, persistent, priority, callback, consumer_tag, delivery_tag)
        return connection.run()

    def send_message(self, receiver, content, msg_type="text", priority=0):
        """
        Send a natural language message to a specified queue (receiver).
        """
        message = {
            "sender": self.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": content
        }
        return self._execute("send", receiver, json.dumps(message), priority=priority)

    def receive_message(self, queue_name):
        """
        Receive a natural language message from a specified queue.
        """
        raw_message = self._execute("receive", queue_name)
        message = json.loads(raw_message)
        return message["content"]

    def create_queue(self, queue_name):
        """
        Create a new queue.
        """
        return self._execute("create_queue", queue_name)

    def delete_queue(self, queue_name):
        """
        Delete a specified queue.
        """
        return self._execute("delete_queue", queue_name)

    def add_consumer(self, queue_name, callback=None):
        """
        Add a consumer to a specified queue.
        """
        return self._execute("add_consumer", queue_name, callback=callback)

    def remove_consumer(self, queue_name, consumer_tag=None):
        """
        Remove a consumer from a specified queue.
        """
        return self._execute("remove_consumer", queue_name, consumer_tag=consumer_tag)

    def send_ack(self, queue_name, delivery_tag=None):
        """
        Send an acknowledgement for a specified queue.
        """
        return self._execute("send_ack", queue_name, delivery_tag=delivery_tag)
