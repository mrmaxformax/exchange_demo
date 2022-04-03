from pydantic import BaseModel
from typing import List, Optional, Dict


class Description(BaseModel):
    pair: str
    type: str
    ordertype: str
    price: str
    price2: str
    leverage: str
    order: str
    close: str


class OpenOrder(BaseModel):
    refid: Optional[str]
    userref: int
    status: str
    opentm: float
    starttm: int
    expiretm: int
    descr: Description
    vol: str
    vol_exec: str
    cost: str
    fee: str
    price: str
    stopprice: str
    limitprice: str
    misc: str
    oflags: str
    trades: List[str]


class OpenOrderResponse(BaseModel):
    open: Optional[Dict[str, OpenOrder]]