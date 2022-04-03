import re
from datetime import  datetime
from typing import Optional
from pydantic import BaseModel, validator



class ClientInfoIn(BaseModel):
    phone: str
    phone_code: str
    tag: str
    time_zone: str

    @validator('phone')
    def phone_validation(cls, v):
        regex = r"^[7]\d{10}$"
        if v and not re.match(regex, v):
            raise ValueError("Phone Number Invalid. Format 7XXXXXXXXXX, where X-digit")
        return v

    @validator('phone_code')
    def phone_code_validation(cls, v):
        regex = r"\d{3}$"
        if v and not re.match(regex, v):
            raise ValueError("Phone code Invalid. Format XXX, where X-digit")
        return v


class MailingInfoIn(BaseModel):
    date_time_start: datetime
    message_text: str
    mob_code_filter: str
    tag_filter: str
    date_time_end: datetime

    @validator('mob_code_filter')
    def phone_code_filter_validation(cls, v):
        regex = r"\d{3}$"
        if v and not re.match(regex, v):
            raise ValueError("Phone code Invalid. Format XXX, where X-digit")
        return v