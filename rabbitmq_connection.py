import pika
from pika import PlainCredentials

class RabbitMQConnection:
    def __init__(self, queue_name, message, rabbitmq_server, rabbitmq_username, rabbitmq_password):
        self.queue_name = queue_name
        self.message = message

        if not isinstance(self.queue_name, str):
            raise TypeError('queue_name must be a string')

        self.rabbitmq_server = rabbitmq_server
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password
        self.connection = None
        self.channel = None

    def open_connection(self):
        credentials = PlainCredentials(self.rabbitmq_username, self.rabbitmq_password)
        parameters = pika.ConnectionParameters(self.rabbitmq_server, credentials=credentials)
        self.connection = pika.SelectConnection(parameters, self.on_connection_open, stop_ioloop_on_close=False)

    def on_connection_open(self, unused_connection):
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.queue_declare(queue=self.queue_name, durable=True, exclusive=False, auto_delete=False)

        properties = pika.BasicProperties(content_type='text/plain', delivery_mode=1)
        
        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=self.message, properties=properties)
        except Exception as e:
            print(f"Failed to publish message: {e}")

    def close_connection(self):
        self.connection.close()

    def run(self):
        self.open_connection()
        self.connection.ioloop.start()

    def stop(self):
        self.connection.ioloop.stop()
