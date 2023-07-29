
from superagi.tools.base_tool import BaseToolkit
from rabbitmq_send_tool import RabbitMQSendTool
from rabbitmq_receive_tool import RabbitMQReceiveTool

class RabbitMQToolkit(BaseToolkit):
    def get_tools(self):
        return [RabbitMQSendTool(), RabbitMQReceiveTool()]

    def get_env_keys(self):
        return ["RABBITMQ_SERVER", "RABBITMQ_USERNAME", "RABBITMQ_PASSWORD"]