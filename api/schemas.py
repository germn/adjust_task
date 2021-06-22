from typing import Optional, Literal
import datetime

from pydantic import BaseModel

from orm.models import Channel, Country, Os


class Metric(BaseModel):
    date: Optional[datetime.date]
    channel: Optional[Channel]
    country: Optional[Country]
    os: Optional[Os]
    impressions: int
    clicks: int
    installs: int
    spend: float
    revenue: float
    cpi: Optional[float]

    class Config:
        orm_mode = True


def _get_sorting_type():
    """
    Return type that allows string containing `Metric` attribute name
    or `Metric` attribute name preceded by dash.
    """
    fields = list(Metric.schema()["properties"])
    desc_fields = [f"-{field}" for field in fields]
    return Literal[tuple(fields + desc_fields)]


SortByFields = _get_sorting_type()


GroupByFields = Literal["date", "channel", "country", "os"]
