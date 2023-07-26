
import pika
import logging

class RabbitMQConnection:
    def __init__(self, connection_params, operation, queue_name, message=None):
        self.connection_params = connection_params
        self.operation = operation
        self.queue_name = queue_name
        self.message = message
        self.logger = logging.getLogger(__name__)
        self.connection = None
        self.channel = None

    def __enter__(self):
        try:
            self.logger.debug("Establishing RabbitMQ connection.")
            self.connection = pika.BlockingConnection(self.connection_params)
            self.channel = self.connection.channel()
            self.logger.debug("RabbitMQ connection established.")
        except pika.exceptions.AMQPConnectionError as error:
            self.logger.error(f"Error establishing RabbitMQ connection: {error}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            self.logger.debug("Closing RabbitMQ connection.")
            self.connection.close()

    def send(self):
        if self.channel is not None:
            self.logger.debug("Sending message.")
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=self.message,
                properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
            )
            self.logger.debug("Message sent.")
        else:
            self.logger.error("Cannot send message. Channel is None.")
        return self.message

    def receive(self):
        if self.channel is not None:
            self.logger.debug("Receiving message.")
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            method_frame, properties, body = self.channel.basic_get(queue=self.queue_name, auto_ack=True)
            self.logger.debug("Message received.")
            if method_frame:
                return body.decode()
        else:
            self.logger.error("Cannot receive message. Channel is None.")
        return None