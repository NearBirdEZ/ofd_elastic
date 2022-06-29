from pydantic import BaseModel


class FdCounts(BaseModel):
    totalFd: int
    fiscalReport: int
    fiscalReportCorrection: int
    openShift: int
    currentStateReport: int
    receipt: int
    receiptCorrection: int
    bso: int
    bsoCorrection: int
    closeShift: int
    closeArchive: int
