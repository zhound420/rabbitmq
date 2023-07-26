from superagi.tools.rabbitmq.rabbitmq_tool import RabbitMQTool
from superagi.agent.super_agi import SuperAgi

# Create an instance of SuperAgi with your desired AI name
superagi_instance = SuperAgi(ai_name='agent_name')

# You should provide a valid configuration object for RabbitMQTool
config = {
    'name': 'RabbitMQ-SuperAGI Tool',
    'rabbitmq_server': 'localhost',
    'rabbitmq_username': 'guest',
    'rabbitmq_password': 'guest',
}

tool = RabbitMQTool(superagi_instance.ai_name, **config)
tool._execute(tool_input={"operation": "send_message", "receiver": "hello", "message": "Hello World!"})
