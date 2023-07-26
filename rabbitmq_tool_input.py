
from typing import Optional
from pydantic import BaseModel

class RabbitMQToolInput(BaseModel):
    action: str
    queue_name: str
    message: Optional[str]