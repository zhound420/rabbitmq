from abc import ABC
from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from rabbitmq_connection import RabbitMQConnection
import json
import datetime

class BaseRabbitMQTool(BaseTool, ABC):
    """
    Base class for RabbitMQ tools. All RabbitMQ tools should inherit from this class.
    """
    connection_params: Any
    logger: Any

    def _execute(self, action, queue_name, message=None, persistent=False, priority=0, callback=None, consumer_tag=None, delivery_tag=None):
        """
        Execute a RabbitMQ operation.
        """
        connection = RabbitMQConnection(self.connection_params, action, queue_name, message, persistent, priority, callback, consumer_tag, delivery_tag)
        return connection.run()

class SendMessageTool(BaseRabbitMQTool):
    """
    Tool for sending a message.
    """
    name: str = "Send Message Tool"
    description: str = "Tool for sending a message via RabbitMQ"

    def send_message(self, receiver, content, msg_type="text", priority=0):
        message = {
            "sender": self.name,
            "receiver": receiver,
            "timestamp": datetime.datetime.now().isoformat(),
            "type": msg_type,
            "content": content
        }
        return self._execute("send", receiver, json.dumps(message), priority=priority)

class ReceiveMessageTool(BaseRabbitMQTool):
    """
    Tool for receiving a message.
    """
    name: str = "Receive Message Tool"
    description: str = "Tool for receiving a message via RabbitMQ"

    def receive_message(self, queue_name):
        raw_message = self._execute("receive", queue_name)
        message = json.loads(raw_message)
        return message["content"]

class CreateQueueTool(BaseRabbitMQTool):
    """
    Tool for creating a queue.
    """
    name: str = "Create Queue Tool"
    description: str = "Tool for creating a queue via RabbitMQ"

    def create_queue(self, queue_name):
        return self._execute("create_queue", queue_name)

class DeleteQueueTool(BaseRabbitMQTool):
    """
    Tool for deleting a queue.
    """
    name: str = "Delete Queue Tool"
    description: str = "Tool for deleting a queue via RabbitMQ"

    def delete_queue(self, queue_name):
        return self._execute("delete_queue", queue_name)

class AddConsumerTool(BaseRabbitMQTool):
    """
    Tool for adding a consumer.
    """
    name: str = "Add Consumer Tool"
    description: str = "Tool for adding a consumer via RabbitMQ"

    def add_consumer(self, queue_name, callback=None):
        return self._execute("add_consumer", queue_name, callback=callback)

class RemoveConsumerTool(BaseRabbitMQTool):
    """
    Tool for removing a consumer.
    """
    name: str = "Remove Consumer Tool"
    description: str = "Tool for removing a consumer via RabbitMQ"

    def remove_consumer(self, queue_name, consumer_tag=None):
        return self._execute("remove_consumer", queue_name, consumer_tag=consumer_tag)

class SendAckTool(BaseRabbitMQTool):
    """
    Tool for sending an acknowledgement.
    """
    name: str = "Send Acknowledgement Tool"
    description: str = "Tool for sending an acknowledgement via RabbitMQ"

    def send_ack(self, queue_name, delivery_tag=None):
        return self._execute("send_ack", queue_name, delivery_tag=delivery_tag)
