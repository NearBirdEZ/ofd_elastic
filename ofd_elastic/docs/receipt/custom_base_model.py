from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    class Config:
        validate_assignment: bool = True
