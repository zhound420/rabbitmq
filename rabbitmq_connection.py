# rabbitmq_connection.py

import pika
import logging

class RabbitMQConnection:
    def __init__(self, connection_params, action, queue_name=None, message=None, persistent=False, priority=0, callback=None, consumer_tag=None, delivery_tag=None):
        self.connection_params = connection_params
        self.action = action
        self.queue_name = queue_name
        self.message = message
        self.persistent = persistent
        self.priority = priority
        self.callback = callback
        self.consumer_tag = consumer_tag
        self.delivery_tag = delivery_tag
        self.channel = None
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def on_connected(self, connection):
        self.connection = connection
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        # Declare the queue before performing actions
        self.channel.queue_declare(queue=self.queue_name, durable=True, exclusive=False, auto_delete=False)
        if self.action == 'add_consumer':
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        elif self.action == 'remove_consumer':
            self.channel.basic_cancel(self.consumer_tag)
        elif self.action == 'send_ack':
            self.channel.basic_ack(self
