from superagi.tools.base_tool import BaseToolkit
from typing import List
from rabbitmq_send_tool import RabbitMQSendTool
from rabbitmq_receive_tool import RabbitMQReceiveTool
from superagi.agent.super_agi import SuperAGI


class RabbitMQToolkit(BaseToolkit):
    name: str = "RabbitMQ Toolkit"
    description: str = "A toolkit for sending and receiving messages using RabbitMQ."


    def get_tools(self) -> List:
        return [RabbitMQSendTool(), RabbitMQReceiveTool()]

    def get_env_keys(self) -> List[str]:
        return ["RABBITMQ_SERVER", "RABBITMQ_USERNAME", "RABBITMQ_PASSWORD"]
    