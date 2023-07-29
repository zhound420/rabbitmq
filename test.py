
from rabbitmq_toolkit import RabbitMQToolkit

def test_send_and_receive():
    toolkit = RabbitMQToolkit()
    send_tool = toolkit.get_tools()[0]
    receive_tool = toolkit.get_tools()[1]

    # Send a test message
    send_tool._execute('test_queue', 'Hello, world!', 2, 0)

    # Receive the test message
    message = receive_tool._execute('test_queue')

    # Check that the received message matches the sent message
    assert message == 'Hello, world!', f"Expected 'Hello, world!', but got {message}"

if __name__ == "__main__":
    test_send_and_receive()