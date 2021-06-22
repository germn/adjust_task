import enum

from sqlalchemy import Column, Integer, Date, Enum, Float

from orm.session import Base


class Channel(enum.Enum):
    adcolony = "adcolony"
    apple_search_ads = "apple_search_ads"
    chartboost = "chartboost"
    facebook = "facebook"
    google = "google"
    unityads = "unityads"
    vungle = "vungle"


class Country(enum.Enum):
    CA = "CA"
    DE = "DE"
    FR = "FR"
    GB = "GB"
    US = "US"


class Os(enum.Enum):
    android = "android"
    ios = "ios"


class Metric(Base):
    __tablename__ = "metrics"

    metric_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    channel = Column(Enum(Channel), nullable=False)
    country = Column(Enum(Country), nullable=False)
    os = Column(Enum(Os), nullable=False)
    impressions = Column(Integer, nullable=False)
    clicks = Column(Integer, nullable=False)
    installs = Column(Integer, nullable=False)
    spend = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
