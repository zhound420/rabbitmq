import os
from superagi.tools.rabbitmq.rabbitmq_tool import RabbitMQTool, RabbitMQConfig

# Retrieve the values from environment variables
rabbitmq_server = os.getenv('RABBITMQ_SERVER', 'localhost')
rabbitmq_username = os.getenv('RABBITMQ_USERNAME', 'guest')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

# Create a RabbitMQConfig instance
config = RabbitMQConfig(rabbitmq_server=rabbitmq_server,
                        rabbitmq_username=rabbitmq_username,
                        rabbitmq_password=rabbitmq_password)

# Create an instance of the class
tool = RabbitMQTool(config)

# Check that the attributes are correctly initialized
assert tool.config.rabbitmq_server == rabbitmq_server, f'Expected rabbitmq_server to be {rabbitmq_server}, but got {tool.config.rabbitmq_server}'
assert tool.config.rabbitmq_username == rabbitmq_username, f'Expected rabbitmq_username to be {rabbitmq_username}, but got {tool.config.rabbitmq_username}'
assert tool.config.rabbitmq_password == rabbitmq_password, f'Expected rabbitmq_password to be {rabbitmq_password}, but got {tool.config.rabbitmq_password}'
print('All attributes are correctly initialized!')
