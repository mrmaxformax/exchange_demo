from pydantic import BaseModel


class Asset(BaseModel):
    aclass: str
    altname: str
    decimals: int
    display_decimals: int
