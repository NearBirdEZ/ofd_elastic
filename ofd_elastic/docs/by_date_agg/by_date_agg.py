from typing import Optional
from pydantic import BaseModel, Field

from .source import Source


class ByDateAgg(BaseModel):
    index: Optional[str] = Field(..., alias='_index')
    id: Optional[str] = Field(..., alias='_id')
    type: Optional[str] = Field(..., alias='_type')
    source: Source = Field(..., alias='_source')
