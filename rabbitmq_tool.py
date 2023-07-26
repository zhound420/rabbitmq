

from pydantic import BaseModel, Field
from superagi.common.base_tool import BaseTool
from superagi.tools.rabbitmq.rabbitmq_connection import RabbitMQConnection
from superagi.tools.rabbitmq.rabbitmq_tool_input import RabbitMQToolInput
import pika

class RabbitMQTool(BaseModel, BaseTool):
    name: str = Field("RabbitMQ-SuperAGI Tool")
    rabbitmq_server: str = Field("localhost")
    rabbitmq_username: str = Field("guest")
    rabbitmq_password: str = Field("guest")
    agent_name: str = Field("test_agent_name")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection = RabbitMQConnection(
            rabbitmq_server=self.rabbitmq_server,
            rabbitmq_username=self.rabbitmq_username,
            rabbitmq_password=self.rabbitmq_password,
        )

    def _execute(self, tool_input: RabbitMQToolInput):
        operation = tool_input.operation
        if operation == 'send_message':
            receiver = tool_input.receiver
            message = tool_input.message
            self.connection.send_message(receiver, message)
        elif operation == 'receive_message':
            sender = tool_input.sender
            return self.connection.receive_message(sender)

    def send_message(self, queue_name, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_server))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        logger.info(f"[x] Sent {message}")

        connection.close()

    def receive_message(self, queue_name):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_server))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        def callback(ch, method, properties, body):
            logger.info(f"[x] Received {body}")

        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        logger.info('[*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()