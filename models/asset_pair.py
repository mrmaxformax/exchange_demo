from pydantic import BaseModel
from typing import List, Union


class AssetPair(BaseModel):
    altname: str
    wsname: str
    aclass_base: str
    base: str
    aclass_quote: str
    quote: str
    lot: str
    pair_decimals: int
    lot_decimals: int
    lot_multiplier: int
    leverage_buy: List[int]
    leverage_sell: List[int]
    fees: List[List[Union[int, float]]]
    fees_maker: List[List[Union[int, float]]]
    fee_volume_currency: str
    margin_call: int
    margin_stop: int
    ordermin: str
