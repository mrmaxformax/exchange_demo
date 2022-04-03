import uuid

from pydantic import BaseModel
from typing import List, Optional, Dict

from pydantic.validators import UUID


class OpenOrderDemo(BaseModel):
    order_id: UUID
    symbol: str
    side: str
    orderType: str
    limitPrice: int
    stopPrice: int
    unfilledSize: int
    receivedTime: str
    status: str
    filledSize: int
    reduceOnly: bool
    triggerSignal: str
    lastUpdateTime: str

class OpenOrderDemoResponse(BaseModel):
    result: str
    openOrders: List[OpenOrderDemo]
    serverTime: str
