from typing import Optional
from pydantic import BaseModel

from .meta import Meta
from .request_message import Requestmessage


class Source(BaseModel):
    requestmessage: Optional[Requestmessage]
    meta: Optional[Meta]
    id: Optional[str]
