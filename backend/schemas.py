from datetime import  datetime
from typing import Optional
from pydantic import BaseModel



class ClientInfoIn(BaseModel):
    phone: str
    phone_code: str
    tag: str
    time_zone: str


class MailingInfoIn(BaseModel):
    date_time_start: datetime
    message_text: str
    mob_code_filter: str
    tag_filter: str
    date_time_end: datetime