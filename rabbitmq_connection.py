
import pika
from pika import PlainCredentials

class RabbitMQConnection:
    def __init__(self, queue_name, message, rabbitmq_server, rabbitmq_username, rabbitmq_password):
        self.queue_name = queue_name
        self.message = message
        self.rabbitmq_server = rabbitmq_server
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password

        if not isinstance(self.queue_name, str):
            raise TypeError('queue_name must be a string')

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