import pika
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

class RabbitMQConnection:
    def __init__(self, server: str, username: str, password: str):
        self.server = server
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = PlainCredentials(self.username, self.password)
        parameters = ConnectionParameters(self.server, credentials=credentials)
        self.connection = BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def send_message(self, queue_name, message, persistent, priority):
        # Declare the queue before sending a message
        self.channel.queue_declare(queue=queue_name, durable=True)
        properties = pika.BasicProperties(delivery_mode=persistent, priority=priority)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message, properties=properties)

    def receive_message(self, queue_name):
        # Declare the queue before receiving a message
        self.channel.queue_declare(queue=queue_name, durable=True)
        method_frame, header_frame, body = self.channel.basic_get(queue_name)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return body.decode()
        else:
            return None