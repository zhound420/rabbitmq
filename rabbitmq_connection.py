import pika

class RabbitMQConnection:
    def __init__(self, server, username, password):
        self.credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(server, credentials=self.credentials)
        self.connection = None
        self.channel = None

    def open_connection(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def send_message(self, queue_name, message, persistent, priority):
        self.channel.queue_declare(queue=queue_name, durable=True)
        properties = pika.BasicProperties(delivery_mode=persistent, priority=priority)
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message, properties=properties)

    def receive_message(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)
        method_frame, header_frame, body = self.channel.basic_get(queue_name)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return body.decode('utf-8')
        else:
            return None