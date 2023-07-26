from rabbitmq_tool import RabbitMQTool, RabbitMQToolInput

# You should provide a valid configuration object for RabbitMQTool
config = {
    'name': 'RabbitMQ-SuperAGI Tool',
    'rabbitmq_server': '192.168.4.194',
    'rabbitmq_username': 'guest',
    'rabbitmq_password': 'guest',
    'agent_name': 'test_agent_name',  # Define your agent name directly
}

tool = RabbitMQTool(**config)
tool_input = RabbitMQToolInput(operation="send_message", receiver="hello", message="Hello World!")
tool._execute(tool_input=tool_input)
