
from typing import Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod

class RabbitMQToolInput(BaseModel):
    operation: Optional[str]
    receiver: Optional[str]
    message: Optional[str]

class RabbitMQConnection(ABC, BaseModel):
    name: str
    rabbitmq_server: str
    rabbitmq_username: str
    rabbitmq_password: str
    agent_name: Optional[str] = None

    @abstractmethod
    def connect(self):
        pass

class RabbitMQTool(RabbitMQConnection):
    def __init__(self, **data):
        super().__init__(**data)
        self.connect()

    def _execute(self, tool_input: RabbitMQToolInput):
        operation = tool_input.operation
        receiver = tool_input.receiver
        message = tool_input.message

        if operation == 'send_message':
            self.send_message(receiver, message)
        elif operation == 'receive_message':
            self.receive_message(receiver)
        else:
            raise ValueError(f"Invalid operation {operation}")

    def connect(self):
        print(f"Connecting to RabbitMQ server at {self.rabbitmq_server}...")

    def send_message(self, receiver, message):
        print(f"Sending message {message} to {receiver}...")

    def receive_message(self, receiver):
        print(f"Receiving message from {receiver}...")
        