from superagi.tools.rabbitmq.rabbitmq_toolkit import RabbitMQTool

# Create an instance of the class
tool = RabbitMQTool(BaseTool)

# Check that the attributes are correctly initialized
assert tool.rabbitmq_server == 'localhost', f'Expected rabbitmq_server to be localhost, but got {tool.rabbitmq_server}'
assert tool.rabbitmq_username == 'guest', f'Expected rabbitmq_username to be guest, but got {tool.rabbitmq_username}'
assert tool.rabbitmq_password == 'guest', f'Expected rabbitmq_password to be guest, but got {tool.rabbitmq_password}'

print('All attributes are correctly initialized!')
