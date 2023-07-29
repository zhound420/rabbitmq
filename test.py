from pika import BlockingConnection, ConnectionParameters, PlainCredentials
import os

def test_connection():
    # Retrieve RabbitMQ server details from environment variables
    rabbitmq_server = os.getenv('RABBITMQ_SERVER', 'localhost')
    rabbitmq_username = os.getenv('RABBITMQ_USERNAME', 'guest')
    rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

    # Set up the connection parameters
    connection_params = ConnectionParameters(
        host=rabbitmq_server,
        credentials=PlainCredentials(rabbitmq_username, rabbitmq_password)
    )

    # Test the connection to the RabbitMQ server
    try:
        connection = BlockingConnection(connection_params)
        connection.close()
        print("Connection to RabbitMQ server successful.")
    except Exception as e:
        print(f"Failed to connect to RabbitMQ server: {e}")

if __name__ == '__main__':
    test_connection()
