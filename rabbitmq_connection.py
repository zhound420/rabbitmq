
import pika
import logging


class RabbitMQConnection:
    def __init__(self, connection_params):
        self.connection_params = connection_params
        self.connection = None
        self.logger = logging.getLogger(__name__)

    def connect(self):
        # Enhanced error handling
        try:
            # Only establish a new connection if there isn't one already
            if not self.connection:
                self.connection = pika.SelectConnection(
                    self.connection_params,
                    on_open_callback=self.on_connected,
                    on_close_callback=self.on_close
                )
        except Exception as e:
            self.logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def close(self):
        # Enhanced error handling
        try:
            # Close the connection if it exists
            if self.connection:
                self.connection.close()
                self.connection = None
        except Exception as e:
            self.logger.error(f"Failed to close the RabbitMQ connection: {e}")
            raise

    ...

    def on_message(self, channel, method, properties, body):
        # Call the callback function with the message body
        self.callback(body)

        # Send an acknowledgement
        # Note: The callback function should handle any exceptions and 
        #       only return if the message has been successfully processed
        channel.basic_ack(delivery_tag=method.delivery_tag)