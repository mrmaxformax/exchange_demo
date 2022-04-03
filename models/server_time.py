from pydantic import BaseModel


class ServerTime(BaseModel):
    unixtime: int
    rfc1123: str
