from superagi.tools.rabbitmq.rabbitmq_tool import RabbitMQTool

# You should provide a valid configuration object for RabbitMQTool
config = {
    'name': 'RabbitMQ-SuperAGI Tool',
    'rabbitmq_server': 'localhost',
    'rabbitmq_username': 'guest',
    'rabbitmq_password': 'guest',
    'agent_name': 'my_agent_name',  # Define your agent name directly
}

tool = RabbitMQTool(**config)
tool._execute(tool_input={"operation": "send_message", "receiver": "hello", "message": "Hello World!"})
