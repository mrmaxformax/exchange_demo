from typing import List, Any
from pydantic import BaseModel


class ApiResponse(BaseModel):
    error: List[str]
    result: Any
