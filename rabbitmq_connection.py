
import os
import pika

class RabbitMQConnection:
    def __init__(self):
        self.server = os.getenv('RABBITMQ_SERVER', 'localhost')
        self.username = os.getenv('RABBITMQ_USERNAME', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')

    def send_message(self, queue_name, message, persistent, priority):
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.server, credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=persistent,  # make message persistent
                                  priority=priority
                              ))
        connection.close()

    def receive_message(self, queue_name):
        credentials = pika.PlainCredentials(self.username, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.server, credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)

        method_frame, header_frame, body = channel.basic_get(queue=queue_name)
        if method_frame:
            channel.basic_ack(method_frame.delivery_tag)
            return body.decode()
        else:
            return None