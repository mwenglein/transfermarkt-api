from datetime import datetime
from typing import Optional

from dateutil import parser
from pydantic import BaseModel, Field, field_validator


class TransfermarktBaseModel(BaseModel):
    # id: Optional[str] = Field(default=None)
    # updated_at: datetime = Field(alias="updatedAt", default_factory=datetime.now)

    # @field_validator("*", mode="before")
    # def parse_date(cls, value: str, field: ValidationInfo):
    #     if cls.__fields__[field.field_name].annotation == date:
    #         return parser.parse(value).date()
    #     return value

    @field_validator("dob", "joined_on", "contract", "founded_on", "members_date", mode="before", check_fields=False)
    def parse_str_to_date(cls, v: str):
        return parser.parse(v).date()

    @field_validator("height", mode="before", check_fields=False)
    def height_format(cls, v: str):
        return int(v.replace(",", "").replace("m", ""))

    @field_validator("market_value", "current_market_value", mode="before", check_fields=False)
    def parse_market_value(cls, v: str):
        v = v.replace("m", "000000").replace("k", "000").replace("€", "").replace(".", "").replace("-", "")
        if v:
            return int(v)
        return None


class IDMixin(BaseModel):
    id: str


class AuditMixin(BaseModel):
    updated_at: datetime = Field(alias="updatedAt", default_factory=datetime.now)
