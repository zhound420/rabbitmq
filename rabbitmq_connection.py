
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from superagi.tools.base_tool import BaseTool

class RabbitMQConnection:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        rabbitmq_server = self.get_tool_config('RABBITMQ_SERVER')
        rabbitmq_username = self.get_tool_config('RABBITMQ_USERNAME')
        rabbitmq_password = self.get_tool_config('RABBITMQ_PASSWORD')

        connection_params = ConnectionParameters(
            host=rabbitmq_server,
            credentials=PlainCredentials(rabbitmq_username, rabbitmq_password)
        )
        self.connection = BlockingConnection(connection_params)
        self.channel = self.connection.channel()

    def send_message(self, queue_name, message, persistent, priority):
        properties = pika.BasicProperties(delivery_mode=persistent, priority=priority)
        self.channel.basic_publish(
            exchange='', routing_key=queue_name, body=message, properties=properties
        )

    def receive_message(self, queue_name):
        method_frame, header_frame, body = self.channel.basic_get(queue_name)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            return body
        else:
            return None