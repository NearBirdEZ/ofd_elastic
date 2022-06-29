from pydantic import BaseModel


class Aggregation(BaseModel):
    fdCount: int
    totalSum: int
    totalSumMin: int
    totalSumMax: int
    cashTotalSum: int
    ecashTotalSum: int
    prepaidSum: int
    creditSum: int
    provisionSum: int
    itemsCount: int
    nds0: int
    nds10: int
    nds18: int
    nds10110: int
    nds18118: int
    ndsNo: int
