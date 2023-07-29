
from typing import Optional
from pydantic import BaseModel
from superagr.superclasses.superagent import SuperAgent, SuperAgentConfig
from superagr.superclasses.superagent import AgentConnection as SuperAgentConnection
from superagr.superclasses.superagent import AgentMessage as SuperAgentMessage
import pika
from pika import PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel


class RabbitMQConnection(SuperAgentConnection):
    connection: Optional[pika.BlockingConnection] = None
    channel: Optional[BlockingChannel] = None

    def __init__(self, connection_params):
        credentials = PlainCredentials(connection_params.username, connection_params.password)
        parameters = pika.ConnectionParameters(connection_params.host,
                                               connection_params.port,
                                               '/',
                                               credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def __del__(self):
        if self.connection:
            self.connection.close()


class RabbitMQMessage(SuperAgentMessage):
    pass


class RabbitMQConfig(SuperAgentConfig):
    host: str
    port: str
    username: str
    password: str


class RabbitMQAgent(SuperAgent):
    config: RabbitMQConfig
    connection: RabbitMQConnection
    message: Optional[RabbitMQMessage] = None

    def __init__(self, config: RabbitMQConfig, name: str, description: str):
        super().__init__(name=name, description=description)
        self.config = config
        self.connection = RabbitMQConnection(self.config)

    def __del__(self):
        if hasattr(self, 'connection'):
            del self.connection
