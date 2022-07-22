from typing import Optional

from pydantic import BaseModel, Field, validator


class PartitionAgg(BaseModel):
    head_agg: str = Field(alias='key',
                          description='Первый ключ агрегации',
                          allow_mutation=False)
    sub_aggs: Optional[list[str]] = Field(alias='name2',
                                          description='Второй ключ агрегации',
                                          allow_mutation=False)

    class Config:
        validate_assignment: bool = True

    @validator("sub_aggs", pre=True, always=True, check_fields=False)
    def _set_sub_aggs(cls, values: Optional[dict]) -> Optional[list[str]]:
        return [bucket.get('key') for bucket in values["buckets"]] if values else []
