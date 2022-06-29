from pydantic import BaseModel

from .stats import Stats


class Source(BaseModel):
    kktRegId: int
    fsId: int
    date: int
    ranges: str
    min: int
    max: int
    stats: Stats
    modifiedTime: int
