from superagi.tools.rabbitmq.rabbitmq_tool import RabbitMQTool

# You should provide a valid configuration object for RabbitMQTool
config = {
    'rabbitmq_server': 'localhost',
    'rabbitmq_username': 'guest',
    'rabbitmq_password': 'guest',
    'queue_name': 'hello',
    'message': 'Hello World!'
}
tool = RabbitMQTool(config=config, operation_type="send_message")
tool._execute(tool_input={"operation": "send_message"})
