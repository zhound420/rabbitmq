
import pika
import logging
from pika.exceptions import AMQPConnectionError, AMQPChannelError

class RabbitMQConnection:
    def __init__(self, connection_params, operation_type, queue_name=None, message=None, persistent=False, priority=0):
        self.connection_params = connection_params
        self.operation_type = operation_type
        self.queue_name = queue_name
        self.message = message
        self.persistent = persistent
        self.priority = priority
        self.logger = logging.getLogger(__name__)

    def send(self):
        with pika.BlockingConnection(self.connection_params) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name, durable=True)
            if self.persistent:
                properties = pika.BasicProperties(delivery_mode=2, priority=self.priority)
            else:
                properties = pika.BasicProperties(priority=self.priority)

            if isinstance(self.queue_name, bytes):
                self.queue_name = self.queue_name.decode()

            if not isinstance(self.queue_name, str):
                raise TypeError(f'Expected self.queue_name to be a string, but got {type(self.queue_name).__name__}')

            channel.basic_publish(exchange="", routing_key=self.queue_name, body=self.message, properties=properties)
            return "Message sent successfully."

    def receive(self):
        with pika.BlockingConnection(self.connection_params) as connection:
            channel = connection.channel()
            method_frame, header_frame, body = channel.basic_get(queue=self.queue_name, auto_ack=True)
            return body