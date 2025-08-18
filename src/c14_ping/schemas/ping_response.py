from typing import Literal
from pydantic import BaseModel


class PingResponse(BaseModel):
    pong: Literal['ping'] = 'ping'
