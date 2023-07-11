
from pika import PlainCredentials, ConnectionParameters
from pika.exceptions import AMQPConnectionError, AMQPChannelError
import json
import logging
import pika

class RabbitMQConnection:
    def __init__(self, rabbitmq_username, rabbitmq_password, rabbitmq_server, operation_type, receiver=None, message=None, persistent=False, priority=0):
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password
        self.rabbitmq_server = rabbitmq_server
        self.connection_params = connection_params
        self.operation_type = operation_type
        self.queue_name = queue_name
        self.message = message
        self.persistent = persistent
        self.priority = priority
        self.logger = logging.getLogger(__name__)

    def _connect(self):
        self.logger.debug("Connecting to RabbitMQ.")
        connection = pika.BlockingConnection(self.connection_params)
        self.logger.debug("Connected.")
        return connection

    def _open_channel(self, connection):
        self.logger.debug("Opening channel.")
        channel = connection.channel()
        self.logger.debug("Channel opened.")
        return channel

    # rest of the code is the same

    def run(self):
        try:
            credentials = PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_server, credentials=credentials))
            channel = connection.channel()

            channel.queue_declare(queue=self.queue_name)

            # Enable delivery confirmations
            channel.confirm_delivery()

            if channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=self.message,
                properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
            ):
                print(f"[x] Sent {self.message}")
            else:
                print("Message not delivered")
                
            connection.close()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")
            return
