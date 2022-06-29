from pydantic import BaseModel

from .aggregation import Aggregation
from .fd_count import FdCounts


class Stats(BaseModel):
    firstDateTime: int
    lastDateTime: int
    flcErrorCount: int
    emailCount: int
    phoneCount: int
    fdCounts: FdCounts
    total: Aggregation
    sell: Aggregation
    sellReturn: Aggregation
    buy: Aggregation
    buyReturn: Aggregation
    totalCorrection: Aggregation
    sellCorrection: Aggregation
    buyCorrection: Aggregation
