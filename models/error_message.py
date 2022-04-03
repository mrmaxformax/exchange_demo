from typing import List
from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass
class ErrorMessage:
    error: List[str]
    error_message: str = Field(default='', init=False)

    def __post_init__(self):
        self.error_message = "\n".join(self.error)
