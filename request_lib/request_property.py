from dataclasses import dataclass
from re import sub
from typing import Optional, Union


@dataclass
class RequestProperty:
    base_url: str
    request_type: str
    endpoint: Optional[str] = None
    headers: Optional[dict] = None
    params: Optional[Union[dict, str]] = None
    payload: Optional[dict] = None
    data: Optional[Union[dict, str]] = None
    file: Optional[bytes] = None

    def update_headers(self, value: dict):
        self.headers.update(value)

    def replace_headers(self, value: dict):
        self.headers = value

    def __post_init__(self):
        self.request_type = f"{self.request_type.lower()}"
        if self.endpoint is not None:
            self.base_url = sub("/$", "", self.base_url)
            self.base_url = f"{self.base_url}{self.endpoint}"
        if self.headers is None:
            self.headers = {
                "Content-type": "application/json",
                "Accept": "application/json",
            }
