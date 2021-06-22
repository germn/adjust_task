import datetime

from pydantic import BaseModel

from orm.models import Channel, Country, Os


class Metric(BaseModel):
    date: datetime.date
    channel: Channel
    country: Country
    os: Os
    impressions: int
    clicks: int
    installs: int
    spend: float
    revenue: float

    class Config:
        orm_mode = True
