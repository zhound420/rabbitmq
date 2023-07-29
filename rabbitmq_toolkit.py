
from typing import List, Type
from superagi.tools.base_tool import BaseTool, BaseToolkit
from rabbitmq_send_tool import RabbitMQSendTool
from rabbitmq_receive_tool import RabbitMQReceiveTool

class RabbitMQToolkit(BaseToolkit):
    name: str = "RabbitMQ Toolkit"
    description: str = "A toolkit for communicating with a RabbitMQ server"

    def get_tools(self) -> List[Type[BaseTool]]:
        return [RabbitMQSendTool(), RabbitMQReceiveTool()]

    def get_env_keys(self) -> List[str]:
        return ['RABBITMQ_SERVER', 'RABBITMQ_USERNAME', 'RABBITMQ_PASSWORD']