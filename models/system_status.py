from pydantic import BaseModel


class SystemStatus(BaseModel):
    status: str
    timestamp: str
