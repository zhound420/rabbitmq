
from superagi.tools.rabbitmq.rabbitmq_tool_input import RabbitMQToolInput
from superagi.tools.base_tool import BaseTool
import logging
import pika


class RabbitMQTool(BaseTool):
    def __init__(self, name: str, rabbitmq_server: str, rabbitmq_username: str, rabbitmq_password: str, agent_name: str = None):
        self.name = name
        self.rabbitmq_server = rabbitmq_server
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password
        self.agent_name = agent_name

    def _execute(self, tool_input: RabbitMQToolInput):
        operation = tool_input.operation
        queue_name = tool_input.queue_name if tool_input.queue_name is not None else self.agent_name
        message = tool_input.message

        if operation == "send_message":
            self.send_message(queue_name, message)
        elif operation == "receive_message":
            self.receive_message(queue_name)
        else:
            logger.error(f"Unsupported operation: {operation}")
            raise ValueError(f"Unsupported operation: {operation}")

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