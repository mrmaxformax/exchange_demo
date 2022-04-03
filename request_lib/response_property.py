from dataclasses import dataclass, field
from json import JSONDecodeError
from typing import Optional
from requests import Response

from utilities.logging import LOG


@dataclass
class ResponseProperty:
    status_code: int
    response: Response
    response_time: float
    response_json: Optional[dict] = field(init=False)
    exception: Optional[Exception] = None

    def __post_init__(self):
        try:
            self.response_json = self.response.json()
        except JSONDecodeError as err:
            LOG.info(err.msg)
            self.response_json = None
        except TypeError as err:
            LOG.info(err)
            self.response_json = None
