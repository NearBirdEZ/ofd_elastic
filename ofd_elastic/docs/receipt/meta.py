from typing import Optional, Union
from pydantic import validator, Field
from datetime import datetime as dt

from .custom_base_model import CustomBaseModel
from .enums.doc_type import DocTypeEnum
from .setter_default_or_value import SetterDefaultOrValue


class Meta(CustomBaseModel):
    flc_validation_errors: Optional[str] = Field(alias='flcValidationErrors',
                                                 description='',
                                                 allow_mutation=False)
    flc_error: Optional[bool] = Field(alias='flcError',
                                      description='',
                                      allow_mutation=False)
    raw_data_size: Optional[int] = Field(alias='rawDataSize',
                                         description='',
                                         allow_mutation=False)
    user_inn: Optional[str] = Field(alias='userInn',
                                    description='',
                                    allow_mutation=False)
    kkt_reg_id: Optional[int] = Field(alias='kktRegId',
                                      description='',
                                      allow_mutation=False)
    doc_id: Optional[int] = Field(alias='docId',
                                  description='',
                                  allow_mutation=False)
    a_version: Optional[int] = Field(alias='aVersion',
                                     description='',
                                     allow_mutation=False)
    receive_time: Optional[dt] = Field(alias='receiveTimeMs',
                                       description='Время получения ФД ОФД.',
                                       allow_mutation=False)
    date_time: Optional[dt] = Field(alias='dateTimeMs',
                                    description='Время формирования ФД.',
                                    allow_mutation=False)
    uuid: Optional[str] = Field(alias='uuid',
                                description='',
                                allow_mutation=False)
    tag_number: Optional[int] = Field(alias='tagNumber',
                                      description='',
                                      allow_mutation=False)
    flc_version: Optional[int] = Field(alias='flcVersion',
                                       description='',
                                       allow_mutation=False)
    fs_id: Optional[int] = Field(alias='fsId',
                                 description='',
                                 allow_mutation=False)
    ffd_version: Optional[int] = Field(alias='ffdVersion',
                                       description='',
                                       allow_mutation=False)

    @validator("raw_data_size",
               "kkt_reg_id",
               "doc_id",
               "a_version",
               "tag_number",
               "flc_version",
               "fs_id",
               "ffd_version",
               pre=True,
               always=True,
               check_fields=False)
    def _set_int_fields(cls, value: Optional[int]) -> int:
        return SetterDefaultOrValue.set_number(value)

    @validator("flc_validation_errors", pre=True, always=True, check_fields=False)
    def _set_flc_validation_errors(cls, value: Union[str, bool]) -> Union[str, bool]:
        return SetterDefaultOrValue.set_union(value)

    @validator(
        "user_inn",
        "uuid",
        pre=True,
        always=True,
        check_fields=False)
    def _set_string_fields(cls, value: Optional[str]) -> str:
        return SetterDefaultOrValue.set_str(value)

    @validator("receive_time",
               "date_time",
               pre=True,
               always=True,
               check_fields=False)
    def _set_date_time_fields(cls, value: Optional[int]) -> dt:
        return SetterDefaultOrValue.set_date_time(value / 1000)

    @validator("flc_error", pre=True, always=True, check_fields=False)
    def _set_flc_error(cls, value: Optional[str]) -> bool:
        return SetterDefaultOrValue.set_bool(value)

    @validator("tag_number", pre=True, always=True, check_fields=False)
    def _set_system_tax(cls, value: Optional[int]) -> DocTypeEnum:
        return DocTypeEnum(value)
