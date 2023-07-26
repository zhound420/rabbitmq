
from pydantic import BaseModel, Field


class RabbitMQToolInput(BaseModel):
    operation: str = Field(...)
    queue_name: str = Field(...)
    message: str = Field(None)