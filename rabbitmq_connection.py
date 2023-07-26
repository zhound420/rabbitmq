
from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from pika.exceptions import AMQPConnectionError, AMQPChannelError
import logging
from abc import ABC
from pydantic import BaseModel
from superagi.tools.base_tool import BaseTool
import json
from typing import Any


class RabbitMQConnection(BaseTool, BaseModel, ABC):
    logger: Any
    connection_params: Any
    operation: str
    queue_name: str
    message: Optional[str] = None

    def __init__(self, connection_params, operation, queue_name, message=None, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.connection_params = connection_params
        self.operation = operation
        self.queue_name = queue_name
        self.message = message
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        self.logger.debug("Creating a new RabbitMQ connection.")
        try:
            self.connection = BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            self.logger.debug("RabbitMQ connection established.")
        except (AMQPConnectionError, AMQPChannelError) as e:
            self.logger.error("Failed to connect to RabbitMQ.", exc_info=True)

    def send(self):
        self.logger.debug(f"Sending message: {self.message}")
        if self.channel is None:
            self.logger.error("Cannot send message. Channel is None.")
            return
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=self.message)
        self.logger.debug("Message sent.")

    def receive(self):
        self.logger.debug(f"Receiving message from queue: {self.queue_name}")
        if self.channel is None:
            self.logger.error("Cannot receive message. Channel is None.")
            return
        method_frame, header_frame, body = self.channel.basic_get(queue=self.queue_name)
        if method_frame:
            self.logger.debug(f"Received message: {body}")
            self.channel.basic_ack(method_frame.delivery_tag)
            return body.decode('utf-8')
        else:
            self.logger.debug("No message received.")
            return None