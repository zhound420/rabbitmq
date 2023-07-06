from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool
import pika
import os
import logging
import datetime
import json


class RabbitMQConnection:
    def __init__(self, connection_params, action, queue_name, message, persistent, priority, callback=None, consumer_tag=None, delivery_tag=None):
        self.connection_params = connection_params
        self.action = action
        self.queue_name = queue_name
        self.message = message
        self.persistent = persistent
        self.priority = priority
        self.callback = callback
        self.consumer_tag = consumer_tag
        self.delivery_tag = delivery_tag
        self.logger = logging.getLogger(__name__)

    def on_connected(self, connection):
        if self.action == 'add_consumer':
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        elif self.action == 'remove_consumer':
            self.channel.basic_cancel(self.consumer_tag)
        elif self.action == 'send_ack':
            self.channel.basic_ack(self.delivery_tag)
        elif self.action == 'send':
            properties = pika.BasicProperties(priority=self.priority)
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=self.message, properties=properties)
        # ... rest of the method ...

    def on_message(self, channel, method, properties, body):
        # Call the callback function with the message body
        self.callback(body)

        # Send an acknowledgement
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def on_closed(self, connection, reason):
        if isinstance(reason, pika.exceptions.AMQPConnectionError):
            self.logger.error('Failed to connect to RabbitMQ')
        elif isinstance(reason, pika.exceptions.AMQPChannelError):
            self.logger.error('An error occurred with the channel')
        # ... rest of the method ...

    def run(self):
        self.connection = pika.SelectConnection(
            self.connection_params,
            on_open_callback=self.on_connected,
            on_close_callback=self.on_close
        )
        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.connection.close()
            self.connection.ioloop.start()


class RabbitMQTool(BaseTool, ABC):
    name = "RabbitMQ Tool"
    description = "A tool for interacting with RabbitMQ"

    def __init__(self):
        self.rabbitmq_server = os.getenv('RABBITMQ_SERVER', 'localhost')
        self.rabbitmq_username = os.getenv('RABBITMQ_USERNAME', 'guest')
        self.rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.connection_params = pika.ConnectionParameters(
            host=self.rabbitmq_server,
            credentials=pika.PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        )
        self.logger = logging.getLogger(__name__)

    def execute(self, action, queue_name, message=None, persistent=False, priority=0, callback=None, consumer_tag=None, delivery_tag=None):
        """
        Execute a RabbitMQ operation.
        
        The operation can be either "send", "receive", "create_queue", "delete_queue", "add_consumer", "remove_consumer", or "send_ack". 
        """
        connection = RabbitMQConnection(self.connection_params, action, queue_name, message, persistent, priority, callback, consumer_tag, delivery_tag)
        connection.run()

    def send_natural_language_message(self, receiver, content, msg_type="text", priority=0):
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
        self.execute("send", receiver, json.dumps(message), priority=priority)

    def receive_natural_language_message(self, queue_name):
        """
        Receive a natural language message from a specified queue.
        """
        raw_message = self.execute("receive", queue_name)
        message = json.loads(raw_message)
        return message["content"]
