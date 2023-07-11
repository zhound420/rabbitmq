from superagi.tools.rabbitmq.rabbitmq_tool import RabbitMQTool
from superagi.helper.tool_helper import Operation, RabbitMQConfig

config = RabbitMQConfig(rabbitmq_server='localhost', rabbitmq_username='guest', rabbitmq_password='guest', queue_name='hello', message='Hello World!')
tool = RabbitMQTool(config=config, operation_type=Operation.SEND_MESSAGE)
tool.run_operation(operation_type=Operation.SEND_MESSAGE, input=None)
